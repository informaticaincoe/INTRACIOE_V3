from datetime import datetime, time, timedelta
from decimal import ROUND_HALF_UP, ConversionSyntax, Decimal
from itertools import count
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import pytz
import requests
import os, json, uuid
from django.db import transaction
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import enviar_contingencia_hacienda_view, enviar_factura_invalidacion_hacienda_view, firmar_contingencia_view, firmar_factura_anulacion_view, invalidacion_dte_view, generar_json, num_to_letras, agregar_formas_pago_api, generar_json_contingencia, generar_json_doc_ajuste, obtener_listado_productos_view
from INVENTARIO.serializers import DescuentoSerializer

from .serializers import (
    AmbienteSerializer, EventoContingenciaSerializer, FacturaListSerializer, 
    FormasPagosSerializer, LoteContingenciaSerializer, ReceptorSerializer, FacturaElectronicaSerializer, EmisorSerializer, 
    TipoDteSerializer, TiposGeneracionDocumentoSerializer,

    ActividadEconomicaSerializer, ModelofacturacionSerializer,
    TipoTransmisionSerializer, TipoContingenciaSerializer, TipoRetencionIVAMHSerializer,
    TiposEstablecimientosSerializer, TiposServicio_MedicoSerializer,
    OtrosDicumentosAsociadoSerializer, TiposDocIDReceptorSerializer,
    PaisSerializer, DepartamentoSerializer, MunicipioSerializer, CondicionOperacionSerializer,                                                                                                                                                                                             
    PlazoSerializer, TipoDocContingenciaSerializer, TipoInvalidacionSerializer,
    TipoDonacionSerializer, TipoPersonaSerializer, TipoTransporteSerializer, INCOTERMS_Serializer,
    TipoDomicilioFiscalSerializer, TipoMonedaSerializer, DescuentoSerializer

    )
from .models import (
    INCOTERMS, ActividadEconomica, Departamento, Emisor_fe, EventoContingencia, LoteContingencia, Municipio, OtrosDicumentosAsociado, Pais, Receptor_fe, FacturaElectronica, DetalleFactura,
    Ambiente, CondicionOperacion, Modelofacturacion, NumeroControl,
    Tipo_dte, TipoContingencia, TipoDocContingencia, TipoDomicilioFiscal, TipoDonacion, TipoGeneracionDocumento, TipoMoneda, TipoPersona, TipoRetencionIVAMH, TipoTransmision, TipoTransporte, TipoUnidadMedida, TiposDocIDReceptor, EventoInvalidacion, 
    Receptor_fe, TipoInvalidacion, TiposEstablecimientos, TiposServicio_Medico, Token_data, Descuento, FormasPago, TipoGeneracionDocumento, Plazo
)
from INVENTARIO.models import Producto, TipoItem, TipoTributo, Tributo, UnidadMedida
from django.db.models import Q
from django.core.paginator import Paginator  # esta sigue igual
from django.db.models import Count, Sum


FIRMADOR_URL = "http://192.168.2.25:8113/firmardocumento/"
DJANGO_SERVER_URL = "http://127.0.0.1:8000"

SCHEMA_PATH_fe_fc_v1 = "FE/json_schemas/fe-fc-v1.json"

CERT_PATH = "FE/cert/06142811001040.crt"  # Ruta al certificado

# URLS de Hacienda (Pruebas y Producción)
HACIENDA_URL_TEST = "https://apitest.dtes.mh.gob.sv/fesv/recepciondte"
HACIENDA_URL_PROD = "https://api.dtes.mh.gob.sv/fesv/recepciondte"
#cada endpoint que tenga url quemada agregarlas en una tabla de config, firmador y djangoserver
#BC 04/03/2025: Constantes
COD_CONSUMIDOR_FINAL = "01"
COD_CREDITO_FISCAL = "03"
VERSION_EVENTO_INVALIDACION = 2
AMBIENTE = Ambiente.objects.get(codigo="01")#Hacer dinamico
#AMBIENTE = "01"
COD_FACTURA_EXPORTACION = "11"
COD_TIPO_INVALIDACION_RESCINDIR = 2
COD_NOTA_CREDITO = "05"
COD_NOTA_DEBITO = "06"
COD_COMPROBANTE_LIQUIDACION = "08"
EMI_SOLICITA_INVALIDAR_DTE = "emisor"
REC_SOLICITA_INVALIDAR_DTE = "receptor"
COD_TIPO_ITEM_OTROS = "4"
COD_TRIBUTOS_SECCION_2 = "2"
COD_DOCUMENTO_RELACIONADO_NO_SELEC = "S"
ID_CONDICION_OPERACION = 2
RELACIONAR_DOC_FISICO = 1
RELACIONAR_DOC_ELECTRONICO = 2
COD_TIPO_CONTINGENCIA = "5"
DTE_APLICA_CONTINGENCIA = ["01", "03", "04", "05", "06", "11", "14"]

formas_pago = [] #Asignar formas de pago
documentos_relacionados = []
tipo_dte_doc_relacionar = None
documento_relacionado = False
productos_ids_r = []
cantidades_prod_r = []
descuentos_r = []
tipo_documento_dte = "01"
productos_inventario = None

emisor_fe = Emisor_fe.objects.get(id=1)#Hacer dinamico el id de empresa


######################################################
# AUTENTICACION CON MH
######################################################

