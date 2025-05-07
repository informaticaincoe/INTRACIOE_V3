# views.py
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from FE.models import FacturaElectronica
from .serializers import AnexoConsumidorFinalRowSerializer

class AnexoConsumidorFinalAPIView(APIView):
    """
    Devuelve JSON con todas las filas para el Anexo de Consumidor Final (tipo_dte='01').
    """

    def get(self, request, *args, **kwargs):
        qs = FacturaElectronica.objects.filter(tipo_dte__codigo='01').order_by('fecha_emision')
        rows = []
        for f in qs:
            rows.append({
                "fecha": f.fecha_emision.strftime("%d/%m/%Y"),
                "clase": "4",
                "tipo": f.tipo_dte.codigo,
                "numero_resolucion": f.numero_control or "",
                "serie_documento": f.codigo_generacion.hex.upper() if f.codigo_generacion else "",
                "control_interno_del": "",
                "control_interno_al": "",
                "numero_doc_del": "",
                "numero_doc_al": "",
                "numero_maquina": "",
                "ventas_exentas": f.total_exentas or 0,
                "ventas_internas_exentas": 0,
                "ventas_no_sujetas": f.total_no_sujetas or 0,
                "ventas_gravadas": f.total_gravadas or 0,
                "exportaciones_dentro": 0,
                "exportaciones_fuera": 0,
                "exportaciones_servicio": 0,
                "ventas_zonas_francas": 0,
                "ventas_cuenta_terceros": 0,
                "total_ventas": f.total_pagar or 0,
                "tipo_operacion": f.condicion_operacion.codigo if f.condicion_operacion else "",
                "tipo_ingreso": "",
                "numero_anexo": "2",
            })
        serializer = AnexoConsumidorFinalRowSerializer(rows, many=True)
        return Response(serializer.data)