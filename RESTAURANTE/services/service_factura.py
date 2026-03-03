from decimal import ROUND_HALF_UP, Decimal
from FE.models import FacturaElectronica
from django.shortcuts import get_object_or_404
from django.utils import timezone

from RESTAURANTE.models import Caja

def to_dec(v):
    if v is None:
        return Decimal("0.00")
    return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    


def finalizar_venta_exitosa(factura_id):
    print("FACTURA DENTRO FUNC ", factura_id)
    factura = get_object_or_404(FacturaElectronica, id=factura_id)

    # ---------------------------
    # 1) CAJA
    # ---------------------------
    caja_actual = Caja.objects.filter(estado="ABIERTA").first()
    if caja_actual:
        monto_total = to_dec(factura.total_pagar)

        caja_actual.total_ventas = to_dec(caja_actual.total_ventas) + monto_total

        pagos = (factura.json_original or {}).get("resumen", {}).get("pagos", []) or []
        for pago in pagos:
            codigo = (pago.get("codigo") or "").strip()
            
            monto_pago = to_dec(pago.get("montoPago", pago.get("monto", 0)))
            print("monto_pago ", monto_pago)
            

            if codigo == "01":
                caja_actual.total_efectivo = to_dec(caja_actual.total_efectivo) + monto_pago                
            elif codigo == "03":
                
                caja_actual.total_tarjeta = to_dec(caja_actual.total_tarjeta) + monto_pago

        caja_actual.save(update_fields=["total_ventas", "total_efectivo", "total_tarjeta"])

    # ---------------------------
    # 2) CERRAR CUENTA + PEDIDO
    # ---------------------------
    cuenta = getattr(factura, "cuenta_pedido", None)

    # Si NO lo agregaste y quieres fallback:
    if cuenta is None:
        # intenta resolver por consulta (seguro)
        from RESTAURANTE.models import CuentaPedido
        cuenta = CuentaPedido.objects.filter(factura=factura_id).select_related("pedido", "pedido__mesa").first()

    if not cuenta:
        return

    if cuenta.estado != "PAGADA":
        cuenta.estado = "PAGADA"
        cuenta.pagado_el = timezone.now()
        cuenta.save(update_fields=["estado", "pagado_el"])

    pedido = cuenta.pedido
    print("PEDIDO ESTADO ", pedido.estado)
    # Si todas las cuentas están resueltas, pagar pedido y liberar mesa
    if not pedido.cuentas.exclude(estado__in=["PAGADA", "ANULADO"]).exists():
        if pedido.estado != "PAGADO":
            pedido.estado = "PAGADO"
            pedido.pagado_el = timezone.now()
            pedido.save(update_fields=["estado", "pagado_el"])
        
        mesa = pedido.mesa
        
        if mesa.estado != "LIBRE":
            mesa.estado = "PAGADO"
            mesa.save(update_fields=["estado"])