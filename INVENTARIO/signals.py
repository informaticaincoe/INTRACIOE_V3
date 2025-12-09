from django.db.models import F, Value
from django.db.models.functions import Greatest
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from .models import (
    DevolucionCompra, MovimientoInventario, Producto,
    DetalleCompra, DetalleDevolucionCompra, DetalleDevolucionVenta,
    AjusteInventario
)

# ==========================
# Helpers
# ==========================
def _signed_delta(tipo, qty):
    """
    Entrada:  +abs(qty)
    Salida:   -abs(qty)
    Ajuste:    qty (puede ser + / -)
    """
    if tipo == 'Entrada':
        return abs(qty)
    if tipo == 'Salida':
        return -abs(qty)
    return qty


# ==========================
# Stock por MovimientoInventario
# (ÚNICA fuente de verdad)
# ==========================
@receiver(pre_save, sender=MovimientoInventario)
def _store_old_values(sender, instance, **kwargs):
    """ Guarda valores previos para recalcular delta en updates. """
    print("<<<<_store_old_values")
    print(f"<<<<<_store_old_values {instance} - {sender}")
    
    if instance.pk:        
        old = sender.objects.get(pk=instance.pk)
        
        instance._old_producto_id = old.producto_id
        instance._old_tipo = old.tipo
        instance._old_cantidad = old.cantidad
        
    else:        
        instance._old_producto_id = None


@receiver(post_save, sender=MovimientoInventario)
def _apply_stock_on_save(sender, instance, created, **kwargs):
    """
    - create: aplica delta nuevo
    - update: revierte delta viejo y aplica delta nuevo
    (con tope en 0 para no negativos)
    """
    print(">>> Devolucion o asignacion de stock")
    
    if created:
        delta = _signed_delta(instance.tipo, instance.cantidad)
        print(f">>> cantidad a agregar {Value(delta)}")
        
        Producto.objects.filter(pk=instance.producto_id).update(
            stock=Greatest(F('stock') + Value(delta), Value(0))
        )
        
        return
    
    

    # Update
    if getattr(instance, '_old_producto_id', None) is not None:            
        old_delta = _signed_delta(getattr(instance, '_old_tipo'), getattr(instance, '_old_cantidad'))
        
        # Revertir el viejo (tope en 0)
        Producto.objects.filter(pk=instance._old_producto_id).update(
            stock=Greatest(F('stock') - Value(old_delta), Value(0))
        )

    new_delta = _signed_delta(instance.tipo, instance.cantidad)
    
    Producto.objects.filter(pk=instance.producto_id).update(
        stock=Greatest(F('stock') + Value(new_delta), Value(0))
    )


@receiver(pre_delete, sender=MovimientoInventario)
def _revert_stock_on_delete(sender, instance, **kwargs):
    """ Al borrar un movimiento, revertimos su efecto (tope en 0). """
    delta = _signed_delta(instance.tipo, instance.cantidad)
    Producto.objects.filter(pk=instance.producto_id).update(
        stock=Greatest(F('stock') - Value(delta), Value(0))
    )


# ==========================
# Generación automática de Movimientos
# (NO toques stock aquí; solo creamos MovimientoInventario)
# ==========================

@receiver(post_save, sender=DetalleCompra)
def crear_movimiento_desde_detalle_compra(sender, instance, created, **kwargs):
    if not created:
        return
    producto = instance.producto
    almacen = producto.almacenes.first()
    if not almacen:
        return

    ref = f'Compra #{instance.compra_id} - det #{instance.id}'
    # Defensa simple antireintento:
    if not MovimientoInventario.objects.filter(referencia=ref, producto=producto).exists():
        MovimientoInventario.objects.create(
            producto=producto,
            almacen=almacen,
            tipo='Entrada',
            cantidad=instance.cantidad,
            referencia=ref
        )


@receiver(post_save, sender=DetalleDevolucionCompra)
def crear_movimiento_salida_devolucion_compra(sender, instance, created, **kwargs):
    if not created:
        return
    # Crear salida solo si la devolución madre está Aprobada
    if instance.devolucion.estado != 'Aprobada':
        return

    producto = instance.producto
    almacen = producto.almacenes.first()
    if not almacen:
        return
    
    print(f"Decolucion de compra {instance}")

    ref = f'Devolución Compra #{instance.devolucion_id} - det #{instance.id}'
    if not MovimientoInventario.objects.filter(referencia=ref, producto=producto).exists():
        MovimientoInventario.objects.create(
            producto=producto,
            almacen=almacen,
            tipo='Salida',
            cantidad=instance.cantidad,
            referencia=ref
        )


@receiver(post_save, sender=DevolucionCompra)
def on_cambio_estado_devolucion(sender, instance, created, **kwargs):
    # Si cambió a Aprobada, crear salidas para detalles que aún no las tengan    
    if not created and instance.estado == 'Aprobada':
        for d in instance.detalles.all():            
            ref = f'Devolución Compra #{instance.id} - det #{d.id}'
            
            if not MovimientoInventario.objects.filter(referencia=ref, producto=d.producto).exists():
                MovimientoInventario.objects.create(
                    producto=d.producto,
                    almacen=d.producto.almacenes.first(),
                    tipo='Salida',
                    cantidad=d.cantidad,
                    referencia=ref
                )
                
    # Si cambió a Rechazada, eliminar salidas existentes (pre_delete de Movimiento revertirá stock)
    if not created and instance.estado == 'Rechazada':
        MovimientoInventario.objects.filter(
            referencia__startswith=f'Devolución Compra #{instance.id}'
        ).delete()

@receiver(post_save, sender=DetalleDevolucionVenta)
def crear_movimiento_entrada_devolucion_venta(sender, instance, created, **kwargs):
    if not created:
        return
    producto = instance.producto
    almacen = producto.almacenes.first()
    if not almacen:
        return

    num_factura = instance.devolucion.num_factura or "SIN_NUM_FACTURA"

    # Puedes diseñar la referencia como quieras
    ref = f'Dev Venta #{instance.devolucion_id} (Fact: {num_factura}) - det #{instance.id}'
        
    if not MovimientoInventario.objects.filter(referencia=ref, producto=producto).exists():
        MovimientoInventario.objects.create(
            producto=producto,
            almacen=almacen,
            tipo='Entrada',
            cantidad=instance.cantidad,
            referencia=ref
        )


@receiver(post_save, sender=AjusteInventario)
def crear_movimiento_por_ajuste(sender, instance, created, **kwargs):
    print("Creando movimiento por ajuste")
    if not created:
        return
    qty = instance.cantidad_ajustada
    if qty == 0:
        return

    if qty > 0:
        movimiento_tipo = 'Entrada'
        movimiento_cantidad = qty
    else:
        movimiento_tipo = 'Salida'
        movimiento_cantidad = abs(qty)

    ref = f'Ajuste Inventario #{instance.id}'
    if not MovimientoInventario.objects.filter(referencia=ref, producto=instance.producto).exists():
        MovimientoInventario.objects.create(
            producto=instance.producto,
            almacen=instance.almacen,
            tipo=movimiento_tipo,
            cantidad=movimiento_cantidad,
            referencia=ref
        )
