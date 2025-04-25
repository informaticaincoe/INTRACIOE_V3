from django.db.models import F, Value
from django.db.models.functions import Greatest
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovimientoInventario, Producto

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