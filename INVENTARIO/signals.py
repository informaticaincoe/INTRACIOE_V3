from django.db.models import F, Value
from django.db.models.functions import Greatest
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AjusteInventario, DetalleCompra, DetalleDevolucionCompra, DetalleDevolucionVenta, MovimientoInventario, Producto, DevolucionVenta, DevolucionCompra

@receiver(post_save, sender=MovimientoInventario)
def ajustar_stock(sender, instance, created, **kwargs):
    if not created:
        return

    producto_id = instance.producto_id
    cantidad = instance.cantidad
    tipo = instance.tipo
    print(f"[Signal] Ajustando stock: producto={producto_id} cantidad={cantidad} tipo={tipo}")

    if tipo == 'Salida':
        # Resta atómica y no negativa
        Producto.objects.filter(pk=producto_id).update(
            stock=Greatest(F('stock') - Value(cantidad), Value(0))
        )
    elif tipo == 'Entrada':
        # Entrada suma stock
        Producto.objects.filter(pk=producto_id).update(
            stock=F('stock') + Value(cantidad)
        )
    else:
        # Ajuste u otros tipos: sumar o restar según la cantidad ajustada (que puede ser negativa)
        Producto.objects.filter(pk=producto_id).update(
            stock=Greatest(F('stock') + Value(instance.cantidad), Value(0))
        )

    # Volvemos a leer y mostrar el nuevo stock para verificar
    nuevo = Producto.objects.get(pk=producto_id).stock
    print(f"[Signal] Nuevo stock para producto {producto_id}: {nuevo}")

############################################################################################
## COMPRAS
############################################################################################

# Crear movimiento al guardar un DetalleCompra
@receiver(post_save, sender=DetalleCompra)
def crear_movimiento_desde_detalle(sender, instance, created, **kwargs):
    if not created:
        return

    producto = instance.producto
    # Elegir almacén; aquí el primero asociado
    almacen = producto.almacenes.first()
    if not almacen:
        return

    MovimientoInventario.objects.create(
        producto=producto,
        almacen=almacen,
        tipo='Entrada',
        cantidad=instance.cantidad,
        referencia=f'Compra #{instance.compra_id}'
    )


@receiver(post_save, sender=DetalleDevolucionCompra)
def crear_movimiento_salida_devolucion_compra(sender, instance, created, **kwargs):
    """
    Cuando se crea un DetalleDevolucionCompra, generamos un MovimientoInventario
    de tipo 'Salida' para descontar el stock.
    """
    if not created:
        return

    producto = instance.producto
    # Elegimos un almacén; aquí usamos el primero asociado
    almacen = producto.almacenes.first()
    if not almacen:
        return

    MovimientoInventario.objects.create(
        producto=producto,
        almacen=almacen,
        tipo='Salida',
        cantidad=instance.cantidad,
        referencia=f'Devolución Compra #{instance.devolucion.id}'
    )

############################################################################################
## VENTAS
############################################################################################

@receiver(post_save, sender=DetalleDevolucionVenta)
def crear_movimiento_entrada_devolucion(sender, instance, created, **kwargs):
    """
    Cada vez que se cree un DetalleDevolucionVenta, generamos un MovimientoInventario
    de tipo 'Entrada' para reponer el stock.
    """
    if not created:
        return

    producto = instance.producto
    # Usamos el primer almacén asociado al producto; ajústalo si necesitas otro criterio
    almacen = producto.almacenes.first()
    if not almacen:
        return

    MovimientoInventario.objects.create(
        producto=producto,
        almacen=almacen,
        tipo='Entrada',
        cantidad=instance.cantidad,
        referencia=f'Devolución Venta #{instance.devolucion.id}'
    )


############################################################################################
## AJUSTE DE INVENTARIO
############################################################################################

@receiver(post_save, sender=AjusteInventario)
def crear_movimiento_por_ajuste(sender, instance, created, **kwargs):
    """
    Cada vez que se crea un AjusteInventario, generamos un MovimientoInventario:
    - Si cantidad_ajustada > 0: tipo 'Entrada' (suma stock)
    - Si cantidad_ajustada < 0: tipo 'Salida'  (resta stock)
    """
    if not created:
        return

    producto = instance.producto
    almacen  = instance.almacen
    qty      = instance.cantidad_ajustada

    if qty == 0:
        # Sin cambio, no crear movimiento
        return

    if qty > 0:
        movimiento_tipo = 'Entrada'
        movimiento_cantidad = qty
    else:
        movimiento_tipo = 'Salida'
        movimiento_cantidad = abs(qty)

    MovimientoInventario.objects.create(
        producto=producto,
        almacen=almacen,
        tipo=movimiento_tipo,
        cantidad=movimiento_cantidad,
        referencia=f'Ajuste Inventario #{instance.id}'
    )