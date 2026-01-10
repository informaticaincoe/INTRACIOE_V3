# FE/services.py
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
import uuid

from FE.models import FacturaElectronica, DetalleFactura, Tipo_dte, CondicionOperacion, TipoMoneda
from INVENTARIO.models import Producto

# Ajusta según tus catálogos reales:
COD_DTE_CF = "01"  # consumidor final

@transaction.atomic
def crear_factura_cf_desde_pedido(*, pedido, usuario, receptor=None, formas_pago_json=None):
    """
    Mapea Pedido/DetallePedido -> FacturaElectronica/DetalleFactura.
    """
    # 1) tipo DTE consumidor final
    tipo_dte = Tipo_dte.objects.get(codigo=COD_DTE_CF)

    # 2) emisor (según tu lógica existente)
    # ideal: reutiliza tu helper _get_emisor_for_user(...) pero aquí no tenemos request
    # así que asumo que puedes resolver emisor por usuario:
    emisor = usuario.perfilusuario.emisor_fe  # <-- AJUSTA a tu proyecto real

    # 4) moneda/condición
    moneda = TipoMoneda.objects.first()
    cond_op = CondicionOperacion.objects.first()  # contado, etc.

    factura = FacturaElectronica.objects.create(
        usuario=usuario,
        version="1",
        tipo_dte=tipo_dte,
        codigo_generacion=uuid.uuid4(),
        tipomodelo=emisor.modelofacturacion_default,   # AJUSTA
        tipomoneda=moneda,
        dteemisor=emisor,
        dtereceptor=receptor,

        # resumen (mínimo)
        total_no_sujetas=Decimal("0.00"),
        total_exentas=Decimal("0.00"),
        total_gravadas=pedido.subtotal - pedido.descuento_total,
        sub_total_ventas=pedido.subtotal,
        descuento_gravado=pedido.descuento_total,
        total_descuento=pedido.descuento_total,
        sub_total=pedido.subtotal - pedido.descuento_total,
        total_iva=pedido.iva_total,
        total_pagar=pedido.total,
        condicion_operacion=cond_op,
        formas_Pago=(formas_pago_json or []),

        json_original={},  # lo llenas cuando generes el JSON real para MH
    )

    # 5) detalles
    for i, det in enumerate(pedido.detalles.select_related("platillo__producto"), start=1):
        prod = det.platillo.producto
        if not prod:
            # si por algún motivo no existe producto asociado, evita facturar
            raise ValueError(f"Platillo {det.platillo_id} no tiene Producto asociado.")

        neto = det.subtotal_linea - det.descuento_monto
        gravadas = neto  # si aplica IVA

        DetalleFactura.objects.create(
            factura=factura,
            producto=prod,
            cantidad=det.cantidad,
            unidad_medida=get_unidad_default(prod),  # implementa según inventario

            precio_unitario=det.precio_unitario,
            iva_item=det.iva_monto,

            ventas_no_sujetas=Decimal("0.00"),
            ventas_exentas=Decimal("0.00"),
            ventas_gravadas=gravadas,

            pre_sug_venta=det.precio_unitario,
            no_gravado=Decimal("0.00"),
            tiene_descuento=(det.descuento_monto > 0),
            descuento=None,  # si quieres mapear a tu modelo Descuento, aquí
        )

    # Aquí normalmente llamas tu proceso de:
    # - construir JSON DTE
    # - firmar
    # - enviar a MH
    # - guardar sello/recibido
    # Eso ya lo tienes en tu flujo FE; la idea es invocarlo aquí o en un job.

    return factura
