"""Context processor para notificaciones del sistema."""
from django.db.utils import OperationalError, ProgrammingError
import hashlib


def _notif(key, tipo, icono, titulo, detalle, url):
    return {"key": key, "tipo": tipo, "icono": icono, "titulo": titulo, "detalle": detalle, "url": url}


def notificaciones_context(request):
    if not request.user.is_authenticated:
        return {"notificaciones": [], "notif_count": 0}

    notifs = []

    try:
        from INVENTARIO.models import Producto
        from django.db.models import F
        sin_stock = Producto.objects.filter(stock=0, stock_minimo__gt=0).count()
        bajo_min = Producto.objects.filter(stock_minimo__gt=0, stock__gt=0, stock__lte=F('stock_minimo')).count()
        if sin_stock:
            notifs.append(_notif(
                "stock_agotado", "danger", "bi-exclamation-triangle-fill",
                f"{sin_stock} producto{'s' if sin_stock > 1 else ''} agotado{'s' if sin_stock > 1 else ''}",
                "Sin stock disponible",
                "/inventario/reportes/bajo-stock/",
            ))
        if bajo_min:
            notifs.append(_notif(
                "stock_bajo", "warning", "bi-box-seam",
                f"{bajo_min} producto{'s' if bajo_min > 1 else ''} bajo mínimo",
                "Stock por debajo del mínimo configurado",
                "/inventario/reportes/bajo-stock/",
            ))
    except (OperationalError, ProgrammingError, Exception):
        pass

    try:
        from CONTABILIDAD.models import CuentaPorCobrar
        from datetime import date
        hoy = date.today()
        cxc = CuentaPorCobrar.objects.filter(fecha_vencimiento__lt=hoy).exclude(estado__in=['PAGADO', 'ANULADO']).count()
        if cxc:
            notifs.append(_notif(
                "cxc_vencidas", "warning", "bi-arrow-down-circle",
                f"{cxc} cuenta{'s' if cxc > 1 else ''} por cobrar vencida{'s' if cxc > 1 else ''}",
                "Cuentas pendientes de cobro",
                "/contabilidad/reportes/antiguedad-cxc/",
            ))
    except (OperationalError, ProgrammingError, Exception):
        pass

    try:
        from CONTABILIDAD.models import CuentaPorPagar
        from datetime import date
        hoy = date.today()
        cxp = CuentaPorPagar.objects.filter(fecha_vencimiento__lt=hoy).exclude(estado__in=['PAGADO', 'ANULADO']).count()
        if cxp:
            notifs.append(_notif(
                "cxp_vencidas", "danger", "bi-arrow-up-circle",
                f"{cxp} cuenta{'s' if cxp > 1 else ''} por pagar vencida{'s' if cxp > 1 else ''}",
                "Pagos pendientes a proveedores",
                "/contabilidad/reportes/antiguedad-cxp/",
            ))
    except (OperationalError, ProgrammingError, Exception):
        pass

    try:
        from FE.models import FacturaElectronica
        from django.utils import timezone
        from datetime import timedelta
        hace_24h = timezone.now() - timedelta(hours=24)
        rechazados = FacturaElectronica.objects.filter(
            fecha_emision__gte=hace_24h.date(), recibido_mh=False, firmado=True
        ).count()
        if rechazados:
            notifs.append(_notif(
                "dte_sin_mh", "warning", "bi-file-earmark-x",
                f"{rechazados} DTE{'s' if rechazados > 1 else ''} sin recepción de MH",
                "Documentos firmados no recibidos por Hacienda",
                "/fe/listar_facturas/?recibido_mh=False",
            ))
    except (OperationalError, ProgrammingError, Exception):
        pass

    try:
        from FE.models import Emisor_fe
        from datetime import date, timedelta
        emisor = Emisor_fe.objects.first()
        if emisor:
            try:
                susc = emisor.suscripcion
                if susc and susc.fecha_fin:
                    dias = (susc.fecha_fin - date.today()).days
                    if 0 < dias <= 15:
                        notifs.append(_notif(
                            "suscripcion_vence", "info", "bi-clock-history",
                            f"Suscripción vence en {dias} día{'s' if dias > 1 else ''}",
                            f"Vencimiento: {susc.fecha_fin.strftime('%d/%m/%Y')}",
                            "#",
                        ))
            except Exception:
                pass
    except (OperationalError, ProgrammingError, Exception):
        pass

    return {
        "notificaciones": notifs,
        "notif_count": len(notifs),
    }