class AutenticacionAPIView(APIView):
    # Límite de intentos de autenticación permitidos
    max_attempts = 2

    def post(self, request):
        # Inicializar contador de intentos en la sesión si no existe
        if "auth_attempts" not in request.session:
            request.session["auth_attempts"] = 0
        
        # Verificar si se alcanzó el máximo de intentos permitidos
        if request.session["auth_attempts"] >= self.max_attempts:
            return Response({
                "status": "error",
                "message": "Se alcanzó el límite de intentos de autenticación permitidos",
            }, status=status.HTTP_403_FORBIDDEN)  # Código 403: Forbidden

        user = request.data.get("user")  # Usuario enviado desde el cuerpo de la solicitud
        pwd = request.data.get("pwd")    # Contraseña enviada desde el cuerpo de la solicitud

        # URL de autenticación
        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        
        # Headers para la solicitud
        headers = {
            "User-Agent": "MiAplicacionDjango/1.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Datos para el cuerpo de la solicitud
        data = {
            "user": user,
            "pwd": pwd,
        }

        try:
            # Realizar solicitud POST a la URL de autenticación
            response = requests.post(auth_url, headers=headers, data=data)
            
            # Intentar convertir la respuesta en JSON
            response_data = response.json()

            # Incrementar el contador de intentos de autenticación
            request.session["auth_attempts"] += 1
            request.session.modified = True  # Asegura que los cambios en la sesión se guarden

            # Procesar respuesta en caso de éxito
            if response.status_code == 200 and response_data.get("status") == "OK":
                # Resetear el contador de intentos si autenticación fue exitosa
                request.session["auth_attempts"] = 0
                token = response_data["body"].get("token")
                roles = response_data["body"].get("roles", [])
                token_type = response_data.get("tokenType", "Bearer")

                return Response({
                    "status": "success",
                    "token": f"{token_type} {token}",
                    "roles": roles,
                })

            else:
                return Response({
                    "status": "error",
                    "message": response_data.get("message", "Error en autenticación"),
                    "error": response_data.get("error", "No especificado"),
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            # Error de conexión con el servicio
            return Response({
                "status": "error",
                "message": "Error de conexión con el servicio de autenticación",
                "details": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def autenticacion(request):

    tokens_saves = Token_data.objects.all()

    if request.method == "POST":
        nit_empresa = request.POST.get("user")
        pwd = request.POST.get("pwd")

        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        headers = {"User-Agent": "MiAplicacionDjango/1.0"}
        data = {"user": nit_empresa, "pwd": pwd}

        try:
            response = requests.post(auth_url, headers=headers, data=data)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("status") == "OK":
                    token_body = response_data["body"]
                    token = token_body.get("token")
                    token_type = token_body.get("tokenType", "Bearer")
                    roles = token_body.get("roles", [])

                    # Guardar o actualizar los datos del token en la base de datos
                    token_data, created = Token_data.objects.update_or_create(
                        nit_empresa=nit_empresa,
                        defaults={
                            'password_hacienda': pwd,
                            'token': token,
                            'token_type': token_type,
                            'roles': roles,
                            'activado': True,
                            'fecha_caducidad': timezone.now() + timedelta(days=1)  # Establecer caducidad para 24 horas después
                        }
                    )

                    # Si el token es nuevo, enviamos un mensaje de éxito
                    if created:
                        messages.success(request, "Autenticación exitosa y token guardado.")
                    else:
                        messages.success(request, "Autenticación exitosa y token actualizado.")

                    return redirect('autenticacion')
                else:
                    messages.error(request, "Error en la autenticación: " + response_data.get("message", "Error no especificado"))
            else:
                messages.error(request, "Error en la autenticación.")
        except requests.exceptions.RequestException as e:
            messages.error(request, "Error de conexión con el servicio de autenticación.")

    return render(request, "autenticacion.html", {'tokens':tokens_saves})

######################################################
######################################################
# CATALOGO:
######################################################
######################################################


# ========= ACTIVIDAD ECONOMICA =========
class ActividadEconomicaListAPIView(generics.ListAPIView):

    def get_queryset(self):
        queryset = ActividadEconomica.objects.all()
        filtro = self.request.query_params.get('filtro')

        if filtro:
            queryset = queryset.filter(
                Q(codigo__icontains=filtro) |
                Q(descripcion__icontains=filtro)
            )
        return queryset
    
    serializer_class = ActividadEconomicaSerializer

class ActividadEconomicaCreateAPIView(generics.CreateAPIView):
    queryset = ActividadEconomica.objects.all()
    serializer_class = ActividadEconomicaSerializer

class ActividadEconomicaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ActividadEconomica.objects.all()
    serializer_class = ActividadEconomicaSerializer

class ActividadEconomicaUpdateAPIView(generics.UpdateAPIView):
    queryset = ActividadEconomica.objects.all()
    serializer_class = ActividadEconomicaSerializer

class ActividadEconomicaDestroyAPIView(generics.DestroyAPIView):
    queryset = ActividadEconomica.objects.all()
    serializer_class = ActividadEconomicaSerializer

# ========= AMBIENTE =========
class AmbienteListAPIView(generics.ListAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

class AmbienteCreateAPIView(generics.CreateAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

class AmbienteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

class AmbienteUpdateAPIView(generics.UpdateAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

class AmbienteDestroyAPIView(generics.DestroyAPIView):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

# ========= MODELO FACTURACION =========
class ModelofacturacionListAPIView(generics.ListAPIView):
    queryset = Modelofacturacion.objects.all()
    serializer_class = ModelofacturacionSerializer

class ModelofacturacionCreateAPIView(generics.CreateAPIView):
    queryset = Modelofacturacion.objects.all()
    serializer_class = ModelofacturacionSerializer

class ModelofacturacionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Modelofacturacion.objects.all()
    serializer_class = ModelofacturacionSerializer

class ModelofacturacionUpdateAPIView(generics.UpdateAPIView):
    queryset = Modelofacturacion.objects.all()
    serializer_class = ModelofacturacionSerializer

class ModelofacturacionDestroyAPIView(generics.DestroyAPIView):
    queryset = Modelofacturacion.objects.all()
    serializer_class = ModelofacturacionSerializer

# ========= TIPO TRANSMISION =========
class TipoTransmisionListAPIView(generics.ListAPIView):
    queryset = TipoTransmision.objects.all()
    serializer_class = TipoTransmisionSerializer

class TipoTransmisionCreateAPIView(generics.CreateAPIView):
    queryset = TipoTransmision.objects.all()
    serializer_class = TipoTransmisionSerializer

class TipoTransmisionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoTransmision.objects.all()
    serializer_class = TipoTransmisionSerializer

class TipoTransmisionUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoTransmision.objects.all()
    serializer_class = TipoTransmisionSerializer

class TipoTransmisionDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoTransmision.objects.all()
    serializer_class = TipoTransmisionSerializer

# ========= TIPO CONTINGENCIA =========
class TipoContingenciaListAPIView(generics.ListAPIView):
    queryset = TipoContingencia.objects.all()
    serializer_class = TipoContingenciaSerializer

class TipoContingenciaCreateAPIView(generics.CreateAPIView):
    queryset = TipoContingencia.objects.all()
    serializer_class = TipoContingenciaSerializer

class TipoContingenciaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoContingencia.objects.all()
    serializer_class = TipoContingenciaSerializer

class TipoContingenciaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoContingencia.objects.all()
    serializer_class = TipoContingenciaSerializer

class TipoContingenciaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoContingencia.objects.all()
    serializer_class = TipoContingenciaSerializer

# ========= TIPO RETENCION IVA MH =========
class TipoRetencionIVAMHListAPIView(generics.ListAPIView):
    queryset = TipoRetencionIVAMH.objects.all()
    serializer_class = TipoRetencionIVAMHSerializer

class TipoRetencionIVAMHCreateAPIView(generics.CreateAPIView):
    queryset = TipoRetencionIVAMH.objects.all()
    serializer_class = TipoRetencionIVAMHSerializer

class TipoRetencionIVAMHRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoRetencionIVAMH.objects.all()
    serializer_class = TipoRetencionIVAMHSerializer

class TipoRetencionIVAMHUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoRetencionIVAMH.objects.all()
    serializer_class = TipoRetencionIVAMHSerializer

class TipoRetencionIVAMHDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoRetencionIVAMH.objects.all()
    serializer_class = TipoRetencionIVAMHSerializer

# ========= TIPO GENERACION DOCUMENTO =========
class TipoGeneracionDocumentoListAPIView(generics.ListAPIView):
    queryset = TipoGeneracionDocumento.objects.all()
    serializer_class = TiposGeneracionDocumentoSerializer

class TipoGeneracionDocumentoCreateAPIView(generics.CreateAPIView):
    queryset = TipoGeneracionDocumento.objects.all()
    serializer_class = TiposGeneracionDocumentoSerializer

class TipoGeneracionDocumentoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoGeneracionDocumento.objects.all()
    serializer_class = TiposGeneracionDocumentoSerializer

class TipoGeneracionDocumentoUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoGeneracionDocumento.objects.all()
    serializer_class = TiposGeneracionDocumentoSerializer

class TipoGeneracionDocumentoDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoGeneracionDocumento.objects.all()
    serializer_class = TiposGeneracionDocumentoSerializer

# ========= TIPOS ESTABLECIMIENTOS =========
class TiposEstablecimientosListAPIView(generics.ListAPIView):
    queryset = TiposEstablecimientos.objects.all()
    serializer_class = TiposEstablecimientosSerializer

class TiposEstablecimientosCreateAPIView(generics.CreateAPIView):
    queryset = TiposEstablecimientos.objects.all()
    serializer_class = TiposEstablecimientosSerializer

class TiposEstablecimientosRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TiposEstablecimientos.objects.all()
    serializer_class = TiposEstablecimientosSerializer

class TiposEstablecimientosUpdateAPIView(generics.UpdateAPIView):
    queryset = TiposEstablecimientos.objects.all()
    serializer_class = TiposEstablecimientosSerializer

class TiposEstablecimientosDestroyAPIView(generics.DestroyAPIView):
    queryset = TiposEstablecimientos.objects.all()
    serializer_class = TiposEstablecimientosSerializer

# ========= TIPOS SERVICIO MEDICO =========
class TiposServicio_MedicoListAPIView(generics.ListAPIView):
    queryset = TiposServicio_Medico.objects.all()
    serializer_class = TiposServicio_MedicoSerializer

class TiposServicio_MedicoCreateAPIView(generics.CreateAPIView):
    queryset = TiposServicio_Medico.objects.all()
    serializer_class = TiposServicio_MedicoSerializer

class TiposServicio_MedicoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TiposServicio_Medico.objects.all()
    serializer_class = TiposServicio_MedicoSerializer

class TiposServicio_MedicoUpdateAPIView(generics.UpdateAPIView):
    queryset = TiposServicio_Medico.objects.all()
    serializer_class = TiposServicio_MedicoSerializer

class TiposServicio_MedicoDestroyAPIView(generics.DestroyAPIView):
    queryset = TiposServicio_Medico.objects.all()
    serializer_class = TiposServicio_MedicoSerializer

# ========= TIPO_DTE =========
class Tipo_dteListAPIView(generics.ListAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteCreateAPIView(generics.CreateAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteUpdateAPIView(generics.UpdateAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteDestroyAPIView(generics.DestroyAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

# ========= OTROS DOCUMENTOS ASOCIADO =========
class OtrosDicumentosAsociadoListAPIView(generics.ListAPIView):
    queryset = OtrosDicumentosAsociado.objects.all()
    serializer_class = OtrosDicumentosAsociadoSerializer

class OtrosDicumentosAsociadoCreateAPIView(generics.CreateAPIView):
    queryset = OtrosDicumentosAsociado.objects.all()
    serializer_class = OtrosDicumentosAsociadoSerializer

class OtrosDicumentosAsociadoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = OtrosDicumentosAsociado.objects.all()
    serializer_class = OtrosDicumentosAsociadoSerializer

class OtrosDicumentosAsociadoUpdateAPIView(generics.UpdateAPIView):
    queryset = OtrosDicumentosAsociado.objects.all()
    serializer_class = OtrosDicumentosAsociadoSerializer

class OtrosDicumentosAsociadoDestroyAPIView(generics.DestroyAPIView):
    queryset = OtrosDicumentosAsociado.objects.all()
    serializer_class = OtrosDicumentosAsociadoSerializer

# ========= TIPOS DOC ID RECEPTOR =========
class TiposDocIDReceptorListAPIView(generics.ListAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorCreateAPIView(generics.CreateAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorUpdateAPIView(generics.UpdateAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorDestroyAPIView(generics.DestroyAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

# ========= PAIS =========
class PaisListAPIView(generics.ListAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisCreateAPIView(generics.CreateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisUpdateAPIView(generics.UpdateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisDestroyAPIView(generics.DestroyAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

# ========= DEPARTAMENTO =========
class DepartamentoListAPIView(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class DepartamentoCreateAPIView(generics.CreateAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class DepartamentoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class DepartamentoUpdateAPIView(generics.UpdateAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class DepartamentoDestroyAPIView(generics.DestroyAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

# ========= MUNICIPIO =========
class MunicipioListAPIView(generics.ListAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class MunicipioCreateAPIView(generics.CreateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class MunicipioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class MunicipioUpdateAPIView(generics.UpdateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class MunicipioDestroyAPIView(generics.DestroyAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class MunicipioByDepartamentoAPIView(generics.ListAPIView):
    serializer_class = MunicipioSerializer

    def get_queryset(self):
        # Obtener el departamento a partir del id que pasamos en la URL
        departamento_id = self.kwargs['departamento_id']
        # Filtramos los municipios que pertenecen a ese departamento
        return Municipio.objects.filter(departamento__id=departamento_id)
    
# ========= CONDICION OPERACION =========
class CondicionOperacionListAPIView(generics.ListAPIView):
    queryset = CondicionOperacion.objects.all()
    serializer_class = CondicionOperacionSerializer

class CondicionOperacionCreateAPIView(generics.CreateAPIView):
    queryset = CondicionOperacion.objects.all()
    serializer_class = CondicionOperacionSerializer

class CondicionOperacionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CondicionOperacion.objects.all()
    serializer_class = CondicionOperacionSerializer

class CondicionOperacionUpdateAPIView(generics.UpdateAPIView):
    queryset = CondicionOperacion.objects.all()
    serializer_class = CondicionOperacionSerializer

class CondicionOperacionDestroyAPIView(generics.DestroyAPIView):
    queryset = CondicionOperacion.objects.all()
    serializer_class = CondicionOperacionSerializer

# ========= FORMAS PAGO =========
class FormasPagoListAPIView(generics.ListAPIView):
    queryset = FormasPago.objects.all()
    serializer_class = FormasPagosSerializer

class FormasPagoCreateAPIView(generics.CreateAPIView):
    queryset = FormasPago.objects.all()
    serializer_class = FormasPagosSerializer

class FormasPagoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = FormasPago.objects.all()
    serializer_class = FormasPagosSerializer

class FormasPagoUpdateAPIView(generics.UpdateAPIView):
    queryset = FormasPago.objects.all()
    serializer_class = FormasPagosSerializer

class FormasPagoDestroyAPIView(generics.DestroyAPIView):
    queryset = FormasPago.objects.all()
    serializer_class = FormasPagosSerializer

# ========= PLAZO =========
class PlazoListAPIView(generics.ListAPIView):
    queryset = Plazo.objects.all()
    serializer_class = PlazoSerializer

class PlazoCreateAPIView(generics.CreateAPIView):
    queryset = Plazo.objects.all()
    serializer_class = PlazoSerializer

class PlazoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Plazo.objects.all()
    serializer_class = PlazoSerializer

class PlazoUpdateAPIView(generics.UpdateAPIView):
    queryset = Plazo.objects.all()
    serializer_class = PlazoSerializer

class PlazoDestroyAPIView(generics.DestroyAPIView):
    queryset = Plazo.objects.all()
    serializer_class = PlazoSerializer

# ========= TIPO DOC CONTINGENCIA =========
class TipoDocContingenciaListAPIView(generics.ListAPIView):
    queryset = TipoDocContingencia.objects.all()
    serializer_class = TipoDocContingenciaSerializer

class TipoDocContingenciaCreateAPIView(generics.CreateAPIView):
    queryset = TipoDocContingencia.objects.all()
    serializer_class = TipoDocContingenciaSerializer

class TipoDocContingenciaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoDocContingencia.objects.all()
    serializer_class = TipoDocContingenciaSerializer

class TipoDocContingenciaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoDocContingencia.objects.all()
    serializer_class = TipoDocContingenciaSerializer

class TipoDocContingenciaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoDocContingencia.objects.all()
    serializer_class = TipoDocContingenciaSerializer

# ========= TIPO INVALIDACION =========
class TipoInvalidacionListAPIView(generics.ListAPIView):
    queryset = TipoInvalidacion.objects.all()
    serializer_class = TipoInvalidacionSerializer

class TipoInvalidacionCreateAPIView(generics.CreateAPIView):
    queryset = TipoInvalidacion.objects.all()
    serializer_class = TipoInvalidacionSerializer

class TipoInvalidacionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoInvalidacion.objects.all()
    serializer_class = TipoInvalidacionSerializer

class TipoInvalidacionUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoInvalidacion.objects.all()
    serializer_class = TipoInvalidacionSerializer

class TipoInvalidacionDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoInvalidacion.objects.all()
    serializer_class = TipoInvalidacionSerializer

# ========= TIPO DONACION =========
class TipoDonacionListAPIView(generics.ListAPIView):
    queryset = TipoDonacion.objects.all()
    serializer_class = TipoDonacionSerializer

class TipoDonacionCreateAPIView(generics.CreateAPIView):
    queryset = TipoDonacion.objects.all()
    serializer_class = TipoDonacionSerializer

class TipoDonacionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoDonacion.objects.all()
    serializer_class = TipoDonacionSerializer

class TipoDonacionUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoDonacion.objects.all()
    serializer_class = TipoDonacionSerializer

class TipoDonacionDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoDonacion.objects.all()
    serializer_class = TipoDonacionSerializer

# ========= TIPO PERSONA =========
class TipoPersonaListAPIView(generics.ListAPIView):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializer

class TipoPersonaCreateAPIView(generics.CreateAPIView):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializer

class TipoPersonaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializer

class TipoPersonaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializer

class TipoPersonaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializer

# ========= TIPO TRANSPORTE =========
class TipoTransporteListAPIView(generics.ListAPIView):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

class TipoTransporteCreateAPIView(generics.CreateAPIView):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

class TipoTransporteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

class TipoTransporteUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

class TipoTransporteDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

# ========= INCOTERMS =========
class INCOTERMSListAPIView(generics.ListAPIView):
    queryset = INCOTERMS.objects.all()
    serializer_class = INCOTERMS_Serializer

class INCOTERMSCreateAPIView(generics.CreateAPIView):
    queryset = INCOTERMS.objects.all()
    serializer_class = INCOTERMS_Serializer

class INCOTERMSRetrieveAPIView(generics.RetrieveAPIView):
    queryset = INCOTERMS.objects.all()
    serializer_class = INCOTERMS_Serializer

class INCOTERMSUpdateAPIView(generics.UpdateAPIView):
    queryset = INCOTERMS.objects.all()
    serializer_class = INCOTERMS_Serializer

class INCOTERMSDestroyAPIView(generics.DestroyAPIView):
    queryset = INCOTERMS.objects.all()
    serializer_class = INCOTERMS_Serializer

# ========= TIPO DOMICILIO FISCAL =========
class TipoDomicilioFiscalListAPIView(generics.ListAPIView):
    queryset = TipoDomicilioFiscal.objects.all()
    serializer_class = TipoDomicilioFiscalSerializer

class TipoDomicilioFiscalCreateAPIView(generics.CreateAPIView):
    queryset = TipoDomicilioFiscal.objects.all()
    serializer_class = TipoDomicilioFiscalSerializer

class TipoDomicilioFiscalRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoDomicilioFiscal.objects.all()
    serializer_class = TipoDomicilioFiscalSerializer

class TipoDomicilioFiscalUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoDomicilioFiscal.objects.all()
    serializer_class = TipoDomicilioFiscalSerializer

class TipoDomicilioFiscalDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoDomicilioFiscal.objects.all()
    serializer_class = TipoDomicilioFiscalSerializer

# ========= TIPO MONEDA =========
class TipoMonedaListAPIView(generics.ListAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

class TipoMonedaCreateAPIView(generics.CreateAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

class TipoMonedaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

class TipoMonedaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

class TipoMonedaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

# ========= DESCUENTO =========
class DescuentoListAPIView(generics.ListAPIView):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer

class DescuentoCreateAPIView(generics.CreateAPIView):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer

class DescuentoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer

class DescuentoUpdateAPIView(generics.UpdateAPIView):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer

class DescuentoDestroyAPIView(generics.DestroyAPIView):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer


######################################################
######################################################
# FIN CATALOGO
######################################################
######################################################



######################################################
# RECEPTOR O CLIENTE
######################################################

class ObtenerReceptorAPIView(APIView):
    """
    Devuelve los datos de un receptor en formato JSON.
    """
    def get(self, request, receptor_id):
        try:
            receptor = Receptor_fe.objects.get(id=receptor_id)
            # Si tienes un serializer para Receptor_fe, úsalo:
            serializer = ReceptorSerializer(receptor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Receptor_fe.DoesNotExist:
            return Response({"error": "Receptor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class receptorListAPIView(generics.ListAPIView):
    serializer_class = ReceptorSerializer

    def get_queryset(self):
        qs = Receptor_fe.objects.all()
        nombre = self.request.query_params.get('filtro') #filtrar receptores por nombre, nombre comercial y número de documento
        if nombre:
            qs = qs.filter(
                Q(nombre__icontains=nombre) |
                Q(nombreComercial__icontains=nombre) |
                Q(num_documento__icontains=nombre)
            )
        return qs

class receptorDetailAPIView(generics.RetrieveAPIView):
    queryset = Receptor_fe.objects.all()
    serializer_class = ReceptorSerializer

class receptorCreateAPIView(generics.CreateAPIView):
    serializer_class = ReceptorSerializer
    
class receptorUpdateAPIView(generics.UpdateAPIView):
    queryset = Receptor_fe.objects.all()
    serializer_class = ReceptorSerializer

class receptorDeleteAPIView(generics.DestroyAPIView):
    queryset = Receptor_fe.objects.all()
    serializer_class = ReceptorSerializer

######################################################
# EMISOR O EMPRESA
######################################################
class EmisorListAPIView(generics.ListAPIView):
    queryset = Emisor_fe.objects.all()
    serializer_class = EmisorSerializer

class EmisorUpdateAPIView(generics.UpdateAPIView):
    queryset = Emisor_fe.objects.all()
    serializer_class = EmisorSerializer

class EmisorCreateAPIView(generics.CreateAPIView):
    queryset = Emisor_fe.objects.all()
    serializer_class = EmisorSerializer     
     
######################################################
# GENERACION DE DOCUMENTOS ELECTRONICOS
######################################################
    
class FacturaDetailAPIView(generics.RetrieveAPIView):
    queryset = FacturaElectronica.objects.all()
    serializer_class = FacturaElectronicaSerializer

class FacturaListAPIView(APIView):
    """
    Vista API que devuelve un listado de FacturaElectronica con filtros y paginación.
    Parámetros GET:
      - recibido_mh: 'True' o 'False'
      - sello_recepcion: (filtro por coincidencia, icontains)
      - has_sello_recepcion: 'yes' para facturas con sello, 'no' para aquellas sin sello
      - tipo_dte: id del tipo de DTE
      - page: número de página (paginación de 20 registros)
      
    Además se incluye la lista de tipos de DTE.
    """
    def get(self, request):
        # Obtener el queryset base
        queryset = FacturaElectronica.objects.all()
        
        # Aplicar filtros según los parámetros GET
        recibido = request.GET.get('recibido_mh')
        codigo = request.GET.get('sello_recepcion')
        has_codigo = request.GET.get('has_sello_recepcion')
        tipo = request.GET.get('tipo_dte')
        
        if recibido in ['True', 'False']:
            queryset = queryset.filter(recibido_mh=(recibido == 'True'))
        if codigo:
            queryset = queryset.filter(sello_recepcion__icontains=codigo)
        if has_codigo == 'yes':
            queryset = queryset.exclude(sello_recepcion__isnull=True)
        elif has_codigo == 'no':
            queryset = queryset.filter(sello_recepcion__isnull=True)
        if tipo:
            queryset = queryset.filter(tipo_dte__id=tipo)
        
        # Configurar la paginación: 20 registros por página
        paginator = paginator(queryset, 20)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        # Serializar los datos
        serializer = FacturaElectronicaSerializer(page_obj, many=True)
        
        # Serializar los tipos de DTE para el filtro
        tipos_dte = Tipo_dte.objects.all()
        tipos_dte_data = [{"id": t.id, "codigo": t.codigo, "descripcion": t.descripcion} for t in tipos_dte]
        
        data = {
            "facturas": serializer.data,
            "pagination": {
                "page": page_obj.number,
                "pages": paginator.num_pages,
                "total": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            },
            "tipos_dte": tipos_dte_data
        }
        
        return Response(data, status=status.HTTP_200_OK)

class GenerarFacturaAPIView(APIView):
    """
    Vista API para generar facturas.
    En GET se retornan los datos para armar el formulario (en vez de renderizar una plantilla)  
    y en POST se procesa la generación de la factura.
    """

    def get(self, request, format=None):
        # Inicializamos las variables globales (aunque es recomendable evitar globals)
        global productos_ids_r, cantidades_prod_r, documentos_relacionados, descuentos_r
        productos_ids_r = []
        cantidades_prod_r = []
        documentos_relacionados = []
        descuentos_r = []
        
        global tipo_documento_dte
        tipo_dte = tipo_documento_dte

        emisor_obj = Emisor_fe.objects.first()
        if emisor_obj:
            nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
        else:
            nuevo_numero = ""
        codigo_generacion = str(uuid.uuid4()).upper()
        fecha_generacion = timezone.now().date()
        hora_generacion = timezone.now().strftime('%H:%M:%S')

        emisor_data = {
            "nit": emisor_obj.nit if emisor_obj else "",
            "nombre_razon_social": emisor_obj.nombre_razon_social if emisor_obj else "",
            "direccion_comercial": emisor_obj.direccion_comercial if emisor_obj else "",
            "telefono": emisor_obj.telefono if emisor_obj else "",
            "email": emisor_obj.email if emisor_obj else "",
        } if emisor_obj else None

        receptores = list(Receptor_fe.objects.values("id", "num_documento", "nombre"))
        # Se asume que esta función retorna un listado adecuado
        productos = obtener_listado_productos_view(request)
        tipooperaciones = list(CondicionOperacion.objects.all().values())
        tipoDocumentos = list(
            Tipo_dte.objects.exclude(Q(codigo=COD_NOTA_CREDITO) | Q(codigo=COD_NOTA_DEBITO)).values()
        )
        tipoItems = list(TipoItem.objects.all().values())
        descuentos = list(Descuento.objects.all().values())
        formasPago = list(FormasPago.objects.all().values())
        tipoGeneracionDocumentos = list(TipoGeneracionDocumento.objects.all().values())

        context = {
            "numero_control": nuevo_numero,
            "codigo_generacion": codigo_generacion,
            "fecha_generacion": fecha_generacion,
            "hora_generacion": hora_generacion,
            "emisor": emisor_data,
            "receptores": receptores,
            "productos": productos,
            "tipooperaciones": tipooperaciones,
            "tipoDocumentos": tipoDocumentos,
            "tipoItems": tipoItems,
            "descuentos": descuentos,
            "formasPago": formasPago,
            "tipoGenDocumentos": tipoGeneracionDocumentos
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            items_permitidos = 2000
            data = request.data  # DRF se encarga de parsear el JSON

            docsRelacionados = []  # Acumular documentos relacionados
            contingencia = False

            # Datos básicos
            numero_control = data.get('numero_control', '')
            codigo_generacion = data.get('codigo_generacion', '')
            receptor_id = data.get('receptor_id', None)
            
            nit_receptor = data.get('nit_receptor', '')
            nombre_receptor = data.get('nombre_receptor', '')
            direccion_receptor = data.get('direccion_receptor', '')
            telefono_receptor = data.get('telefono_receptor', '')
            correo_receptor = data.get('correo_receptor', '')
            observaciones = data.get('observaciones', '')
            tipo_dte = data.get("tipo_documento_seleccionado", None)
            tipo_item = data.get("tipo_item_select", None)
            
            tipo_doc_relacionar = data.get("documento_seleccionado", None)
            documento_relacionado = data.get("documento_relacionado", [])
            
            # Configuración adicional
            tipooperacion_id = data.get("condicion_operacion", 1)
            porcentaje_retencion_iva = Decimal(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = data.get("retencion_iva", False)
            productos_retencion_iva = data.get("productos_retencion_iva", [])
            porcentaje_retencion_renta = Decimal(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = data.get("retencion_renta", False)
            formas_pago_id = data.get('formas_pago_id', [])
            
            descuento_global = data.get("descuento_global_input", "0")
            saldo_favor = data.get("saldo_favor_input", "0")
            base_imponible_checkbox = data.get("no_gravado", False)
            
            descu_gravado = data.get("descuento_gravado", "0")
            monto_descuento = data.get("monto_descuento", "0")
            
            if saldo_favor is not None and saldo_favor != "":
                saldo_f = Decimal(saldo_favor)
                if saldo_f > Decimal("0.00"):
                    saldo_favor = saldo_f * Decimal("-1")
                else:
                    saldo_favor = Decimal("0.00")
            else:
                saldo_favor = Decimal("0.00")

            # Datos de productos
            productos_ids = data.get('productos_ids', [])
            cantidades = data.get('cantidades', [])
            descuentos_aplicados = data.get("descuento_select", [])
            
            nombre_responsable = data.get("nombre_responsable", None)
            documento_responsable = data.get("documento_responsable", None)
            
            if numero_control:
                numero_control = NumeroControl.obtener_numero_control(tipo_dte)
            if not codigo_generacion:
                codigo_generacion = str(uuid.uuid4()).upper()

            # Emisor
            emisor_obj = Emisor_fe.objects.first()
            if not emisor_obj:
                return Response({"error": "No hay emisores registrados en la base de datos"}, status=status.HTTP_400_BAD_REQUEST)
            emisor = emisor_obj

            # Receptor
            if receptor_id and receptor_id != "nuevo":
                receptor = Receptor_fe.objects.get(id=receptor_id)
            else:
                tipo_doc, _ = TiposDocIDReceptor.objects.get_or_create(
                    codigo='13', defaults={"descripcion": "DUI/NIT"}
                )
                receptor, _ = Receptor_fe.objects.update_or_create(
                    num_documento=nit_receptor,
                    defaults={
                        'nombre': nombre_receptor,
                        'tipo_documento': tipo_doc,
                        'direccion': direccion_receptor,
                        'telefono': telefono_receptor,
                        'correo': correo_receptor
                    }
                )

            ambiente_obj = Ambiente.objects.get(codigo="01")
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            tipo_item_obj = TipoItem.objects.get(codigo=tipo_item)

            tipomodelo_obj = Modelofacturacion.objects.get(codigo="1")
            tipooperacion_obj = CondicionOperacion.objects.get(id=tipooperacion_id) if tipooperacion_id else None
            tipo_moneda_obj = TipoMoneda.objects.get(codigo="USD")

            factura = FacturaElectronica.objects.create(
                version="1.0",
                tipo_dte=tipo_dte_obj,
                numero_control=numero_control,
                codigo_generacion=codigo_generacion,
                tipomodelo=tipomodelo_obj,
                tipocontingencia=None,
                motivocontin=None,
                tipomoneda=tipo_moneda_obj,
                dteemisor=emisor,
                dtereceptor=receptor,
                json_original={},
                firmado=False,
                base_imponible=base_imponible_checkbox
            )

            # Inicialización de acumuladores
            total_gravada = Decimal("0.00")
            total_iva = Decimal("0.00")
            total_pagar = Decimal("0.00")
            DecimalRetIva = Decimal("0.00")
            DecimalRetRenta = Decimal("0.00")
            DecimalIvaPerci = Decimal("0.00")
            total_operaciones = Decimal("0.00")
            descuento_item = Decimal("0.00")
            total_no_gravado = Decimal("0.00")
            sub_total = Decimal("0.00")
            porc_descuento_global = Decimal("0.00")
            total_iva_item = Decimal("0.00")
            precio_inc_neto = Decimal("0.00")
            descuento_gravado = Decimal("0.00")
            neto_unitario = Decimal("0.00")
            sub_total_item = Decimal("0")
            
            tributo_valor = None

            for index, prod_id in enumerate(productos_ids):
                try:
                    producto = Producto.objects.get(id=prod_id)
                except Producto.DoesNotExist:
                    continue

                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo="99")
                else:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo=producto.unidad_medida.codigo)

                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    cantidad = 1
                else:
                    cantidad = int(cantidades[index]) if index < len(cantidades) else 1
                    
                porcentaje_descuento_producto = descuentos_aplicados[index] if index < len(descuentos_aplicados) else 1
                precio_incl = producto.preunitario

                if (base_imponible_checkbox is False and tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS) or tipo_dte_obj.codigo != COD_CONSUMIDOR_FINAL:
                    tributoIva = Tributo.objects.get(codigo="20")
                    tributo_valor = tributoIva.valor_tributo
                    tributos = [str(tributoIva.codigo)]
                else:
                    tributos = None
                
                if tributo_valor is None:
                    tributo_valor = Decimal("0.00")
                
                if base_imponible_checkbox is True:
                    precio_neto = Decimal("0.00")
                elif base_imponible_checkbox is False and tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
                    if producto.precio_iva:
                        neto_unitario = precio_incl.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = neto_unitario
                    else:
                        neto_unitario = (precio_incl * Decimal("1.13")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = (precio_incl * Decimal("1.13")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    precio_neto = (neto_unitario * cantidad).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                else:
                    if producto.precio_iva:
                        neto_unitario = (precio_incl / Decimal("1.13")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = neto_unitario
                    else:
                        neto_unitario = precio_incl.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = neto_unitario
                    precio_neto = (neto_unitario * cantidad).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    precio_neto = (precio_neto * Decimal(tributo_valor)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    
                precio_neto = Decimal(precio_neto)          
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                if porcentaje_descuento_producto:
                    porcentaje_descuento_item = Descuento.objects.get(porcentaje=(porcentaje_descuento_producto * 100))
                else:
                    porcentaje_descuento_item = Descuento.objects.first()
                    
                descuento_porcentaje = (porcentaje_descuento_item.porcentaje / 100).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                descuento_aplicado = True if porcentaje_descuento_item.porcentaje > Decimal("0.00") else False
                
                if monto_descuento:
                    monto_descuento = Decimal(monto_descuento).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    monto_descuento = Decimal("0.00")
                if not descu_gravado:
                    descu_gravado = Decimal("0.00")
                
                descuento_item = (precio_neto * descuento_porcentaje).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_neto = (precio_neto - descuento_item).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
                    total_iva_item = ( total_neto / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                else:
                    total_iva_item = ( total_neto * Decimal("0.13") ).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                cuerpo_documento_tributos = []
                if producto.tributo is None:
                    return Response({"error": "Seleccionar tributo para el producto"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                        tributo = Tributo.objects.get(codigo=producto.tributo.codigo)
                        precio_neto = (precio_neto * Decimal(tributo.valor_tributo)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    
                detalle = DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    unidad_medida=unidad_medida_obj,
                    precio_unitario=precio_inc_neto,
                    descuento=porcentaje_descuento_item,
                    tiene_descuento=descuento_aplicado,
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=total_neto,
                    pre_sug_venta=precio_inc_neto,
                    no_gravado=Decimal("0.00"),
                    saldo_favor=saldo_favor
                )
                
                total_gravada += total_neto
                
                if descu_gravado:
                    descuento_gravado = (total_gravada * Decimal(descu_gravado) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                if descuento_global:
                    porc_descuento_global = (total_gravada * Decimal(descuento_global) / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                sub_total_item = (total_gravada - descuento_gravado - porc_descuento_global).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                sub_total = sub_total_item
                
                if tributo_valor is not None:
                    valorTributo = ( total_gravada * Decimal(tributo_valor) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_operaciones = (sub_total + valorTributo).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    total_operaciones = sub_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
                    total_con_iva = (total_operaciones - DecimalRetIva - DecimalRetRenta - total_no_gravado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    total_con_iva = (total_operaciones - DecimalIvaPerci - DecimalRetIva - DecimalRetRenta - total_no_gravado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    
                total_iva = total_iva_item.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_pagar = total_con_iva
                
                detalle.total_sin_descuento = total_neto.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.iva = total_iva_item.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.total_con_iva = total_con_iva.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.iva_item = total_iva_item.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.save()
                
            if retencion_iva and porcentaje_retencion_iva > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_iva:
                        DecimalRetIva += (detalle.total_sin_descuento * porcentaje_retencion_iva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if retencion_renta and porcentaje_retencion_renta > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_renta:
                        DecimalRetRenta += (detalle.total_sin_descuento * porcentaje_retencion_renta / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            total_iva = total_iva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_pagar = total_pagar.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            if tipo_doc_relacionar is COD_DOCUMENTO_RELACIONADO_NO_SELEC:
                tipo_doc_relacionar = None
                documento_relacionado = None
                
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = total_gravada.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.sub_total_ventas = total_gravada.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = float(descuento_gravado)
            factura.por_descuento = porc_descuento_global
            factura.total_descuento = float(monto_descuento)
            factura.sub_total = sub_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.iva_retenido = float(DecimalRetIva)
            factura.retencion_renta = float(DecimalRetRenta)
            factura.total_operaciones = float(total_operaciones)
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = float(total_pagar)
            factura.total_letras = num_to_letras(total_pagar)
            factura.total_iva = float(total_iva)
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = float(DecimalIvaPerci)
            factura.tipo_documento_relacionar = tipo_doc_relacionar
            factura.documento_relacionado = documento_relacionado
            factura.save()
            
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                if idx > items_permitidos:
                    return Response({"error": "Cantidad máxima de ítems permitidos"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    codTributo = None 
                    cuerpo_documento_tributos = []
                    if det.producto.tributo is None:
                        return Response({"error": "Seleccionar tributo para el producto"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                            codTributo = tributo.codigo
                            if det.producto.tributo.tipo_tributo.codigo == COD_TRIBUTOS_SECCION_2:
                                cuerpo_documento_tributos.append({
                                    "numItem": idx+1,
                                    "tipoItem": int(tipo_item_obj.codigo),
                                    "numeroDocumento": None,
                                    "codigo": str(det.producto.codigo),
                                    "codTributo": codTributo,
                                    "descripcion": str(tributo.descripcion),
                                    "cantidad": float(det.cantidad),
                                    "uniMedida": int(det.unidad_medida.codigo),
                                    "precioUni": float(det.precio_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                                    "montoDescu": float(((det.precio_unitario * det.cantidad) * (Decimal(det.descuento.porcentaje) / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                                    "ventaNoSuj": 0.0,
                                    "ventaExenta": 0.0,
                                    "ventaGravada": float(det.ventas_gravadas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                                    "tributos": tributos,
                                    "psv": float(det.precio_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                                    "noGravado": 0.0
                                })
                    
                    # Se arma cada item del cuerpo del documento
                    cuerpo_documento.append({
                        "numItem": idx,
                        "tipoItem": int(tipo_item_obj.codigo),
                        "numeroDocumento": None,
                        "codigo": str(det.producto.codigo),
                        "codTributo": codTributo,
                        "descripcion": str(det.producto.descripcion),
                        "cantidad": float(det.cantidad),
                        "uniMedida": int(det.unidad_medida.codigo),
                        "precioUni": float(det.precio_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "montoDescu": float(((det.precio_unitario * det.cantidad) * (Decimal(det.descuento.porcentaje) / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "ventaNoSuj": float(det.ventas_no_sujetas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "ventaExenta": float(det.ventas_exentas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "ventaGravada": float(det.ventas_gravadas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "tributos": tributos,
                        "psv": float(det.pre_sug_venta.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                        "noGravado": float(det.no_gravado.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
                    })
                    
                    if cuerpo_documento_tributos is None:
                        cuerpo_documento.append(cuerpo_documento_tributos)
            
            factura_json = generar_json(
                ambiente_obj, tipo_dte_obj, factura, emisor, receptor,
                cuerpo_documento, observaciones, Decimal(str(total_iva_item)),
                base_imponible_checkbox, saldo_favor, documentos_relacionados, contingencia, 
                total_gravada, nombre_responsable, documento_responsable
            )
            
            factura.json_original = factura_json
            if formas_pago_id:
                factura.formas_Pago = formas_pago_id
            factura.save()

            json_path = os.path.join("FE/json_facturas", f"{factura.numero_control}.json")
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(factura_json, f, indent=4, ensure_ascii=False)

            return Response({
                    "mensaje": "Factura generada correctamente",
                    "factura_id": factura.id,
                    "numero_control": factura.numero_control,
                    "redirect": reverse('detalle_factura', args=[factura.id])
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
######################################################
# GENERACION DE NOTA DE CREDITO Y DEBITO API
######################################################
class GenerarDocumentoAjusteAPIView(APIView):
    cod_generacion = str(uuid.uuid4()).upper()
    def get(self, request, format=None):
        print("GET Inicio generar dte")
        if request.method == 'GET':
            tipo_dte = request.query_params.get('tipo_dte', '05')
            emisor_obj = Emisor_fe.objects.first()
            
            if emisor_obj:
                nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
            else:
                nuevo_numero = ""
            codigo_generacion = self.cod_generacion
            fecha_generacion = timezone.now().date()
            hora_generacion = timezone.now().strftime('%H:%M:%S')

            emisor_data = {
                "nit": emisor_obj.nit if emisor_obj else "",
                "nombre_razon_social": emisor_obj.nombre_razon_social if emisor_obj else "",
                "direccion_comercial": emisor_obj.direccion_comercial if emisor_obj else "",
                "telefono": emisor_obj.telefono if emisor_obj else "",
                "email": emisor_obj.email if emisor_obj else "",
            } if emisor_obj else None

            receptores = list(Receptor_fe.objects.values("id", "num_documento", "nombre"))
            productos = list(Producto.objects.all().values())
            tipooperaciones = list(CondicionOperacion.objects.all().values())
            tipoDocumentos = list(Tipo_dte.objects.filter( Q(codigo=COD_NOTA_CREDITO) | Q(codigo=COD_NOTA_DEBITO)).values())
            tipoItems = list(TipoItem.objects.all().values())
            descuentos = list(Descuento.objects.all().values())
            formasPago = list(FormasPago.objects.all().values())
            tipoGeneracionDocumentos = list(TipoGeneracionDocumento.objects.all().values())

            context = {
                "numero_control": nuevo_numero,
                "codigo_generacion": codigo_generacion,
                "fecha_generacion": fecha_generacion,
                "hora_generacion": hora_generacion,
                "emisor": emisor_data,
                "receptores": receptores,
                "productos": productos,
                "tipooperaciones": tipooperaciones,
                "tipoDocumentos": tipoDocumentos,
                "tipoItems": tipoItems,
                "descuentos": descuentos,
                "formasPago": formasPago,
                "tipoGenDocumentos": tipoGeneracionDocumentos
            }
            return Response(context, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        print("POST Inicio generar dte")
        tipo_dte = request.query_params.get('tipo_dte', '05')
        nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
        global formas_pago
        documentos_relacionados = []
        try:
            items_permitidos = 2000
            docsRelacionados = []#Acumular los documentos relacionados
            data = request.data
            contingencia = False
            
            # Datos básicos
            numero_control = nuevo_numero
            #codigo_generacion = self.cod_generacion
            codigo_generacion = str(uuid.uuid4()).upper()
            print(f"Numero de control: {numero_control} Codigo generacion: {codigo_generacion}")
            
            #Datos del receptor
            print("-Inicio datos receptor")
            receptor_id = data.get('receptor_id', None)
            receptor_fe = Receptor_fe.objects.get(id=receptor_id)
            nit_receptor = receptor_fe.num_documento
            nombre_receptor = receptor_fe.nombre
            direccion_receptor = receptor_fe.direccion
            telefono_receptor = receptor_fe.telefono
            correo_receptor = receptor_fe.correo
            print("-Fin datos receptor")
            
            observaciones = data.get('observaciones', '')
            tipo_dte = data.get("tipo_documento_seleccionado", None) #BC: obtiene la seleccion del tipo de documento desde la pantalla del sistema
            tipo_item = data.get("tipo_item_select", None)
            tipo_doc_relacionar = data.get("documento_seleccionado", []) #tipo documento relacionado(FISICO - ELECTRONICO)
            documento_relacionado = data.get("documento_relacionado", []) #Numero de documento relacionado
            #obtener_factura_por_codigo_api(request)
            if documento_relacionado is None or documento_relacionado == []:
                documento_relacionado = None
            else:
                documento_relacionado = documento_relacionado.upper()
            porcentaje_descuento = data.get("descuento_select", "0")
            if porcentaje_descuento:
                porcentaje_descuento_producto = porcentaje_descuento.replace(",", ".")
            print("-Descuento: ", porcentaje_descuento_producto)
                
            # Configuración adicional
            tipooperacion_id = data.get("condicion_operacion", 1)
            porcentaje_retencion_iva = Decimal(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = data.get("retencion_iva", False)
            productos_retencion_iva = data.get("productos_retencion_iva", [])
            porcentaje_retencion_renta = Decimal(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = data.get("retencion_renta", False)
            productos_retencion_renta = data.get("productos_retencion_renta", [])
            
            descuento_global = data.get("descuento_global_input", "0")
            
            saldo_favor = data.get("saldo_favor_input", "0")
            base_imponible_checkbox = data.get("no_gravado", False)
            
            #Descuento gravado
            descu_gravado = data.get("descuento_gravado", "0")
            #Total descuento = descuento por item + descuento global gravado
            monto_descuento = data.get("monto_descuento", "0")
            print(f"descuento global = {descuento_global}, monto descuento = {descu_gravado}")
            
            if saldo_favor is not None and saldo_favor !="":
                saldo_f = Decimal(saldo_favor)
                if saldo_f > Decimal("0.00"):
                    saldo_favor = saldo_f * Decimal("-1")
                else:
                    saldo_favor = Decimal("0.00")
            else:
                saldo_favor = Decimal("0.00")

            # Datos de productos
            productos_ids = data.get('productos_ids', [])
            cantidades = data.get('cantidades', [])
            print(f"productos.: = {productos_ids}, cantidades.: = {cantidades}")
            
            if productos_ids_r is not None and len(productos_ids_r)>0:
                for id in productos_ids_r:
                    productos_ids.append(id)
                
            if cantidades_prod_r is not None and len(cantidades_prod_r)>0:
                for c in cantidades_prod_r:
                    cantidades.append(c)
            
            print(f"id productos: {productos_ids}, cantidades: {cantidades}")
            # En este caso, se asume que el descuento por producto es 0 (se aplica globalmente)
            
            if numero_control:
                numero_control = NumeroControl.obtener_numero_control(tipo_dte)
                print(numero_control)
            if not codigo_generacion:
                codigo_generacion = str(uuid.uuid4()).upper()

            # Obtener emisor
            emisor_obj = Emisor_fe.objects.first()
            if not emisor_obj:
                return Response({"error": "No hay emisores registrados en la base de datos"}, status=status.HTTP_400_BAD_REQUEST)
            emisor = emisor_obj

            # Obtener o asignar receptor
            if receptor_id and receptor_id != "nuevo":
                receptor = Receptor_fe.objects.get(id=receptor_id)
            else:
                tipo_doc, _ = TiposDocIDReceptor.objects.get_or_create(
                    codigo='13', defaults={"descripcion": "DUI/NIT"}
                )
                receptor, _ = Receptor_fe.objects.update_or_create(
                    num_documento=nit_receptor,
                    defaults={
                        'nombre': nombre_receptor,
                        'tipo_documento': tipo_doc,
                        'direccion': direccion_receptor,
                        'telefono': telefono_receptor,
                        'correo': correo_receptor
                    }
                )

            # Configuración por defecto de la factura
            ambiente_obj = Ambiente.objects.get(codigo="01")
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            tipo_item_obj = TipoItem.objects.get(codigo=tipo_item)

            tipomodelo_obj = Modelofacturacion.objects.get(codigo="1")
            tipooperacion_obj = CondicionOperacion.objects.get(id=tipooperacion_id) if tipooperacion_id else None
            tipo_moneda_obj = TipoMoneda.objects.get(codigo="USD")

            factura = FacturaElectronica.objects.create(
                version="1.0",
                tipo_dte=tipo_dte_obj,
                numero_control=numero_control,
                codigo_generacion=codigo_generacion,
                tipomodelo=tipomodelo_obj,
                tipocontingencia=None,
                motivocontin=None,
                tipomoneda=tipo_moneda_obj,
                dteemisor=emisor,
                dtereceptor=receptor,
                json_original={},
                firmado=False,
                base_imponible = base_imponible_checkbox
            )

            # Inicializar acumuladores globales
            total_gravada = Decimal("0.00")  # Suma de totales netos
            total_iva = Decimal("0.00")       # Suma de totales IVA
            total_pagar = Decimal("0.00")     # Suma de totales con IVA
            DecimalRetIva = Decimal("0.00")
            DecimalRetRenta = Decimal("0.00")
            DecimalIvaPerci = Decimal("0.00")
            total_operaciones = Decimal("0.00")
            total_descuento_gravado = Decimal("0.00")
            total_no_gravado = Decimal("0.00")
            sub_total = Decimal("0.00")
            porc_descuento_global = Decimal("0.00")
            total_iva_item = Decimal("0.00")
            precio_inc_neto = Decimal("0.00")
            descuento_gravado = Decimal("0.00")
            
            #Campos DTE
            tributo_valor = None

            # Recorrer productos para crear detalles (realizando el desglose)
            print("productos.: ", productos_ids)
            for index, prod_id in enumerate(productos_ids):
                try:
                    producto = Producto.objects.get(id=prod_id)
                except Producto.DoesNotExist:
                    continue
                total_pagar  = Decimal("0.00")
                # Obtener unidad de medida
                #Unidad de medida = 99 cuando el contribuyente preste un servicio
                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo="99")
                else:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo=producto.unidad_medida.codigo)

                #Cantidad = 1, Si se utiliza el campo base imponible, si el tipo de item es 4, ...
                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    cantidad = 1
                else:
                    cantidad = int(cantidades[index]) if index < len(cantidades) else 1
                print("-Cantidad: ", cantidad, "index: ", index)
                
                # El precio del producto ya incluye IVA 
                precio_incl = producto.preunitario
                
                #Campo tributos
                #if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS: 
                    # Codigo del tributo (tributos.codigo)
                tributoIva = Tributo.objects.get(codigo="20")#IVA este codigo solo aplica a ventas gravadas(ya que estan sujetas a iva)
                tributo_valor = tributoIva.valor_tributo
                tributos = [str(tributoIva.codigo)]
                #else:
                    #tributos = None
                
                if tributo_valor is None:
                    tributo_valor = Decimal("0.00")
                
                #Campo precioUni
                if base_imponible_checkbox is True:
                    precio_neto = float(0.00)
                else:
                    precio_neto = (precio_incl * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_iva_item = ( precio_neto * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    precio_inc_neto = precio_incl
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    precio_neto = (precio_neto * Decimal(tributo_valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    
                precio_neto = Decimal(precio_neto)          
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #total_iva_item = ( ( precio_neto * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                #Campo descuento(montoDescu)
                print("-porcentaje api view: ", porcentaje_descuento_producto)
                if porcentaje_descuento_producto:
                    porcentaje_descuento_item = Descuento.objects.get(porcentaje=porcentaje_descuento_producto)
                else:
                    porcentaje_descuento_item = Descuento.objects.first()
                
                if porcentaje_descuento_item.porcentaje > Decimal("0.00"):
                    descuento_aplicado=True
                else:
                    descuento_aplicado = False
                print("-Descuento por item", porcentaje_descuento_item.porcentaje)
                
                # Totales por ítem
                #Campo Ventas gravadas
                print(f"Monto descuento: {monto_descuento}")
                if monto_descuento:
                    monto_descuento = (Decimal(monto_descuento) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    monto_descuento = Decimal("0.00")
                print(f"Precio neto = {precio_neto}, descuento grav = {descu_gravado}")
                #Descuento a ventas gravadas
                if descu_gravado is None or descu_gravado == "":
                    descu_gravado = Decimal("0.00")
                    
                total_descuento_gravado = (precio_neto * porcentaje_descuento_item.porcentaje).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #total_neto = ((precio_neto * cantidad) - (porcentaje_descuento_item.porcentaje / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_neto = (precio_neto - total_descuento_gravado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                descuento_gravado = (total_neto * Decimal(descu_gravado) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print("descuento aplicado")
                print("calcular descuento global: ", descuento_global)
                sub_total_item = Decimal("0")
                if descuento_global:
                    porc_descuento_global = (total_neto * Decimal(descuento_global) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    sub_total_item = (total_neto - descuento_gravado - porc_descuento_global).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    sub_total_item = (total_neto - descuento_gravado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print(f"-subTotal = {sub_total_item}, total neto = {total_neto}, porcentaje = {descu_gravado}, descuento global = {porc_descuento_global} ")
                print(f"IVA Item = {total_iva_item}, iva unitario = {iva_unitario}, cantidad = {cantidad}, total neto = {total_neto} ")
                #Campo codTributo
                cuerpo_documento_tributos = []
                tributo = None
                if producto.tributo is None:
                    seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                    return Response({"error": "Seleccionar tributo para el producto" })
                
                #Tributo sujeto iva (asociado al prod)
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    tributo = Tributo.objects.get(codigo=producto.tributo.codigo)
                    precio_neto = (precio_neto * Decimal(tributo.valor_tributo)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    
                print("-Crear detalle factura")
                detalle = DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    unidad_medida=unidad_medida_obj,
                    precio_unitario=precio_inc_neto * Decimal("-1"),  # Se almacena el precio bruto (con IVA)
                    descuento=porcentaje_descuento_item,
                    tiene_descuento = descuento_aplicado,
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=total_neto * Decimal("-1"),  # Total neto
                    pre_sug_venta=precio_inc_neto * Decimal("-1"),
                    no_gravado=Decimal("0.00"),
                    saldo_favor=Decimal("0.00"),
                    tipo_documento_relacionar = tipo_doc_relacionar,
                    documento_relacionado = documento_relacionado
                )
                #resumen.totalGravado y subTotalVentas
                total_gravada += total_neto
                sub_total += sub_total_item
                
                #Calcular el valor del tributo
                if tributo_valor is not None:
                    valorTributo = ( Decimal(total_gravada) * Decimal(tributo_valor) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_operaciones = (sub_total + valorTributo + DecimalIvaPerci) - DecimalRetIva
                else:
                    total_operaciones = sub_total
                
                total_operaciones = (total_gravada + valorTributo + DecimalIvaPerci) - DecimalRetIva
                total_con_iva = total_operaciones - DecimalIvaPerci - DecimalRetIva - DecimalRetRenta - total_no_gravado
                
                total_iva += total_iva_item
                #total_pagar += total_con_iva
                total_pagar = total_con_iva
                
                # Actualizamos manualmente los campos calculados
                detalle.total_sin_descuento = total_neto * Decimal("-1")
                detalle.iva = total_iva_item * Decimal("-1")
                detalle.total_con_iva = total_con_iva * Decimal("-1")
                detalle.iva_item = total_iva_item * Decimal("-1") # Guardamos el total IVA para este detalle
                detalle.save()
                
                print("-Aplicar tributo sujeto iva")
                valor_porcentaje = Decimal(porcentaje_descuento_item.porcentaje)
                
                if valor_porcentaje.compare(Decimal("0.00")) > 0:
                    total_descuento_gravado += porcentaje_descuento_item.porcentaje
                print("-Total desc gravado: ", total_descuento_gravado)
                
            # Calcular retenciones (globales sobre el total neto de cada detalle)
            if retencion_iva and porcentaje_retencion_iva > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_iva:
                        DecimalRetIva += (detalle.total_sin_descuento * porcentaje_retencion_iva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if retencion_renta and porcentaje_retencion_renta > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_renta:
                        DecimalRetRenta += (detalle.total_sin_descuento * porcentaje_retencion_renta / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            print("porcentaje rete iva", porcentaje_retencion_iva)
            print("porcentaje renta", porcentaje_retencion_renta)
            # Redondear totales globales
            total_iva = total_iva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_pagar = total_pagar.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            #Sino se ha seleccionado ningun documento a relacionar enviar null los campos
            if tipo_doc_relacionar is COD_DOCUMENTO_RELACIONADO_NO_SELEC:
                tipo_doc_relacionar = None
                documento_relacionado = None
            print(f"Tipo de doc a relacionar: {tipo_doc_relacionar} numero de documento: {documento_relacionado}")

            # Actualizar totales en la factura
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = Decimal(total_gravada) * Decimal("-1")
            factura.sub_total_ventas = Decimal(total_gravada) * Decimal("-1")
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = Decimal(descuento_gravado) * Decimal("-1")
            factura.por_descuento = Decimal(porc_descuento_global) * Decimal("-1") #Decimal("0.00")
            factura.total_descuento = Decimal(monto_descuento) * Decimal("-1")
            factura.sub_total = Decimal(sub_total) * Decimal("-1")
            factura.iva_retenido = Decimal(DecimalRetIva) * Decimal("-1")
            factura.retencion_renta = DecimalRetRenta
            factura.total_operaciones = Decimal(total_operaciones) * Decimal("-1") #total_gravada
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = Decimal(total_pagar) * Decimal("-1")
            factura.total_letras = num_to_letras(total_pagar)
            factura.total_iva = Decimal(total_iva) * Decimal("-1")
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = Decimal(DecimalIvaPerci) * Decimal("-1")
            factura.tipo_documento_relacionar = tipo_doc_relacionar
            factura.documento_relacionado = documento_relacionado
            factura.save()

            # Construir el cuerpoDocumento para el JSON con desglose
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                        
                print("-N° items: ", idx)
                print("-Codigo generacion factura: ", det.factura.codigo_generacion)
                #Items permitidos 2000
                if idx > items_permitidos:
                    return Response({"error": "Cantidad máxima de ítems permitidos " }, {items_permitidos})
                else:
                    codTributo = None 
                    tributo_valor = None
                    cuerpo_documento_tributos = []
                    
                    if det.producto.tributo is None:
                        seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                        return Response({"error": "Seleccionar tributo para el producto" })
                    else:
                        if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                            codTributo = tributo.codigo
                            
                            #Si el tributo asociado el prod pertenece a la seccion 2 de la tabla agregar un segundo item
                            if tributo.tipo_tributo.codigo == COD_TRIBUTOS_SECCION_2:
                                print("-Crear nuevo item")
                                #Nuevo item (requerido cuando el tributo es de la seccion 2)
                                cuerpo_documento_tributos.append({
                                    "numItem": idx+1,
                                    "tipoItem": int(tipo_item_obj.codigo),
                                    "numeroDocumento": str(det.documento_relacionado),
                                    "cantidad": float(det.cantidad), 
                                    "codigo": str(det.producto.codigo),
                                    "codTributo": codTributo,
                                    "uniMedida": int(det.unidad_medida.codigo),
                                    "descripcion": str(tributo.descripcion),
                                    "precioUni": float(abs(det.precio_unitario)),
                                    "montoDescu": float(abs(det.descuento.porcentaje)),
                                    "ventaNoSuj": float(0.0),
                                    "ventaExenta": float(0.0),
                                    "ventaGravada": float(abs(det.ventas_gravadas)),
                                    "tributos": tributos
                                })

                    if contingencia:#Detalle contingencia
                        cuerpo_documento.append({
                            "noItem": idx,
                            "tipoDoc": str(det.factura_id.codigo_generacion),
                            "codigoGeneracion": str(emisor.nombre_razon_social)
                        })
                    else:
                        cuerpo_documento.append({
                            "numItem": idx,
                            "tipoItem": int(tipo_item_obj.codigo),
                            "numeroDocumento": str(det.documento_relacionado),
                            "cantidad": float(det.cantidad), 
                            "codigo": str(det.producto.codigo),
                            "codTributo": codTributo,
                            "uniMedida": int(det.unidad_medida.codigo), 
                            "descripcion": str(det.producto.descripcion),
                            "precioUni": float(abs(det.precio_unitario)),
                            "montoDescu": float(abs(det.descuento.porcentaje)),
                            "ventaNoSuj": float(abs(det.ventas_no_sujetas)),
                            "ventaExenta": float(abs(det.ventas_exentas)),
                            "ventaGravada": float(abs(det.ventas_gravadas)),
                            "tributos": tributos
                        })
                                        
                    if cuerpo_documento_tributos is None:
                        cuerpo_documento.append(cuerpo_documento_tributos)
                print(f"Item {idx}: IVA unitario = {iva_unitario}, Total IVA = {total_iva_item}, IVA almacenado = {det.iva_item}")
        
            docs_permitidos = 50
            #tipo_dte_ob = Tipo_dte.objects.get(codigo=tipo_dte)
            factura_relacionar = None
            tipo_documento = None
            
            #Si supera el limite de documentos relacionados detener el proceso
            print("-Inicio recorrer documentos relacionados: ", documentos_relacionados)
            if documentos_relacionados is not None and documentos_relacionados !=[]:
                print("-Existen documentos relacionados")
                for idx, docR in enumerate(documentos_relacionados, start=1):
                    if idx > docs_permitidos:
                        return Response({"error": "Limite de documentos relacionados: " }, {docs_permitidos})
                    
                    #No permitir relacionar documentos de diferentes tipos, es decir, si es NC no se pueden asociar CCF y NR al mismo tiempo
                    
                print("Documentos relacionados agregados: ", idx)
            
            print("-Tipo doc relacionado: ", tipo_doc_relacionar, "doc a relacionar: ", documento_relacionado)
            #Buscar documento relacionado
            if tipo_doc_relacionar:
                if tipo_doc_relacionar == RELACIONAR_DOC_FISICO:
                    # Q permite realizar busqueda por varios campos
                    #factura_relacionar = FacturaElectronica.objects.get( Q(numero_control=numero_documento) & (Q(tipo_dte.codigo == "03") | Q(tipo_dte.codigo == "07")) )
                    factura_relacionar = FacturaElectronica.objects.get( numero_control=documento_relacionado )
                else:#documento electronico
                    #factura_relacionar = FacturaElectronica.objects.get( Q(codigo_generacion=numero_documento) & (Q(tipo_dte.codigo == "03") | Q(tipo_dte.codigo == "07")) )
                    factura_relacionar = FacturaElectronica.objects.get( codigo_generacion=documento_relacionado )
            
            print("-Inicio json docs relacionados: ", factura_relacionar)
            #Si existe el documento generar estructura de documentos relacionados
            if factura_relacionar is not None and factura_relacionar.estado and factura_relacionar.sello_recepcion is not None and factura_relacionar.sello_recepcion !="":
                tipo_documento = factura_relacionar.tipo_dte.codigo
                tipo_dte_doc_relacionar = tipo_documento
                #Crear json
                documento_relacionado_json  = {
                    "tipoDocumento": str(tipo_documento) if str(tipo_documento) else None,
                    "tipoGeneracion": int(tipo_doc_relacionar),
                    "numeroDocumento": str(documento_relacionado).upper(),
                    "fechaEmision": str(factura_relacionar.fecha_emision)
                }
                documentos_relacionados.append(documento_relacionado_json)
                print("-Lista documentos relacionados: ", documentos_relacionados)

            elif factura_relacionar is None:
                notificar_respuesta = "Error: Documento a relacionar no encontrado."
            else:
                notificar_respuesta = "Verifica que el DTE este vigente para poder relacionarlo."
                
            if contingencia:
                generar_json_contingencia(emisor, cuerpo_documento)
            else:
                factura_json = generar_json_doc_ajuste(
                    ambiente_obj, tipo_dte_obj, factura, emisor, receptor,
                    cuerpo_documento, observaciones, documentos_relacionados, contingencia, total_gravada
                )

            
            factura.json_original = factura_json
            factura.save()

            # Guardar el JSON en la carpeta "FE/json_facturas"
            json_path = os.path.join("FE/json_facturas", f"{factura.numero_control}.json")
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(factura_json, f, indent=4, ensure_ascii=False)

                return Response({
                    "mensaje": "Factura generada correctamente",
                    "factura_id": factura.id,
                    "numero_control": factura.numero_control,
                    "redirect": reverse('detalle_factura', args=[factura.id])
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error al generar la factura: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FirmarFacturaAPIView(APIView):
    """
    Firma la factura y, si ya está firmada, la envía a Hacienda.
    """

    def post(self, request, factura_id, format=None):
        print("-Inicio firma DTE api view")
        factura = get_object_or_404(FacturaElectronica, id=factura_id)

        token_data = Token_data.objects.filter(activado=True).first()
        if not token_data:
            return Response(
                {"error": "No hay token activo registrado en la base de datos."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not os.path.exists(CERT_PATH):
            return Response(
                {"error": "No se encontró el certificado en la ruta especificada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar y formatear el JSON original de la factura
        try:
            if isinstance(factura.json_original, dict):
                dte_json_str = json.dumps(factura.json_original, separators=(',', ':'))
            else:
                json_obj = json.loads(factura.json_original)
                dte_json_str = json.dumps(json_obj, separators=(',', ':'))
        except Exception as e:
            return Response(
                {"error": "El JSON original de la factura no es válido", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construir el payload con los parámetros requeridos
        payload = {
            "nit": "06142811001040",   # Nit del contribuyente
            "activo": True,            # Indicador activo
            "passwordPri": "3nCr!pT@d0Pr1v@d@",   # Contraseña de la llave privada
            "dteJson": factura.json_original    # JSON del DTE (se envía tal cual)
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(FIRMADOR_URL, json=payload, headers=headers)

            try:
                response_data = response.json()
            except Exception as e:
                response_data = {"error": "No se pudo parsear JSON", "detalle": response.text}

            # Guardar la respuesta en la factura para depuración y marcar como firmado
            factura.json_firmado = response_data
            factura.firmado = True
            factura.save()

            # Verificar si la firma fue exitosa
            if response.status_code == 200 and response_data.get("status") == "OK":
                # (Opcional) Guardar el JSON firmado en un archivo
                json_signed_path = f"FE/json_facturas_firmadas/{factura.codigo_generacion}.json"
                os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
                with open(json_signed_path, "w", encoding="utf-8") as json_file:
                    json.dump(response_data, json_file, indent=4, ensure_ascii=False)

                return Response({
                    "mensaje": "Factura firmada correctamente",
                    "redirect": reverse('detalle_factura', args=[factura_id])
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Error al firmar la factura",
                    "detalle": response_data
                }, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({
                "error": "Error de conexión con el firmador",
                "detalle": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnviarFacturaHaciendaAPIView(APIView):
    """
    Vista API para enviar la factura a Hacienda.
    Se espera que la URL reciba el parámetro factura_id.
    """
    def post(self, request, factura_id, format=None):
        print("Inicio enviar factura a MH")
        
        contingencia = True
        intento = 1
        intentos_max = 3  # Número máximo de reintentos
        tipo_contiengencia_obj = None
        mensaje = None

        # Buscar la factura por su id
        factura = get_object_or_404(FacturaElectronica, id=factura_id)

        # PASO 1: Autenticación con el servicio de Hacienda
        nit_empresa = str(emisor_fe.nit)  # Ejemplo: "06142811001040"
        pwd = str(emisor_fe.clave_publica)  # Ejemplo: "Q#3P9l5&@aF!gT2sA"
        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MiAplicacionDjango/1.0"
        }
        auth_data = {"user": nit_empresa, "pwd": pwd}
        auth_response = None

        print("Inicio response autenticacion")
        while intento <= intentos_max:
            print(f"Intento {intento} de {intentos_max}")
            try:
                auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
                print("Autenticacion response:", auth_response)
            except requests.exceptions.RequestException as e:
                tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="3")
                time.sleep(8)
                intento += 1
                mensaje = "Error de conexión con el servicio de autenticación: " + str(e)
                print(mensaje)
                continue

            if auth_response:
                try:
                    auth_response_data = auth_response.json()
                except ValueError:
                    print("Error al decodificar la respuesta de autenticación")
                    mensaje = "Error al decodificar la respuesta de autenticación"
                    auth_response.status_code = 500
                    time.sleep(8)
                    intento += 1
                    continue

                print("Autenticacion:", auth_response)
                if auth_response.status_code == 200:
                    token_body = auth_response_data.get("body", {})
                    token = token_body.get("token")
                    token_type = token_body.get("tokenType", "Bearer")
                    roles = token_body.get("roles", [])

                    if token and token.startswith("Bearer "):
                        token = token[len("Bearer "):]

                    token_data_obj, created = Token_data.objects.update_or_create(
                        nit_empresa=nit_empresa,
                        defaults={
                            'password_hacienda': pwd,
                            'token': token,
                            'token_type': token_type,
                            'roles': roles,
                            'activado': True,
                            'fecha_caducidad': timezone.now() + timedelta(days=1)
                        }
                    )
                    contingencia = False
                    break  # Se obtuvo autenticación exitosa
                elif auth_response.status_code == 500:
                    tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="1")
                    time.sleep(8)
                    print(f"Error {auth_response.status_code} - intento {intento}")
                    intento += 1
                elif auth_response.status_code in [502, 503]:
                    tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="2")
                    time.sleep(8)
                    print(f"Error {auth_response.status_code} - intento {intento}")
                    intento += 1
                elif auth_response.status_code == "E010":
                    tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="3")
                    time.sleep(8)
                    print(f"Error {auth_response.status_code} - intento {intento}")
                    intento += 1
                elif auth_response.status_code in ["E015", "E019"]:
                    tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="4")
                    time.sleep(8)
                    print(f"Error {auth_response.status_code} - intento {intento}")
                    intento += 1
                else:
                    mensaje = "Error en la autenticación: " + str(auth_response.status_code)
                    time.sleep(8)
                    intento += 1
                print(f"error: {auth_response.status_code}, tipo contingencia: {tipo_contiengencia_obj}")

        # Verificar que se obtuvo un token activo
        token_data_obj = Token_data.objects.filter(activado=True).first()
        if not token_data_obj or not token_data_obj.token:
            return Response({"error": "No hay token activo para enviar la factura"},
                            status=status.HTTP_401_UNAUTHORIZED)

        codigo_generacion_str = str(factura.codigo_generacion)

        # PASO 2: Validar y limpiar el documento firmado
        documento_str = factura.json_firmado
        if not isinstance(documento_str, str):
            documento_str = json.dumps(documento_str)
        documento_str = documento_str.lstrip('\ufeff').strip()
        try:
            if isinstance(factura.json_firmado, str):
                firmado_data = json.loads(factura.json_firmado)
            else:
                firmado_data = factura.json_firmado
        except Exception as e:
            return Response({
                "error": "Error al parsear el documento firmado",
                "detalle": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        documento_token = firmado_data.get("body", "")
        if not documento_token:
            return Response({
                "error": "El documento firmado no contiene el token en 'body'"
            }, status=status.HTTP_400_BAD_REQUEST)
        documento_token = documento_token.strip()

        # Armar el JSON de envío
        envio_json = {
            "ambiente": AMBIENTE.codigo,  # Ejemplo: "00" para pruebas, "01" para producción
            "idEnvio": factura.id,
            "version": int(factura.json_original["identificacion"]["version"]),
            "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
            "documento": documento_token,  # Se envía el JWT firmado
            "codigoGeneracion": codigo_generacion_str
        }

        envio_headers = {
            "Authorization": f"Bearer {token_data_obj.token}",
            "User-Agent": "DjangoApp",
            "Content-Type": "application/json"
        }

        try:
            print("Inicio envío a Hacienda")
            envio_response = requests.post(
                "https://api.dtes.mh.gob.sv/fesv/recepciondte",
                json=envio_json,
                headers=envio_headers
            )
            print("Envio response status code:", envio_response.status_code)
            print("Envio response headers:", envio_response.headers)
            print("Envio response text:", envio_response.text)

            try:
                response_data = envio_response.json() if envio_response.text.strip() else {}
            except ValueError as e:
                response_data = {"raw": envio_response.text or "No content"}
                print("Error al decodificar JSON en envío:", e)

            if envio_response.status_code == 200:
                factura.sello_recepcion = response_data.get("selloRecibido", "")
                factura.recibido_mh = True
                # Guardar la respuesta de MH en el campo json_original
                json_response_data = {"jsonRespuestaMh": response_data}
                json_original = factura.json_original
                # Combinar ambos diccionarios (usa el operador | para fusionar en Python 3.9+)
                factura.json_original = json_original | json_response_data
                factura.estado = True
                factura.save()
                contingencia = False

                # Actualización de contingencias: se buscan eventos en las últimas 24 horas
                el_salvador_tz = pytz.timezone('America/El_Salvador')
                hora_actual = timezone.now().astimezone(el_salvador_tz)
                plazo_transmitir_contingencia = (hora_actual - timedelta(hours=24)).replace(second=0, microsecond=0)
                contingencia_registrada = EventoContingencia.objects.filter(
                    hora_transmision=plazo_transmitir_contingencia, finalizado=False
                )
                print("Contingencias registradas:", contingencia_registrada)
                if contingencia_registrada.exists():
                    for contingencia_activa in contingencia_registrada:
                        if not contingencia_activa.finalizado:
                            contingencia_activa.finalizado = True
                            contingencia_activa.save()
                else:
                    mensaje = "Contingencias no encontradas"

                return Response({
                    "mensaje": "Factura enviada con éxito",
                    "respuesta": response_data
                }, status=status.HTTP_200_OK)

            elif envio_response.status_code == 500:
                tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="1")
                factura.save()
                time.sleep(8)
                print("Error en el envío de la factura - intento", intento)
                intento += 1
            elif envio_response.status_code in [502, 503]:
                tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="2")
                factura.save()
                time.sleep(8)
                print("Error en el envío de la factura - intento", intento)
                intento += 1
            elif envio_response.status_code == "E010":
                tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="3")
                factura.save()
                time.sleep(8)
                print("Error en el envío de la factura - intento", intento)
                intento += 1
            elif envio_response.status_code in ["E015", "E019"]:
                tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="4")
                factura.save()
                time.sleep(8)
                print("Error en el envío de la factura - intento", intento)
                intento += 1
            else:
                factura.estado = False
                factura.save()
                print("Error en el envío de la factura - intento", intento)
            print(f"error: {envio_response.status_code}, tipo contingencia: {tipo_contiengencia_obj}")

        except requests.exceptions.RequestException as e:
            tipo_contiengencia_obj = TipoContingencia.objects.get(codigo="1")
            factura.estado = False
            factura.contingencia = True
            factura.save()
            contingencia = True
            time.sleep(8)
            intento += 1

        try:
            # Si se está en contingencia, se actualiza la factura y se asocia a un evento de contingencia
            if contingencia:
                factura.estado = False
                factura.contingencia = True
                factura.tipomodelo = Modelofacturacion.objects.get(codigo="2")  # Modelo "Diferido"
                factura.tipotransmision = TipoTransmision.objects.get(codigo="2")  # Transmisión por Contingencia
                factura.save()

                evento_contingencia = EventoContingencia.objects.filter(finalizado=False).first()
                print("Contingencia encontrada:", evento_contingencia)
                if evento_contingencia:
                    evento_contingencia.factura.add(factura)
                    evento_contingencia.save()
                    print("Se agregó la factura al evento de contingencia existente")
                else:
                    print("Creando nueva contingencia")
                    codigo_generacion_contingencia = str(uuid.uuid4()).upper()
                    evento_contingencia = EventoContingencia.objects.create(
                        codigo_generacion=codigo_generacion_contingencia,
                        estado=False,
                        tipo_contingencia=tipo_contiengencia_obj
                    )
                    evento_contingencia.factura.add(factura)
                    evento_contingencia.save()
                return Response({
                    "mensaje": "Factura en contingencia, no se pudo enviar a Hacienda. Se creó evento de contingencia.",
                    "factura_id": factura.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Error de conexión con Hacienda"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

######################################################
# EVENTOS DE INVALIDACION
######################################################
class InvalidarDteUnificadoAPIView(APIView):
    """
    Vista API unificada que realiza en un solo paso:
      1. Genera el DTE de invalidación (llama a invalidacion_dte_view)
      2. Firma el DTE de invalidación (llama a firmar_factura_anulacion_view)
      3. Envía el DTE firmado a Hacienda (llama a enviar_factura_invalidacion_hacienda_view)
    
    Se espera que se realice una petición POST a:
      /api/invalidar-firmar-enviar/<factura_id>/
    """
    def post(self, request, factura_id):
        try:
            # Paso 1: Llamar a la función de invalidación
            response_evento = invalidacion_dte_view(request, factura_id)
            if response_evento.status_code != 302:
                # Si el proceso de invalidación falla, retorna el error
                return Response(json.loads(response_evento.content),
                                status=response_evento.status_code)
            
            # Paso 2: Llamar a la función de firma de la factura de invalidación
            response_firma = firmar_factura_anulacion_view(request, factura_id)
            if response_firma.status_code != 302:
                return Response(json.loads(response_firma.content),
                                status=response_firma.status_code)
            
            # Paso 3: Llamar a la función que envía la factura firmada a Hacienda
            response_envio = enviar_factura_invalidacion_hacienda_view(request, factura_id)
            
            # Consultar el estado final del evento
            evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
            if evento:
                mensaje = "Factura invalidada con éxito" if evento.estado else "No se pudo invalidar la factura"
            else:
                mensaje = "No se encontró el evento de invalidación para la factura"
            
            try:
                detalle = json.loads(response_envio.content)
            except Exception:
                detalle = response_envio.content.decode()
            
            return Response({
                "mensaje": mensaje,
                "detalle": detalle
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#Obtener factura por numero de correlativo
class FacturaPorCodigoGeneracionAPIView(APIView):
    """
    Devuelve la factura por su código de generación, incluyendo receptor y productos.
    """

    def get(self, request):
        global documento_relacionado, productos_ids_r
        documento_relacionado = True
        productos_ids_r = []

        codigo_generacion = request.GET.get("codigo_generacion")
        print("cod generacion relacionado: ", codigo_generacion)
        if not codigo_generacion:
            return Response({"error": "Código de generación no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            factura = FacturaElectronica.objects.get(codigo_generacion=codigo_generacion)
        except FacturaElectronica.DoesNotExist:
            return Response({"error": "Factura no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        detalle_relacionado = DetalleFactura.objects.filter(documento_relacionado=codigo_generacion)
        if detalle_relacionado.exists():
            return Response({"error": "El documento ya tiene una relación con otro Documento Tributario Electrónico."}, status=status.HTTP_400_BAD_REQUEST)

        if not (factura.estado and factura.sello_recepcion):
            return Response({"error": "El DTE no está vigente o no tiene sello de recepción."}, status=status.HTTP_400_BAD_REQUEST)

        receptor = factura.dtereceptor

        productos = []
        for detalle in factura.detalles.all():
            neto_unitario = detalle.precio_unitario / Decimal('1.13')
            iva_unitario = detalle.precio_unitario - neto_unitario
            total_neto = neto_unitario * detalle.cantidad
            total_iva = iva_unitario * detalle.cantidad
            total_incl = detalle.precio_unitario * detalle.cantidad

            productos.append({
                "producto_id": detalle.producto.id,
                "codigo": detalle.producto.codigo,
                "descripcion": detalle.producto.descripcion,
                "cantidad": detalle.cantidad,
                "precio_unitario": str(detalle.precio_unitario),
                "neto_unitario": str(round(neto_unitario, 2)),
                "iva_unitario": str(round(iva_unitario, 2)),
                "total_neto": str(round(total_neto, 2)),
                "total_iva": str(round(total_iva, 2)),
                "total_incl": str(round(total_incl, 2)),
                "descuento": str(detalle.descuento.porcentaje) if detalle.descuento else "",
            })
            productos_ids_r.append(detalle.producto.id)

        response_data = {
            "codigo_generacion": str(factura.codigo_generacion),
            "tipo_documento": factura.tipo_dte.descripcion if factura.tipo_dte else "",
            "num_documento": factura.numero_control,
            "fecha_emision": factura.fecha_emision.strftime("%Y-%m-%d"),
            "fecha_vencimiento": factura.fecha_emision.strftime("%Y-%m-%d") if factura.fecha_emision else "",
            "total": str(factura.total_pagar),
            "receptor": {
                "id": receptor.id,
                "nombre": receptor.nombre,
                "num_documento": receptor.num_documento,
                "direccion": receptor.direccion,
                "telefono": receptor.telefono,
                "correo": receptor.correo,
            },
            "productos": productos
        }

        return Response(response_data, status=status.HTTP_200_OK)

from rest_framework.pagination import PageNumberPagination
class FacturaPagination(PageNumberPagination):
    page_size = 10  # Valor por defecto
    page_size_query_param = 'page_size'  # Permite al cliente especificar el tamaño de página
    max_page_size = 50  # Máximo de registros por página permitido
    
    def get_paginated_response(self, data):
        return Response({
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'total_records': self.page.paginator.count,
            'results': data,
        })

# Crear la vista API usando ListAPIView de DRF
class FacturaListAPIView(generics.ListAPIView):
    serializer_class = FacturaListSerializer
    pagination_class = FacturaPagination

    def get_queryset(self):
        queryset = FacturaElectronica.objects.all()

        recibido = self.request.GET.get('recibido_mh')
        codigo = self.request.GET.get('sello_recepcion')
        has_codigo = self.request.GET.get('has_sello_recepcion')
        tipo_dte = self.request.GET.get('tipo_dte')
        estado = self.request.GET.get('estado')  # Estado normal, por ejemplo "true" o "false"
        estado_invalidacion = self.request.GET.get('estado_invalidacion')  # Para filtrar el estado de invalidación

        if recibido and recibido.lower() in ['true', 'false']:
            queryset = queryset.filter(recibido_mh=(recibido.lower() == 'true'))
        if codigo:
            queryset = queryset.filter(sello_recepcion__icontains=codigo)
        if has_codigo and has_codigo.lower() in ['true', 'false']:
            if has_codigo.lower() == 'true':
                queryset = queryset.exclude(sello_recepcion__isnull=True)
            else:
                queryset = queryset.filter(sello_recepcion__isnull=True)
        if tipo_dte:
            queryset = queryset.filter(tipo_dte__id=tipo_dte)
        if estado and estado.lower() in ['true', 'false']:
            queryset = queryset.filter(estado=(estado.lower() == 'true'))
        if estado_invalidacion:
            estado_inv_lower = estado_invalidacion.lower()
            if estado_inv_lower == "invalidada":
                queryset = queryset.filter(dte_invalidacion__estado=True)
            elif estado_inv_lower == "firmar":
                # Filtra facturas sin evento de invalidación y con recibido_mh == False (Firma pendiente).
                queryset = queryset.filter(dte_invalidacion__isnull=True, recibido_mh=False)
            elif estado_inv_lower == "enproceso":
                queryset = queryset.filter(dte_invalidacion__estado=False)
            elif estado_inv_lower == "viva":
                queryset = queryset.filter(dte_invalidacion__isnull=True)
                

        return queryset

######################################################
# EVENTOS DE CONTINGENCIA
######################################################

class ContingenciaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContingenciaListAPIView(generics.ListAPIView):
    """
    Lista los eventos de contingencia con filtros:
    - recibido_mh: True/False
    - sello_recepcion: búsqueda parcial
    - has_sello_recepcion: 'yes'/'no'
    - tipo_dte: id del tipo
    """
    serializer_class = EventoContingenciaSerializer
    pagination_class = ContingenciaPagination

    def get_queryset(self):
        qs = EventoContingencia.objects.prefetch_related(
            'factura', 'factura__tipo_dte', 'lotes_evento'
        ).order_by('id')

        recibido = self.request.query_params.get('recibido_mh')
        sello   = self.request.query_params.get('sello_recepcion')
        has_sello = self.request.query_params.get('has_sello_recepcion')
        tipo    = self.request.query_params.get('tipo_dte')

        if recibido in ['True', 'False', '0']:
            qs = qs.filter(recibido_mh=(recibido == 'True'))
        if sello:
            qs = qs.filter(sello_recepcion__icontains=sello)
        if has_sello == 'yes':
            qs = qs.exclude(sello_recepcion__isnull=True)
        elif has_sello == 'no':
            qs = qs.filter(sello_recepcion__isnull=True)
        if tipo:
            qs = qs.filter(lotes_evento__factura__tipo_dte__id=tipo)

        return qs
    

    """
    Genera el JSON de contingencia para un EventoContingencia,
    lo guarda en json_original y devuelve el JSON resultante.
    """
    def post(self, request, contingencia_id):
        evento = get_object_or_404(EventoContingencia, id=contingencia_id)
        
        detalles_dte = []
        # Recolectamos todas las facturas de todos los lotes
        for lote in evento.lotes_evento.all():
            for fe in lote.factura.all():
                detalles_dte.append({
                    "noItem": len(detalles_dte) + 1,
                    "tipoDoc":   str(fe.tipo_dte.codigo),
                    "codigoGeneracion": str(fe.codigo_generacion).upper()
                })
        
        # Si no hay facturas, devolvemos error
        if not detalles_dte:
            return Response(
                {"error": "No se encontraron facturas en los lotes de contingencia."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Armado del JSON completo
        ahora = datetime.now()
        fecha_transmision = ahora.strftime('%Y-%m-%d')
        
        json_identificacion = {
            "version": 3,
            "ambiente": str(AMBIENTE.codigo),
            "codigoGeneracion": str(evento.codigo_generacion).upper(),
            "fTransmision": fecha_transmision,
            "hTransmision": ahora.strftime('%H:%M:%S'),
        }
        
        em = request.user.emisor_fe  # o como tengas la instancia de emisor_fe
        json_emisor = {
            "nit": str(em.nit),
            "nombre": em.nombre_razon_social,
            "nombreResponsable": em.nombre_razon_social,
            "tipoDocResponsable": em.tipo_documento.codigo,
            "numeroDocResponsable": str(em.nit),
            "tipoEstablecimiento": em.tipoestablecimiento.codigo if em.tipoestablecimiento else "",
            "codEstableMH": em.codigo_establecimiento,
            "codPuntoVenta": em.codigo_punto_venta,
            "telefono": em.telefono,
            "correo": em.email,
        }
        
        json_motivo = {
            "fInicio": evento.fecha_transmision.strftime('%Y-%m-%d'),
            "fFin": evento.fecha_transmision.strftime('%Y-%m-%d'),
            "hInicio": evento.hora_transmision.strftime('%H:%M:%S'),
            "hFin": ahora.strftime('%H:%M:%S'),
            "tipoContingencia": int(evento.tipo_contingencia.codigo),
            "motivoContingencia": (
                evento.tipo_contingencia.motivo_contingencia
                if evento.tipo_contingencia.codigo == COD_TIPO_CONTINGENCIA
                else None
            )
        }
        
        json_completo = {
            "identificacion": json_identificacion,
            "emisor": json_emisor,
            "detalleDTE": detalles_dte,
            "motivo": json_motivo
        }
        
        # Guardamos en el evento
        evento.json_original = json_completo
        evento.fecha_modificacion = timezone.now().date()
        evento.hora_modificacion = now = datetime.now()
        evento.save()
        
        return Response(json_completo, status=status.HTTP_200_OK)
    
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ContingenciaDteAPIView(APIView):
    """
    Genera el JSON de contingencia para un EventoContingencia dado,
    lo guarda en json_original y devuelve el JSON resultante.
    """

    def post(self, request, contingencia_id):
        evento = get_object_or_404(EventoContingencia, id=contingencia_id)

        # Generar detalleDTE
        detalles = []
        for lote in evento.lotes_evento.all():
            for fe in lote.factura.all():
                detalles.append({
                    "noItem": len(detalles) + 1,
                    "tipoDoc": str(fe.tipo_dte.codigo),
                    "codigoGeneracion": str(fe.codigo_generacion).upper(),
                })

        if not detalles:
            return Response(
                {"error": "No se encontraron facturas en los lotes de contingencia."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fechas
        ahora = datetime.now()
        fecha_str = ahora.strftime('%Y-%m-%d')
        hora_str  = ahora.strftime('%H:%M:%S')

        # JSON Identificación
        json_ident = {
            "version": 3,
            "ambiente": str(AMBIENTE.codigo),
            "codigoGeneracion": str(evento.codigo_generacion).upper(),
            "fTransmision": fecha_str,
            "hTransmision": hora_str,
        }

        # JSON Emisor (ajusta emisor_fe como corresponda)
        em = request.user.emisor_fe  
        json_emisor = {
            "nit": str(em.nit),
            "nombre": em.nombre_razon_social,
            "nombreResponsable": em.nombre_razon_social,
            "tipoDocResponsable": em.tipo_documento.codigo,
            "numeroDocResponsable": str(em.nit),
            "tipoEstablecimiento": em.tipoestablecimiento.codigo if em.tipoestablecimiento else "",
            "codEstableMH": em.codigo_establecimiento,
            "codPuntoVenta": em.codigo_punto_venta,
            "telefono": em.telefono,
            "correo": em.email,
        }

        # JSON Motivo
        json_motivo = {
            "fInicio": evento.fecha_transmision.strftime('%Y-%m-%d'),
            "fFin": evento.fecha_transmision.strftime('%Y-%m-%d'),
            "hInicio": evento.hora_transmision.strftime('%H:%M:%S'),
            "hFin": hora_str,
            "tipoContingencia": int(evento.tipo_contingencia.codigo),
            "motivoContingencia": (
                evento.tipo_contingencia.motivo_contingencia
                if evento.tipo_contingencia.codigo == COD_TIPO_CONTINGENCIA
                else None
            )
        }

        # JSON Completo
        json_completo = {
            "identificacion": json_ident,
            "emisor": json_emisor,
            "detalleDTE": detalles,
            "motivo": json_motivo,
        }

        # Guardar en la instancia
        evento.json_original = json_completo
        evento.fecha_modificacion = timezone.now().date()
        evento.hora_modificacion = ahora
        evento.save()

        return Response(json_completo, status=status.HTTP_200_OK)
    

# ENVIO DE LOTES EN CONTINGENCIA


@method_decorator(csrf_exempt, name='dispatch')
class LoteContingenciaDteAPIView(APIView):
    """
    Crea un LoteContingencia para una Factura en un EventoContingencia activo
    (o crea uno nuevo si no hay ninguno disponible).
    """

    MAX_LOTES_POR_EVENTO = 2

    def post(self, request, factura_id, tipo_contingencia_id):
        # 1) Obtener la factura y el tipo de contingencia
        factura = get_object_or_404(FacturaElectronica, id=factura_id)
        tipo = get_object_or_404(TipoContingencia, id=tipo_contingencia_id)

        # 2) Solo permitimos facturas en modo contingencia
        if not factura.contingencia:
            return Response(
                {"error": "El documento electrónico no está disponible en contingencia."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Buscar un EventoContingencia activo con espacio para más lotes
        eventos = EventoContingencia.objects.annotate(
            num_lotes=count('lotes_evento')
        ).filter(finalizado=False, recibido_mh=False, num_lotes__lt=self.MAX_LOTES_POR_EVENTO)

        if eventos.exists():
            evento = eventos.first()
        else:
            # 4) Crear uno nuevo
            evento = EventoContingencia.objects.create(
                codigo_generacion = str(uuid.uuid4()).upper(),
                tipo_contingencia = tipo
            )

        # 5) Crear el lote
        try:
            lote = LoteContingencia.objects.create(
                factura = factura,
                evento  = evento
            )
        except Exception as e:
            return Response(
                {"error": "No se pudo crear el lote", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 6) Devolver datos del lote
        serializer = LoteContingenciaSerializer(lote)
        return Response(
            {"mensaje": f"Lote creado con éxito (id={lote.id})", "lote": serializer.data},
            status=status.HTTP_201_CREATED
        )
    



    