"""
Generación automática de asientos contables, CxC y CxP.

Llamar desde signals o directamente desde las vistas de compras/facturación.
"""
import logging
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

logger = logging.getLogger(__name__)


def generar_contabilidad_venta(factura, usuario=None):
    """
    Genera CxC + Asiento contable al crear/aprobar una factura.

    Asiento:
        Debe: CxC (total con IVA)
        Haber: Ingresos por ventas (subtotal sin IVA)
        Haber: IVA Débito Fiscal (IVA)
    """
    from .models import (
        ConfiguracionContable, AsientoContable, LineaAsiento, CuentaPorCobrar
    )

    config = ConfiguracionContable.get()
    if not config.cuenta_cxc or not config.cuenta_ingresos_ventas:
        logger.warning("Contabilidad auto: faltan cuentas configuradas para ventas")
        return None

    total = Decimal(str(factura.total_pagar or 0))
    if total <= 0:
        return None

    # Calcular IVA y subtotal
    iva = Decimal(str(getattr(factura, 'total_iva', 0) or 0))
    if iva <= 0:
        # Intentar calcular desde detalles
        from django.db.models import Sum
        iva_det = factura.detalles.aggregate(t=Sum('iva_item'))['t'] or 0
        iva = Decimal(str(iva_det))
    subtotal = total - iva

    fecha = getattr(factura, 'fecha_emision', None) or timezone.localdate()
    if hasattr(fecha, 'date'):
        fecha = fecha.date()
    elif isinstance(fecha, str):
        from datetime import date
        fecha = date.fromisoformat(fecha)

    receptor_nombre = ''
    if hasattr(factura, 'receptor') and factura.receptor:
        receptor_nombre = factura.receptor.nombre
    elif hasattr(factura, 'dtereceptor') and factura.dtereceptor:
        receptor_nombre = factura.dtereceptor.nombre

    # ── Crear asiento contable ──
    estado = 'CONFIRMADO' if config.auto_confirmar_asientos else 'BORRADOR'
    asiento = AsientoContable.objects.create(
        fecha=fecha,
        concepto=f'Venta factura #{factura.id} – {receptor_nombre}',
        estado=estado,
        creado_por=usuario,
    )

    # Debe: Cuentas por Cobrar (total)
    LineaAsiento.objects.create(
        asiento=asiento, cuenta=config.cuenta_cxc,
        descripcion=f'CxC {receptor_nombre}',
        debe=total, haber=0
    )
    # Haber: Ingresos (subtotal sin IVA)
    LineaAsiento.objects.create(
        asiento=asiento, cuenta=config.cuenta_ingresos_ventas,
        descripcion=f'Venta factura #{factura.id}',
        debe=0, haber=subtotal
    )
    # Haber: IVA Débito Fiscal
    if iva > 0 and config.cuenta_iva_debito_fiscal:
        LineaAsiento.objects.create(
            asiento=asiento, cuenta=config.cuenta_iva_debito_fiscal,
            descripcion=f'IVA 13% factura #{factura.id}',
            debe=0, haber=iva
        )

    # ── Crear CxC ──
    cxc = None
    if hasattr(factura, 'receptor') and factura.receptor:
        cxc = CuentaPorCobrar.objects.create(
            factura=factura,
            receptor=factura.receptor,
            fecha_emision=fecha,
            fecha_vencimiento=fecha + timedelta(days=config.dias_vencimiento_cxc),
            monto_original=total,
            creado_por=usuario,
        )

    logger.info(f"Contabilidad venta: asiento #{asiento.numero}, CxC #{cxc.pk if cxc else 'N/A'}")
    return asiento


def generar_contabilidad_compra(compra, usuario=None):
    """
    Genera CxP + Asiento contable al crear una compra.

    Asiento:
        Debe: Compras/Inventario (subtotal sin IVA)
        Debe: IVA Crédito Fiscal (IVA)
        Haber: CxP (total con IVA)
    """
    from .models import (
        ConfiguracionContable, AsientoContable, LineaAsiento, CuentaPorPagar
    )

    config = ConfiguracionContable.get()
    if not config.cuenta_cxp or not config.cuenta_compras:
        logger.warning("Contabilidad auto: faltan cuentas configuradas para compras")
        return None

    total = Decimal(str(compra.total or 0))
    if total <= 0:
        return None

    # Calcular IVA desde detalles
    from django.db.models import Sum
    iva = Decimal(str(
        compra.detalles.aggregate(t=Sum('iva_item'))['t'] or 0
    ))
    subtotal = total - iva

    fecha = compra.fecha
    if hasattr(fecha, 'date'):
        fecha = fecha.date()
    elif isinstance(fecha, str):
        from datetime import date
        fecha = date.fromisoformat(fecha)

    proveedor_nombre = compra.proveedor.nombre if compra.proveedor else ''

    # ── Crear asiento contable ──
    estado = 'CONFIRMADO' if config.auto_confirmar_asientos else 'BORRADOR'
    asiento = AsientoContable.objects.create(
        fecha=fecha,
        concepto=f'Compra #{compra.id} – {proveedor_nombre}',
        estado=estado,
        creado_por=usuario,
    )

    # Debe: Compras/Inventario (subtotal)
    cuenta_debe = config.cuenta_inventario or config.cuenta_compras
    LineaAsiento.objects.create(
        asiento=asiento, cuenta=cuenta_debe,
        descripcion=f'Compra #{compra.id} – {proveedor_nombre}',
        debe=subtotal, haber=0
    )
    # Debe: IVA Crédito Fiscal
    if iva > 0 and config.cuenta_iva_credito_fiscal:
        LineaAsiento.objects.create(
            asiento=asiento, cuenta=config.cuenta_iva_credito_fiscal,
            descripcion=f'IVA 13% compra #{compra.id}',
            debe=iva, haber=0
        )
    # Haber: Cuentas por Pagar (total)
    LineaAsiento.objects.create(
        asiento=asiento, cuenta=config.cuenta_cxp,
        descripcion=f'CxP {proveedor_nombre}',
        debe=0, haber=total
    )

    # ── Crear CxP ──
    cxp = CuentaPorPagar.objects.create(
        compra=compra,
        proveedor=compra.proveedor,
        fecha_emision=fecha,
        fecha_vencimiento=fecha + timedelta(days=config.dias_vencimiento_cxp),
        monto_original=total,
        creado_por=usuario,
    )

    logger.info(f"Contabilidad compra: asiento #{asiento.numero}, CxP #{cxp.pk}")
    return asiento
