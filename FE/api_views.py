from datetime import datetime, timedelta
import time
from decimal import ROUND_HALF_UP, ConversionSyntax, Decimal
from itertools import count
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import pytz
import requests
import os, json, uuid
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from .views import (
    contingencia_dte_view, enviar_contingencia_hacienda_view, enviar_correo_individual_view, enviar_factura_hacienda_view, enviar_factura_invalidacion_hacienda_view, enviar_lotes_hacienda_view, 
    finalizar_contigencia_view, firmar_contingencia_view, firmar_factura_anulacion_view, firmar_factura_view, 
    invalidacion_dte_view, generar_json, lote_contingencia_dte_view, num_to_letras, agregar_formas_pago_api, generar_json_contingencia, 
    generar_json_doc_ajuste, obtener_fecha_actual, obtener_listado_productos_view
)

from INVENTARIO.serializers import DescuentoSerializer, ProductoSerializer

from .serializers import (
    AmbienteSerializer, EventoContingenciaSerializer, FacturaListSerializer, 
    FormasPagosSerializer, LoteContingenciaSerializer, ReceptorSerializer, FacturaElectronicaSerializer, EmisorSerializer, 
    TipoDteSerializer, TiposGeneracionDocumentoSerializer, ActividadEconomicaSerializer, ModelofacturacionSerializer,
    TipoTransmisionSerializer, TipoContingenciaSerializer, TipoRetencionIVAMHSerializer, TiposEstablecimientosSerializer, TiposServicio_MedicoSerializer,
    OtrosDicumentosAsociadoSerializer, TiposDocIDReceptorSerializer, PaisSerializer, DepartamentoSerializer, MunicipioSerializer, CondicionOperacionSerializer,                                                                                                                                                                                             
    PlazoSerializer, TipoDocContingenciaSerializer, TipoInvalidacionSerializer, TipoDonacionSerializer, TipoPersonaSerializer, TipoTransporteSerializer, INCOTERMS_Serializer,
    TipoDomicilioFiscalSerializer, TipoMonedaSerializer, DescuentoSerializer
    )
from .models import (
    INCOTERMS, ActividadEconomica, Departamento, Emisor_fe, EventoContingencia, LoteContingencia, Municipio, OtrosDicumentosAsociado, Pais, Receptor_fe, FacturaElectronica, DetalleFactura,
    Ambiente, CondicionOperacion, Modelofacturacion, NumeroControl, Tipo_dte, TipoContingencia, TipoDocContingencia, TipoDomicilioFiscal, TipoDonacion, TipoGeneracionDocumento, 
    TipoMoneda, TipoPersona, TipoRetencionIVAMH, TipoTransmision, TipoTransporte, TipoUnidadMedida, TiposDocIDReceptor, EventoInvalidacion, 
    Receptor_fe, TipoInvalidacion, TiposEstablecimientos, TiposServicio_Medico, Token_data, Descuento, FormasPago, TipoGeneracionDocumento, Plazo
)
from INVENTARIO.models import Almacen, DetalleDevolucionVenta, DevolucionVenta, MovimientoInventario, Producto, TipoItem, TipoTributo, Tributo, UnidadMedida
from django.db.models import Q
from django.core.paginator import Paginator  # esta sigue igual

from rest_framework.test import APIRequestFactory
from django.forms.models import model_to_dict
from rest_framework.response import Response
from django.db.models import Count, Sum
from AUTENTICACION.models import ConfiguracionServidor
from django.core.mail import EmailMessage
from intracoe import settings
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string

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
RUTA_COMPROBANTES_PDF = ConfiguracionServidor.objects.filter(codigo="ruta_comprobantes_dte").first()
RUTA_COMPROBANTES_JSON = ConfiguracionServidor.objects.filter(codigo="ruta_comprobante_json").first()
RUTA_JSON_FACTURA = ConfiguracionServidor.objects.filter(codigo="json_factura").first()

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

class Tipo_dteDetailAPIView(generics.RetrieveAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteCreateAPIView(generics.CreateAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

class Tipo_dteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Tipo_dte.objects.all()
    serializer_class = TipoDteSerializer

    def get_object(self):
        """
        Sobrescribe el método `get_object()` para que recupere el objeto
        basándose en el parámetro `codigo` en lugar de `id`.
        """
        codigo = self.kwargs['codigo']
        # Usamos get_object_or_404 para simplificar la obtención y manejo de errores
        tipo_dte = get_object_or_404(Tipo_dte, codigo=codigo)
        return tipo_dte


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

class TiposDocIDReceptorDetailAPIView(generics.RetrieveAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorCreateAPIView(generics.CreateAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

class TiposDocIDReceptorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TiposDocIDReceptor.objects.all()
    serializer_class = TiposDocIDReceptorSerializer

    def get_object(self):
        """
        Sobrescribe el método `get_object()` para que recupere el objeto
        basándose en el parámetro `codigo` en lugar de `id`.
        """
        codigo = self.kwargs['codigo']
        return TiposDocIDReceptor.objects.get(codigo=codigo)

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

class CondicionOperacionDetailAPIView(generics.RetrieveAPIView):
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

class ProductoListAPIView(APIView):
    global tipo_documento_dte

    def get(self, request, format=None):
        print("request listado de productos: ", request)

        documento_ajuste = request.query_params.get('documento_ajuste', False)
        if documento_ajuste:
            tipo_documento_dte = request.GET.get('tipo_documento_dte', '05')
        else:
            tipo_documento_dte = request.GET.get('tipo_documento_dte', '01')

        tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_documento_dte)
        productos = Producto.objects.all()  # No incluye la imagen
        
        descuentos = list(Descuento.objects.all().values())
        tipoItems = list(TipoItem.objects.all().values())
        productos_modificados = []

        if productos:
            #recorrer todos los productos y mostrarlos con IVA si aplica
            for producto in productos:
                if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
                    if producto.precio_iva:
                        producto.preunitario = (producto.preunitario).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    else:
                        producto.preunitario = (producto.preunitario * Decimal("1.13")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                else:
                    if producto.precio_iva:
                        producto.preunitario = (producto.preunitario / Decimal("1.13")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    else:
                        producto.preunitario = (producto.preunitario).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                #Excluir el campo "imagen" de la lista
                productos_modificados.append(producto)
        
        # Convertir los productos a diccionario, excluyendo la imagen
        productos_dict = [model_to_dict(producto, exclude=['imagen']) for producto in productos_modificados]
        
        #Retornar los productos modificados temporalmente
        return Response(productos_dict, status=200)

class GenerarFacturaAPIView(APIView):
    """
    Vista API para generar facturas.
    En GET se retornan los datos para armar el formulario (en vez de renderizar una plantilla)  
    y en POST se procesa la generación de la factura.
    """
    cod_generacion = str(uuid.uuid4()).upper()
    global productos_ids_r
    productos_ids_r = []
    global cantidades_prod_r
    cantidades_prod_r = []
    global documentos_relacionados
    documentos_relacionados = []
    global descuentos_r
    descuentos_r = []
    global emisor_fe
    
    # Puedes agregar permisos o autenticación según tus necesidades:
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        
        # Inicializamos las variables globales (aunque es recomendable evitar globals)
        global productos_ids_r, cantidades_prod_r, documentos_relacionados, descuentos_r
        productos_ids_r = []
        cantidades_prod_r = []
        documentos_relacionados = []
        descuentos_r = []
        
        tipo_dte = request.query_params.get('tipo_dte', '01')

        emisor_obj = Emisor_fe.objects.first()
        if emisor_obj:
            nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
        else:
            nuevo_numero = ""
        print("Numero de control: ", nuevo_numero)
        codigo_generacion = str(uuid.uuid4()).upper()#self.cod_generacion
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

        # Se convierten los querysets a listas de diccionarios
        #productos = list(Producto.objects.all().values())
        
        #1.Llamar al listado de productos(simular un request GET), 2.Crear una instancia de APIRequestFactory(para solicitudes http), enviar parametros
        # request = APIRequestFactory().get('/api/productos/', {'documento_ajuste': 'False', 'tipo_documento_dte': '01'})
        # vista = ProductoListAPIView.as_view() #Obtener instancia para manejar la solicitud http, obtener productos
        # response = vista(request) #Simular la solicitud http (request) usando una vista
        # productos = response.data #Obtener los datos de la respuesta
        
        productos_qs = Producto.objects.all()
        productos = ProductoSerializer(productos_qs, many=True).data
        
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
            data = request.data 
            docsRelacionados = []#Acumular los documentos relacionados
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
            #porcentaje_descuento = data.get("descuento_select", "0")
            #porcentaje_descuento_producto = porcentaje_descuento.replace(",", ".")

            # Configuración adicional
            tipooperacion_id = data.get("condicion_operacion", 1)
            porcentaje_retencion_iva = Decimal(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = data.get("retencion_iva", False)
            productos_retencion_iva = data.get("productos_retencion_iva", [])
            porcentaje_retencion_renta = Decimal(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = data.get("retencion_renta", False)
            productos_retencion_renta = data.get("productos_retencion_renta", [])
            #formas_pago_id = data.get('formas_pago_id', [])
            formas_pago_id = agregar_formas_pago_api(request)
            
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
            
            print(f"parametro num control: {numero_control}, tipo dte: {tipo_dte}")
            if not numero_control:
                numero_control = NumeroControl.obtener_numero_control(tipo_dte)
                print("Numero control asignado: ", numero_control)
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
                total_gravada, nombre_responsable, documento_responsable, formas_pago_id
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

######################################################
# FIRMA Y ENVIO DE DOCUMENTOS A MH
######################################################

class FirmarFacturaAPIView(APIView):
    """
    POST /api/factura/{factura_id}/firmar/
    Firma el DTE de la factura y maneja contingencia si falla.
    """
    @transaction.atomic
    def post(self, request, factura_id, format=None):
        factura = get_object_or_404(FacturaElectronica, id=factura_id)
        fecha_actual = obtener_fecha_actual()

        contingencia = True
        mensaje = None
        motivo_otro = False
        mostrar_modal = False
        tipo_contingencia_obj = None
        intentos_max = 3
        response_data = {}

        # Leer intentos previos de sesión
        intentos_sesion = request.session.get('intentos_reintento', 0)

        # Ciclo de intentos
        for intento in range(1, intentos_max + 1):
            # Verificar token activo
            token_data = Token_data.objects.filter(activado=True).first()
            if not token_data:
                return Response({"error": "No hay token activo."}, status=status.HTTP_401_UNAUTHORIZED)
            # Verificar certificado
            if not os.path.exists(CERT_PATH):
                return Response({"error": "Certificado no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
            # Preparar JSON a firmar
            try:
                if isinstance(factura.json_original, dict):
                    dte_obj = factura.json_original
                else:
                    dte_obj = json.loads(factura.json_original)
            except Exception as e:
                return Response({"error": "JSON inválido", "detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            payload = {
                "nit": str(factura.dteemisor.nit),
                "activo": True,
                "passwordPri": str(factura.dteemisor.clave_privada),
                "dteJson": dte_obj
            }
            try:
                resp = requests.post(FIRMADOR_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
                try:
                    response_data = resp.json()
                except ValueError:
                    response_data = {"error": "No se pudo parsear JSON", "detalle": resp.text}
                # Éxito
                if resp.status_code == 200 and response_data.get("status") == "OK":
                    factura.json_firmado = response_data
                    factura.firmado = True
                    factura.save()
                    # Resetear intentos en sesión
                    request.session['intentos_reintento'] = 0
                    request.session.modified = True
                    contingencia = False
                    mostrar_modal = False
                    return Response({
                        "mensaje": "Firma exitosa",
                        "detalle": response_data
                    }, status=status.HTTP_200_OK)
                # Error transitorio o definitivo
                if resp.status_code in [500,502,503,504,408]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                elif resp.status_code in [408,499]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                elif resp.status_code in [503,504]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                else:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                    motivo_otro = True
                    mensaje = f"Error en firma: {resp.status_code}"
                time.sleep(8)
            except requests.RequestException as e:
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                time.sleep(8)
            # continue next attempt

        # Si tras todos los intentos sigue en contingencia
        if contingencia:
            # Crear evento de contingencia si aplica
            if intentos_sesion == 0:
                finalizar_contigencia_view(request)
                factura.estado = False
                factura.contingencia = True
                factura.tipomodelo = Modelofacturacion.objects.get(codigo="2")
                factura.tipotransmision = TipoTransmision.objects.get(codigo="2")
                factura.fecha_modificacion = fecha_actual.date()
                factura.hora_modificacion = fecha_actual.time()
                factura.save()
                lote_contingencia_dte_view(request, factura_id, tipo_contingencia_obj)
            # Actualizar sesión
            request.session['intentos_reintento'] = intentos_sesion + 1
            request.session.modified = True
            return Response({
                "error": "No se pudo firmar el DTE después de varios intentos",
                "motivo_otro": motivo_otro
            }, status=status.HTTP_400_BAD_REQUEST)

        # Caso inesperado
        return Response({"error": "Error inesperado en firma"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnviarFacturaHaciendaAPIView(APIView):
    """
    POST /api/factura/{factura_id}/enviar/
    Autentica con MH, envía el DTE, registra movimientos de inventario y maneja contingencia.
    """
    global emisor_fe
    @transaction.atomic
    def post(self, request, factura_id, format=None):
        try:
            factura = get_object_or_404(FacturaElectronica, id=factura_id)
            fecha_actual = obtener_fecha_actual()
            print("factura_id: ", factura_id)
        
            # Paso 1: Autenticación
            nit = str(emisor_fe.nit)
            pwd = str(emisor_fe.clave_publica)
            auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
            auth_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "MiAplicacionDjango/1.0"
            }
            auth_data = {"user": nit, "pwd": pwd}

            contingencia = True
            error_auth = None
            for intento in range(1, 4):
                try:
                    resp = requests.post(auth_url, data=auth_data, headers=auth_headers, timeout=30)
                    if resp.status_code == 200:
                        try:
                            resp_data = resp.json()
                            body = resp_data.get("body", {})
                            if not isinstance(body, dict):
                                body = {}
                        except ValueError as e:
                            print(f"Error al parsear JSON: {e}")
                            body = {}
                        
                        token = body.get("token", "")
                        if token.startswith("Bearer "):
                            token = token.split(" ", 1)[1]
                        
                        Token_data.objects.update_or_create(
                            nit_empresa=nit,
                            defaults={
                                "password_hacienda": pwd,
                                "token": token,
                                "token_type": body.get("tokenType", "Bearer"),
                                "roles": body.get("roles", []),
                                "activado": True,
                                "fecha_caducidad": timezone.now() + timedelta(days=1)
                            }
                        )
                        contingencia = False
                        print("Fin token")
                        error_auth = None  # Éxito, no hay error
                        break
                    else:
                        error_auth = f"Auth failed {resp.status_code}"
                except requests.RequestException as e:
                    error_auth = str(e)
                time.sleep(8)

            print("factura_id1: ", factura_id)
            print("datos: ", request)
            if error_auth:
                print("Error autenticacion: ", error_auth)
            else:
                print("Autenticacion exitosa")

            if contingencia:
                return Response(
                    {"error": "No se autenticó con Hacienda", "detalle": error_auth},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            
            # Paso 2: Envío del DTE
            token_obj = Token_data.objects.filter(activado=True).first()
            if not token_obj or not token_obj.token:
                return Response({"error": "Sin token activo"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                dte_json = factura.json_firmado
                if isinstance(dte_json, str):
                    dte_json = json.loads(dte_json)
            except Exception as e:
                return Response(
                    {"error": "JSON firmado inválido", "detalle": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            documento = dte_json.get("body", "").strip()

            print("documento: ", documento)

            if not documento:
                return Response(
                    {"error": "Falta token en 'body' del JSON firmado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            envio_url = "https://api.dtes.mh.gob.sv/fesv/recepciondte"
            envio_headers = {
                "Authorization": f"Bearer {token_obj.token}",
                "User-Agent": "MiAplicacionDjango/1.0",
                "Content-Type": "application/json"
            }
            payload = {
                "ambiente": AMBIENTE.codigo,
                "idEnvio": factura.id,
                "version": int(factura.json_original["identificacion"]["version"]),
                "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
                "documento": documento,
                "codigoGeneracion": str(factura.codigo_generacion)
            }

            error_envio = None
            for intento in range(1, 4):
                try:
                    resp = requests.post(envio_url, json=payload, headers=envio_headers, timeout=30)
                    data = resp.json() if resp.text.strip() else {}
                    print("Response envio mh: data: ", data)
                    if resp.status_code == 200 and data.get("selloRecibido"):
                        # Actualizar factura
                        factura.sello_recepcion = data["selloRecibido"]
                        factura.recibido_mh = True
                        factura.estado = True
                        factura.contingencia = False
                        factura.json_original = {**factura.json_original, "jsonRespuestaMh": data}
                        
                        #Enviar correo
                        if factura.recibido_mh == False:
                            enviar_correo_individual_view(request, factura_id, None, None)
                            factura.envio_correo = True
                        factura.save()
                        
                        # Registrar movimiento de inventario
                        for det in factura.detalles.all():
                            if det is not None and det.producto.almacenes.exists():
                                almacen = det.producto.almacenes.first() or Almacen.objects.first()
                                MovimientoInventario.objects.create(
                                    producto=det.producto,
                                    almacen=almacen,
                                    tipo='Salida',
                                    cantidad=det.cantidad,
                                    referencia=f"Factura {factura.codigo_generacion}"
                                )
                        # Finalizar contingencias
                        finalizar_contigencia_view(request)
                        return Response(
                            {"mensaje": "Factura enviada con éxito", "respuesta": data},
                            status=status.HTTP_200_OK
                        )
                    else:
                        error_envio = f"Envio failed {resp.status_code}"
                except requests.RequestException as e:
                    error_envio = str(e)
                time.sleep(8)

            # Si llegó aquí, envió falló repetidamente → contingencia
            factura.estado = False
            factura.contingencia = True
            
            #Enviar correo
            if factura:
                enviar_correo_individual_view(request, factura_id, None, None)
                factura.envio_correo_contingencia = True
            
            factura.save()
            return Response(
                {"error": "Error al enviar factura", "detalle": error_envio},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print("Error inesperado:")
            return Response(
                {"error": "Error interno del servidor", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

######################################################
# EVENTOS DE INVALIDACION
######################################################

# EVENTO DE INVALIDACION UNIFICADO
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
        
# OBTRENER FACTURA POR CODIGO DE GENERACION
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

# PAGINACION PARA FACTURAS
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

# LISTAR FACTURAS
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

# ENVIAR FACTURA INVALIDACION HACIENDA
class EnviarFacturaInvalidacionAPIView(APIView):
    """
    POST /api/factura/{factura_id}/invalidar/
    Autentica con MH, envía la invalidación de la factura,
    reingresa el inventario y registra la devolución de venta.
    """
    @transaction.atomic
    def post(self, request, factura_id, format=None):
        # 1) Autenticación con MH
        nit = "06142811001040"
        pwd = "Q#3P9l5&@aF!gT2sA"
        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        auth_resp = requests.post(auth_url,
                                  data={"user": nit, "pwd": pwd},
                                  headers={
                                      "Content-Type": "application/x-www-form-urlencoded",
                                      "User-Agent": "MiAplicacionDjango/1.0"
                                  },
                                  timeout=30)
        try:
            auth_body = auth_resp.json().get("body", {})
        except ValueError:
            return Response(
                {"error": "Error al decodificar autenticación", "detalle": auth_resp.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if auth_resp.status_code != 200:
            return Response(
                {"error": "Autenticación fallida", "detalle": auth_body.get("message", auth_resp.text)},
                status=auth_resp.status_code
            )

        token = auth_body.get("token", "")
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        Token_data.objects.update_or_create(
            nit_empresa=nit,
            defaults={
                "password_hacienda": pwd,
                "token": token,
                "token_type": auth_body.get("tokenType", "Bearer"),
                "roles": auth_body.get("roles", []),
                "activado": True,
                "fecha_caducidad": timezone.now() + timedelta(days=1)
            }
        )

        # 2) Obtener evento de invalidación
        evento = get_object_or_404(EventoInvalidacion, factura__id=factura_id)

        # 3) Validar JSON firmado
        try:
            firmado = evento.json_firmado
            if isinstance(firmado, str):
                firmado = json.loads(firmado)
        except Exception as e:
            return Response(
                {"error": "JSON firmado inválido", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        documento = firmado.get("body", "").strip()
        if not documento:
            return Response(
                {"error": "El JSON firmado no contiene 'body'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Envío de invalidación a Hacienda
        envio_url = "https://api.dtes.mh.gob.sv/fesv/anulardte"
        envio_headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "MiAplicacionDjango/1.0",
            "Content-Type": "application/json"
        }
        payload = {
            "ambiente": "01",
            "idEnvio": evento.id,
            "version": int(evento.json_invalidacion["identificacion"]["version"]),
            "documento": documento
        }
        try:
            resp = requests.post(envio_url, json=payload, headers=envio_headers, timeout=30)
            try:
                data = resp.json()
            except ValueError:
                data = {"raw": resp.text}
        except requests.RequestException as e:
            return Response(
                {"error": "Error de conexión con Hacienda", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 5) Procesar respuesta
        if resp.status_code == 200:
            # Actualizar evento
            evento.sello_recepcion = data.get("selloRecibido", "")
            evento.recibido_mh = True
            evento.json_invalidacion = {**evento.json_invalidacion, "jsonRespuestaMh": data}
            evento.estado = True
            evento.save()

            # 6) Reingresar inventario y registrar devolución
            factura = evento.factura
            devolucion = DevolucionVenta.objects.create(
                num_factura=factura.numero_control,
                motivo="Devolución por invalidación",
                estado="Aprobada",
                usuario=request.user.username if request.user.is_authenticated else None
            )
            for det in factura.detalles.all():
                DetalleDevolucionVenta.objects.create(
                    devolucion=devolucion,
                    producto=det.producto,
                    cantidad=det.cantidad,
                    motivo_detalle="Reingreso automático por invalidación"
                )
                almacen = det.producto.almacenes.first() or Almacen.objects.first()
                MovimientoInventario.objects.create(
                    producto=det.producto,
                    almacen=almacen,
                    tipo='Entrada',
                    cantidad=det.cantidad,
                    referencia=f"Invalidación Factura {factura.codigo_generacion}"
                )
                Producto.objects.filter(pk=det.producto.pk).update(
                    stock=F('stock') + det.cantidad
                )

            return Response(
                {"mensaje": "Factura invalidada con éxito", "respuesta": data},
                status=status.HTTP_200_OK
            )
        else:
            # Error al invalidar
            evento.estado = False
            evento.save()
            return Response(
                {"error": "Error al invalidar", "detalle": data},
                status=resp.status_code
            )

# INVALIDACION DE VARIOS DTE
class InvalidarVariasDteAPIView(APIView):
    """
    POST /api/dte/invalidar-lote/
    Invalidación en lote de múltiples DTEs: crea evento, firma, envía, y reingresa stock.
    """
    @transaction.atomic
    def post(self, request, format=None):
        factura_ids = request.data.get('factura_ids')
        if not isinstance(factura_ids, list):
            return Response(
                {"error": "Se requiere 'factura_ids' como lista."},
                status=status.HTTP_400_BAD_REQUEST
            )
        results = []
        for factura_id in factura_ids:
            entry = {"factura_id": factura_id}
            # 1) Invalidación DTE
            resp_inv = invalidacion_dte_view(request, factura_id)
            if getattr(resp_inv, 'status_code', None) != 302:
                entry.update({
                    "mensaje": "Error en invalidación",
                    "detalle": getattr(resp_inv, 'content', b'').decode(errors='ignore')
                })
                results.append(entry)
                continue
            # 2) Firma invalidación
            resp_firma = firmar_factura_anulacion_view(request, factura_id)
            if getattr(resp_firma, 'status_code', None) != 302:
                entry.update({
                    "mensaje": "Error en firma",
                    "detalle": getattr(resp_firma, 'content', b'').decode(errors='ignore')
                })
                results.append(entry)
                continue
            # 3) Envío a Hacienda
            resp_env = enviar_factura_invalidacion_hacienda_view(request, factura_id)
            content_env = getattr(resp_env, 'content', b'')
            # 4) Procesar estado en BD
            evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
            if evento and evento.estado:
                entry['mensaje'] = 'Factura invalidada con éxito'
                # Reingresar inventario y registrar devolución
                factura = get_object_or_404(FacturaElectronica, id=factura_id)
                devolucion = DevolucionVenta.objects.create(
                    num_factura=factura.numero_control,
                    motivo='Devolución por invalidación múltiple',
                    estado='Aprobada',
                    usuario=request.user.username if request.user and request.user.is_authenticated else None
                )
                for detalle in factura.detalles.all():
                    DetalleDevolucionVenta.objects.create(
                        devolucion=devolucion,
                        producto=detalle.producto,
                        cantidad=detalle.cantidad,
                        motivo_detalle='Reingreso automático por invalidación'
                    )
                    almacen = detalle.producto.almacenes.first() or Almacen.objects.first()
                    MovimientoInventario.objects.create(
                        producto=detalle.producto,
                        almacen=almacen,
                        tipo='Entrada',
                        cantidad=detalle.cantidad,
                        referencia=f'Reingreso invalidación Factura {factura.numero_control}'
                    )
                    Producto.objects.filter(pk=detalle.producto.pk).update(
                        stock=F('stock') + detalle.cantidad
                    )
            else:
                entry['mensaje'] = 'No se pudo invalidar la factura'
            # 5) Detalle de respuesta de envío
            try:
                entry['detalle'] = json.loads(content_env)
            except Exception:
                entry['detalle'] = content_env.decode(errors='ignore')
            results.append(entry)
        return Response({"results": results}, status=status.HTTP_200_OK)


######################################################
# EVENTOS DE CONTINGENCIA
######################################################

# PAGINACION DE CONTINGENCIAS
class ContingenciaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# LISTAR CONTINGENCIA
class ContingenciaListAPIView(APIView):
    """
    API para listar eventos de contingencia con lotes y facturas agrupadas,
    aplicando filtros y paginación.
    """
    def get(self, request, format=None):
        try:
            # 1) Finalizar contingencias vencidas
            finalizar_contigencia_view(request)

            # 2) Parámetros de tiempo
            fecha_actual = obtener_fecha_actual()
            fecha_limite = fecha_actual - timezone.timedelta(hours=72)

            # 3) Queryset base
            queryset = (
                EventoContingencia.objects
                .prefetch_related('lotes_contingencia__factura')
                .distinct()
                .order_by('id')
            )

            # 4) Filtros GET
            recibido = request.GET.get('recibido_mh')
            codigo = request.GET.get('sello_recepcion')
            has_codigo = request.GET.get('has_sello_recepcion')
            tipo_dte_id = request.GET.get('tipo_dte')

            if recibido in ['True', 'False', '0']:
                queryset = queryset.filter(recibido_mh=(recibido == 'True'))
            if codigo:
                queryset = queryset.filter(sello_recepcion__icontains=codigo)
            if has_codigo == 'yes':
                queryset = queryset.exclude(sello_recepcion__isnull=True)
            elif has_codigo == 'no':
                queryset = queryset.filter(sello_recepcion__isnull=True)
            if tipo_dte_id:
                queryset = queryset.filter(
                    lotes_contingencia__factura__tipo_dte__id=tipo_dte_id
                )

            # 5) Paginación
            paginator = PageNumberPagination()
            paginator.page_size = 20
            page = paginator.paginate_queryset(queryset, request)

            # 6) Construir resultado
            eventos_con_lotes = []
            for evento in page:
                # Obtener facturas relacionadas
                lotes = list(evento.lotes_contingencia.all())
                facturas = [l.factura for l in lotes]

                # Finalizar lotes vencidos (si aplica)
                if (
                    evento.sello_recepcion is not None
                    and evento.recibido_mh
                    and evento.fecha_sello_recibido is not None
                ):
                    if evento.fecha_sello_recibido <= fecha_limite:
                        for lote in lotes:
                            if not lote.finalizado:
                                lote.finalizado = True
                                lote.fecha_modificacion = fecha_actual.date()
                                lote.hora_modificacion = fecha_actual.time()
                                lote.save()

                # Agrupar en bloques de 100
                facturas_en_grupos = []
                for i in range(0, len(facturas), 100):
                    grupo = facturas[i : i + 100]
                    
                    mostrar_checkbox_lote = any(
                        (not f.recibido_mh)
                        and f.sello_recepcion
                        and evento.sello_recepcion is None
                        for f in grupo
                    )
                    facturas_serializadas = [
                        {
                            'id': f.id,
                            'serie': getattr(f, 'serie', None),
                            'numero': getattr(f, 'numero', None),
                            'recibido_mh': f.recibido_mh,
                            'sello_recepcion': f.sello_recepcion,
                            'fecha_emision': f.fecha_emision,
                            'total_pagar': f.total_pagar,
                            'numero_control': f.numero_control,
                            # 'tipo_dte': f.tipo_dte
                        }
                        for f in grupo
                    ]
                    facturas_en_grupos.append({
                        'facturas': facturas_serializadas,
                        'mostrar_checkbox_lote': mostrar_checkbox_lote
                    })

                eventos_con_lotes.append({
                    'id': evento.id,
                    'recibido_mh': evento.recibido_mh,
                    'sello_recepcion': evento.sello_recepcion,
                    'fecha_sello_recibido': evento.fecha_sello_recibido,
                    'facturas_en_grupos': facturas_en_grupos,
                    'total_lotes_evento': len(facturas_en_grupos),
                    'codigo_generacion': evento.codigo_generacion,
                    'motivo_contingencia': evento.motivo_contingencia,
                    'mostrar_checkbox': any(
                        (not f.recibido_mh) and f.sello_recepcion is None
                        for f in facturas
                    )
                })

            # 7) Tipos DTE
            tipos_dte = list(
                Tipo_dte.objects
                .filter(codigo__in=DTE_APLICA_CONTINGENCIA)
                .values('id', 'codigo', 'descripcion')
            )

            # 8) Respuesta paginada
            return paginator.get_paginated_response({
                'results': eventos_con_lotes,
                'tipos_dte': tipos_dte
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# CONTINGENCIA DTE UNIFICADO
class ContingenciaDteUnificadoAPIView(APIView):
    """
    Ejecuta de forma unificada:
      1) Generación de JSON de contingencia,
      2) Firma del evento,
      3) Envío a Hacienda,
      4) Consulta de estado y detalle.
    """
    def get(self, request, format=None):
        contingencia_id = request.query_params.get("contingencia_id")
        if not contingencia_id:
            return Response(
                {"error": "Falta parámetro 'contingencia_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 1: Generar JSON de contingencia
        try:
            resp_gen = contingencia_dte_view(request, contingencia_id)
            if hasattr(resp_gen, 'status_code') and resp_gen.status_code not in (302, 200):
                return Response(
                    {"error": "Error al generar contingencia", "detail": resp_gen.content},
                    status=resp_gen.status_code
                )
        except Exception as e:
            return Response(
                {"error": "Excepción al generar contingencia", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Paso 2: Firmar el evento
        try:
            resp_firma = firmar_contingencia_view(request, contingencia_id)
            if hasattr(resp_firma, 'status_code') and resp_firma.status_code not in (302, 200):
                return Response(
                    {"error": "Error al firmar contingencia", "detail": resp_firma.content},
                    status=resp_firma.status_code
                )
        except Exception as e:
            return Response(
                {"error": "Excepción al firmar contingencia", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Paso 3: Envío a Hacienda
        try:
            resp_envio = enviar_contingencia_hacienda_view(request, contingencia_id)
            status_envio = getattr(resp_envio, 'status_code', None)
            contenido = getattr(resp_envio, 'content', b'')
        except Exception as e:
            return Response(
                {"error": "Excepción al enviar a Hacienda", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Paso 4: Determinar mensaje según el estado en la BD
        evento = EventoContingencia.objects.filter(id=contingencia_id).first()
        if evento:
            mensaje = "Contingencia enviada con éxito" if evento.recibido_mh else "No se pudo enviar la contingencia"
        else:
            mensaje = "No se encontró el evento de contingencia"

        # Paso 5: Procesar detalle de la respuesta de envío
        if status_envio == 200:
            try:
                detalle = json.loads(contenido)
            except Exception:
                detalle = contenido.decode(errors='ignore')
        else:
            detalle = {
                "status_code": status_envio,
                "content": contenido.decode(errors='ignore')
            }

        return Response(
            {"mensaje": mensaje, "detalle": detalle},
            status=status.HTTP_200_OK
        )

# CONTINGENCIA DTE
class ContingenciaDteAPIView(APIView):
    """
    Genera el JSON de contingencia para un evento, lo guarda en json_original
    y retorna ese JSON como respuesta.
    """
    def get(self, request, format=None):
        contingencia_id = request.query_params.get("contingencia_id")
        if not contingencia_id:
            return Response(
                {"error": "Falta parámetro 'contingencia_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Obtener el evento
        try:
            evento = EventoContingencia.objects.get(id=contingencia_id)
        except EventoContingencia.DoesNotExist:
            return Response(
                {"error": "Evento no encontrado", "detalle": "No existe un evento con ese ID"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2) Reunir facturas de los lotes
        try:
            facturas = [lote.factura for lote in evento.lotes_contingencia.all()]
        except Exception as e:
            return Response(
                {"error": "No se pudieron obtener las facturas", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not facturas:
            return Response(
                {
                    "error": "El evento no contiene lotes asignados",
                    "detalle": "Debe haber al menos una factura asociada"
                },
                status=status.HTTP_204_NO_CONTENT
            )

        # 3) Construir detalleDTE
        detalles_dte = []
        for idx, fe in enumerate(facturas, start=1):
            detalles_dte.append({
                "noItem": idx,
                "tipoDoc": str(fe.tipo_dte.codigo),
                "codigoGeneracion": str(fe.codigo_generacion).upper()
            })

        # 4) Armar JSON completo
        try:
            fecha_actual = obtener_fecha_actual()
            fTransm = fecha_actual.strftime('%Y-%m-%d')
            hTransm = datetime.now().strftime('%H:%M:%S')

            json_identificacion = {
                "version": 3,
                "ambiente": str(AMBIENTE.codigo),
                "codigoGeneracion": str(evento.codigo_generacion).upper(),
                "fTransmision": fTransm,
                "hTransmision": hTransm
            }

            json_emisor = {
                "nit": str(emisor_fe.nit),
                "nombre": str(emisor_fe.nombre_razon_social),
                "nombreResponsable": str(emisor_fe.representante.nombre) if emisor_fe.representante else str(emisor_fe.nombre_razon_social),
                "tipoDocResponsable": str(emisor_fe.representante.tipo_documento.codigo) if emisor_fe.representante else str(emisor_fe.tipo_documento.codigo),
                "numeroDocResponsable": str(emisor_fe.representante.numero_documento) if emisor_fe.representante else str(emisor_fe.nit),
                "tipoEstablecimiento": str(emisor_fe.tipoestablecimiento.codigo) if emisor_fe.tipoestablecimiento else "",
                "codEstableMH": str(emisor_fe.codigo_establecimiento),
                "codPuntoVenta": str(emisor_fe.codigo_punto_venta),
                "telefono": str(emisor_fe.telefono),
                "correo": str(emisor_fe.email)
            }

            json_motivo = {
                "fInicio": str(evento.fecha_transmision),
                "fFin": str(evento.f_fin),
                "hInicio": evento.hora_transmision.strftime('%H:%M:%S'),
                "hFin": evento.h_fin.strftime('%H:%M:%S'),
                "tipoContingencia": int(evento.tipo_contingencia.codigo)
            }
            # Motivo opcional
            if evento.tipo_contingencia and evento.tipo_contingencia.codigo == COD_TIPO_CONTINGENCIA:
                json_motivo["motivoContingencia"] = evento.tipo_contingencia.motivo_contingencia
            else:
                json_motivo["motivoContingencia"] = None

            json_completo = {
                "identificacion": json_identificacion,
                "emisor": json_emisor,
                "detalleDTE": detalles_dte,
                "motivo": json_motivo
            }

            # 5) Guardar en el modelo
            evento.json_original = json_completo
            evento.fecha_modificacion = fecha_actual.date()
            evento.hora_modificacion = fecha_actual.time()
            evento.save()

            # 6) Responder con el JSON generado
            return Response(
                {"json_original": json_completo},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Error generando JSON de contingencia", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# FIRMAR CONTINGENCIA
class FirmarContingenciaAPIView(APIView):
    """
    Firma un evento de contingencia y guarda el resultado.
    """
    def get(self, request, format=None):
        contingencia_id = request.query_params.get("contingencia_id")
        if not contingencia_id:
            return Response(
                {"error": "Falta parámetro 'contingencia_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Cargar evento
        try:
            evento = EventoContingencia.objects.get(id=contingencia_id)
        except EventoContingencia.DoesNotExist:
            return Response(
                {"error": "Evento de contingencia no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        fecha_actual = obtener_fecha_actual()
        intentos_max = 3
        intento = 1
        response_data = None

        # 2) Bucle de intentos
        while intento <= intentos_max:
            # 2.1) Validar token
            token = Token_data.objects.filter(activado=True).first()
            if not token:
                return Response(
                    {"error": "No hay token activo registrado en la base de datos."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 2.2) Validar certificado
            if not os.path.exists(CERT_PATH):
                return Response(
                    {"error": f"No se encontró el certificado en {CERT_PATH}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2.3) Preparar JSON del evento
            try:
                # Asegurarse de tener dict
                if isinstance(evento.json_original, str):
                    dte_json_obj = json.loads(evento.json_original)
                else:
                    dte_json_obj = evento.json_original
            except Exception as e:
                return Response(
                    {"error": "JSON original inválido", "detalle": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            payload = {
                "nit": str(emisor_fe.nit),
                "activo": True,
                "passwordPri": str(emisor_fe.clave_privada),
                "dteJson": dte_json_obj
            }

            try:
                resp = requests.post(FIRMADOR_URL, json=payload, timeout=30)
                status_code = resp.status_code
                try:
                    response_data = resp.json()
                except ValueError:
                    response_data = {"error": "Respuesta no JSON", "detalle": resp.text}

                # 2.4) Evaluar éxito
                if status_code == 200 and response_data.get("status") == "OK":
                    evento.json_firmado = response_data
                    evento.firmado = True
                    evento.fecha_modificacion = fecha_actual.date()
                    evento.hora_modificacion = fecha_actual.time()
                    evento.save()

                    # (Opcional) Guardar archivo local
                    os.makedirs(os.path.dirname(CERT_PATH), exist_ok=True)
                    path = f"FE/json_facturas_firmadas/{evento.codigo_generacion}.json"
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(response_data, f, indent=4, ensure_ascii=False)

                    return Response(
                        {
                            "mensaje": "Firma de contingencia exitosa",
                            "detalle": response_data
                        },
                        status=status.HTTP_200_OK
                    )

                # 2.5) Si falla, asignar tipo de contingencia y reintentar
                codigo = str(status_code)
                if status_code in [500, 502, 503, 504, 408]:
                    tipo = "1"
                elif status_code in [408, 499]:
                    tipo = "2"
                elif status_code in [503, 504]:
                    tipo = "4"
                else:
                    tipo = "5"
                evento.tipo_contingencia = TipoContingencia.objects.get(codigo=tipo)
                evento.save()

                intento += 1
                time.sleep(8)

            except requests.exceptions.RequestException as e:
                # Errores de red
                evento.tipo_contingencia = TipoContingencia.objects.get(codigo="3")
                evento.save()
                response_data = {"error": "Error de conexión", "detalle": str(e)}
                intento += 1
                time.sleep(8)

        # 3) Si agotó los intentos sin éxito
        evento.fecha_modificacion = fecha_actual.date()
        evento.hora_modificacion = fecha_actual.time()
        evento.save()
        return Response(
            {
                "error": "Error al firmar la contingencia tras varios intentos",
                "detalle": response_data
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# ENVIAR CONTINGENCIA A HACIENDA
class EnviarContingenciaHaciendaAPIView(APIView):
    """
    Autentica con MH, envia el DTE firmado y actualiza el EventoContingencia
    """

    def get(self, request, format=None):
        contingencia_id = request.query_params.get("contingencia_id")

        if not contingencia_id:
            return Response(
                {"error": "Falta parametro 'contingencia_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 0) Preparativos
        fecha_actual = obtener_fecha_actual()
        try:
            evento = EventoContingencia.objects.get(id=contingencia_id)
        except EventoContingencia.DoesNotExist:
            return Response(
                {"error": "Evento de contingencia no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        nit = str(emisor_fe.nit)
        pwd = str(emisor_fe.clave_publica)
        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MiAplicacionDjango/1.0"
        }
        auth_data = {"user": nit, "pwd": pwd}

        # 1) Autenticación con Hacienda
        intentos_max = 3
        error_auth = None
        token = None

        for intento in range(1, intentos_max + 1):
            try:
                resp = requests.post(auth_url, data=auth_data, headers=auth_headers, timeout=30)
                if resp.status_code == 200:
                    body = resp.json().get("body", {})
                    token = body.get("token", "")
                    if token.startswith("Bearer "):
                        token = token[len("Bearer "):]
                    Token_data.objects.update_or_create(
                        nit_empresa=nit,
                        defaults={
                            "password_hacienda": pwd,
                            "token": token,
                            "token_type": body.get("tokenType", "Bearer"),
                            "roles": body.get("roles", []),
                            "activado": True,
                            "fecha_caducidad": timezone.now() + timedelta(days=1)
                        }
                    )
                    break
                # si falla la autenticación, asignar tipo de contingencia
                if resp.status_code in [500,502,503,504,408]:
                    codigo_tc = "1"
                elif resp.status_code in [408,499]:
                    codigo_tc = "2"
                elif resp.status_code in [503,504]:
                    codigo_tc = "4"
                else:
                    codigo_tc = "5"
                TipoContingencia.objects.filter(codigo=codigo_tc).update()
                error_auth = f"Auth error {resp.status_code}"
            except requests.RequestException as e:
                TipoContingencia.objects.filter(codigo="1").update()
                error_auth = str(e)
            time.sleep(8)

        # si tras reintentos no hay token
        if not token:
            evento.fecha_modificacion = fecha_actual.date()
            evento.hora_modificacion = fecha_actual.time()
            evento.save()
            return Response(
                {
                    "error": "No se autenticó con Hacienda tras varios intentos",
                    "detalle": error_auth
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Envío del DTE firmado
        envio_url = "https://api.dtes.mh.gob.sv/fesv/contingencia"
        envio_headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "MiAplicacionDjango/1.0",
            "Content-Type": "application/json"
        }
        # Preparar documento firmado
        try:
            firmado = evento.json_firmado
            if isinstance(firmado, str):
                firmado = json.loads(firmado)
            documento_token = firmado.get("body", "")
        except Exception as e:
            return Response(
                {"error": "JSON firmado inválido", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not documento_token:
            return Response(
                {"error": "El JSON firmado no contiene 'body' con el token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = {"nit": nit, "documento": documento_token}
        error_envio = None

        for intento in range(1, intentos_max + 1):
            try:
                resp = requests.post(envio_url, headers=envio_headers, json=payload, timeout=30)
                status_code = resp.status_code
                data = resp.json() if resp.text.strip() else {}

                # éxito
                if status_code == 200 and data.get("selloRecibido"):
                    evento.sello_recepcion = data["selloRecibido"]
                    evento.recibido_mh = True
                    evento.finalizado = True

                    # combinar en json_original
                    evento.json_original = {
                        **evento.json_original,
                        "jsonRespuestaMh": data
                    }
                    evento.fecha_sello_recibido = fecha_actual
                    evento.fecha_modificacion = fecha_actual.date()
                    evento.hora_modificacion = fecha_actual.time()
                    evento.save()

                    return Response(
                        {"mensaje": "Contingencia enviada con éxito", "respuesta": data},
                        status=status.HTTP_200_OK
                    )

                # asignar tipo de contingencia según error
                if status_code in [500,502,503,504,408]:
                    tc = "1"
                elif status_code in [408,499]:
                    tc = "2"
                elif status_code in [503,504]:
                    tc = "4"
                else:
                    tc = "5"
                TipoContingencia.objects.filter(codigo=tc).update()

                error_envio = f"Envio error {status_code}"
            except requests.RequestException as e:
                TipoContingencia.objects.filter(codigo="1").update()
                error_envio = str(e)
            time.sleep(8)

        # si agotó intentos sin éxito
        evento.fecha_modificacion = fecha_actual.date()
        evento.hora_modificacion = fecha_actual.time()
        evento.save()
        return Response(
            {
                "error": "Excedido el máximo número de intentos de envío",
                "detalle": error_envio
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# FINALIZAR EL EVENTO DE CONTINGENCIA
class FinalizarContingenciaAPIView(APIView):
    """
    Cierra automáticamente los eventos de contingencia activos o rechazados
    que tengan más de 24 horas sin finalizar.
    """
    def get(self, request, format=None):
        try:
            zona = pytz.timezone('America/El_Salvador')
            fecha_actual = obtener_fecha_actual()
            fecha_limite = fecha_actual - timezone.timedelta(hours=24)

            # 1) Buscar contingencias activas (no rechazadas, no finalizadas)
            contingencias_activas = []
            eventos = EventoContingencia.objects.filter(rechazado=False, finalizado=False)
            for ev in eventos:
                try:
                    dt = zona.localize(datetime.combine(ev.fecha_transmision, ev.hora_transmision))
                    if dt <= fecha_limite:
                        contingencias_activas.append(ev)
                except Exception:
                    pass

            # 2) Buscar contingencias rechazadas (rechazado=True, no finalizado)
            eventos_rech = EventoContingencia.objects.filter(rechazado=True, finalizado=False)
            for ev in eventos_rech:
                try:
                    dt = zona.localize(datetime.combine(ev.fecha_modificacion, ev.hora_modificacion))
                    if dt <= fecha_limite:
                        contingencias_activas.append(ev)
                except Exception:
                    pass

            # 3) Finalizar y actualizar los eventos seleccionados
            codigos = []
            if contingencias_activas:
                for ev in contingencias_activas:
                    if not ev.finalizado:
                        ev.finalizado = True
                        ev.f_fin = fecha_actual.date()
                        ev.h_fin = fecha_actual.time()
                        ev.fecha_modificacion = fecha_actual.date()
                        ev.hora_modificacion = fecha_actual.time()
                        ev.save()
                        codigos.append(ev.codigo_generacion)
                mensaje = "Contingencias modificadas"
            else:
                mensaje = "Contingencias no encontradas"

            return Response(
                {"results": [{"contingencia": codigos, "mensaje": mensaje}]},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Error inesperado al actualizar contingencia: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# CREAR LOTE CONTINGENCIA
class LoteContingenciaDteAPIView(APIView):
    """
    Crea un LoteContingencia para una FacturaElectronica en un EventoContingencia existente
    (o crea uno nuevo si no hay espacio) del tipo indicado.
    """
    def get(self, request, format=None):
        factura_id = request.query_params.get("factura_id")
        tipo_id   = request.query_params.get("tipo_contingencia_id")
        if not factura_id or not tipo_id:
            return Response(
                {"error": "Debe indicar 'factura_id' y 'tipo_contingencia_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 1: Obtener factura
        try:
            factura = FacturaElectronica.objects.get(id=factura_id)
        except FacturaElectronica.DoesNotExist:
            return Response(
                {"mensaje": f"Factura con ID {factura_id} no encontrada.",
                 "detalle": "No existe documento electrónico."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Asegurarse de que está en contingencia
        if not factura.contingencia:
            return Response(
                {"mensaje": "El documento electrónico no está marcado como contingencia."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 2: Obtener tipo de contingencia
        try:
            tipo_obj = TipoContingencia.objects.get(id=tipo_id)
        except TipoContingencia.DoesNotExist:
            return Response(
                {"error": f"TipoContingencia con ID {tipo_id} no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Paso 3: Verificar si ya existe lote para esa factura
        if LoteContingencia.objects.filter(factura_id=factura.id).exists():
            return Response(
                {"mensaje": "Ya existe un lote para esa factura."},
                status=status.HTTP_200_OK
            )

        # Paso 4: Buscar o crear EventoContingencia disponible
        max_items = 5000
        evento = (
            EventoContingencia.objects
            .annotate(num_lotes=Count('lotes_contingencia'))
            .filter(finalizado=False, recibido_mh=False, num_lotes__lt=max_items)
            .first()
        )
        if not evento:
            evento = EventoContingencia.objects.create(
                codigo_generacion=str(uuid.uuid4()).upper(),
                tipo_contingencia=tipo_obj
            )

        # Paso 5: Crear el lote
        try:
            lote = LoteContingencia.objects.create(
                factura=factura,
                evento=evento
            )
            return Response(
                {
                    "mensaje": f"Lote creado correctamente",
                    "lote": {
                        "id": lote.id,
                        "factura_id": factura.id,
                        "evento_id": evento.id
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"mensaje": "Error al crear el lote", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ENVIO DE LOTES EN CONTINGENCIA UNIFICADO
class EnvioDteUnificadoAPIView(APIView):
    """
    Flujo unificado para firmar un DTE, enviarlo a Hacienda y actualizar el lote asociado.
    """
    def get(self, request, format=None):
        factura_id = request.query_params.get("factura_id")
        if not factura_id:
            return Response(
                {"error": "Falta parámetro 'factura_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fecha actual en zona El Salvador
        try:
            fecha_actual = obtener_fecha_actual()
        except Exception:
            # Fallback manual
            tz = pytz.timezone('America/El_Salvador')
            fecha_actual = datetime.now(tz)

        # 1) Firma del DTE
        try:
            resp_firma = firmar_factura_view(request, factura_id)
            sc_firma = getattr(resp_firma, "status_code", None)
            # Si no es redirect (302) ni OK (200), devolvemos directamente ese error
            if sc_firma not in (302, 200):
                # Intentamos parsear JSON, o devolvemos texto plano
                content = getattr(resp_firma, "content", b"")
                try:
                    data = json.loads(content)
                except Exception:
                    data = content.decode(errors="ignore") if isinstance(content, (bytes, str)) else {}
                return Response(data, status=sc_firma)
        except Exception as e:
            return Response(
                {"error": "Error al firmar la factura", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 2) Envío a Hacienda
        try:
            resp_envio = enviar_factura_hacienda_view(request, factura_id)
            sc_envio = getattr(resp_envio, "status_code", None)
            content_envio = getattr(resp_envio, "content", b"")
        except Exception as e:
            return Response(
                {"error": "Error al enviar la factura a Hacienda", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3) Verificar en la BD y actualizar lote si corresponde
        try:
            factura = FacturaElectronica.objects.filter(id=factura_id).first()
            if factura and factura.sello_recepcion:
                # Marcar lote como finalizado
                lote = LoteContingencia.objects.filter(factura__id=factura_id).first()
                if lote:
                    lote.finalizado = True
                    lote.recibido_mh = True
                    lote.fecha_modificacion = fecha_actual.date()
                    lote.hora_modificacion = fecha_actual.time()
                    lote.save()
                mensaje = "Factura recibida con éxito"
            elif factura:
                mensaje = "No se pudo enviar la factura"
            else:
                mensaje = "No se encontró el documento electrónico"
        except Exception as e:
            mensaje = "Error al consultar el estado de la factura"
        
        # 4) Procesar detalle de la respuesta de envío
        try:
            if sc_envio == 200:
                try:
                    detalle = json.loads(content_envio)
                except Exception:
                    detalle = content_envio.decode(errors="ignore")
            else:
                detalle = {
                    "status_code": sc_envio,
                    "content": content_envio.decode(errors="ignore")
                }
        except Exception as e:
            detalle = f"Error procesando respuesta de envío: {e}"

        return Response(
            {"mensaje": mensaje, "detalle": detalle},
            status=status.HTTP_200_OK
        )

# FIRMAR Y ENVIAR EN LOTES UNA LISTA DE DTES
class LotesDteAPIView(APIView):
    """
    Firma y envía en lote una lista de DTEs (factura_ids) a Hacienda.
    """
    def post(self, request, format=None):
        factura_ids = request.data.get('factura_ids')
        if not isinstance(factura_ids, list):
            return Response(
                {"error": "Se requiere 'factura_ids' como lista en el body"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        for factura_id in factura_ids:
            entry = {"factura_id": factura_id}
            # 1) Firma
            try:
                resp_firma = firmar_factura_view(request, factura_id)
                sc_firma = getattr(resp_firma, "status_code", None)
                if sc_firma not in (200, 302):
                    # error en firma
                    contenido = getattr(resp_firma, "content", b"")
                    try:
                        detalle = json.loads(contenido)
                    except Exception:
                        detalle = contenido.decode(errors="ignore")
                    entry.update({
                        "mensaje": "Error en firma",
                        "detalle_firma": detalle
                    })
                    results.append(entry)
                    continue
                # parsear detalle de firma
                try:
                    detalle_firma = json.loads(resp_firma.content)
                except Exception:
                    detalle_firma = resp_firma.content.decode(errors="ignore")
                entry["detalle_firma"] = detalle_firma
            except Exception as e:
                entry.update({
                    "mensaje": "Error inesperado al firmar",
                    "detalle_firma": str(e)
                })
                results.append(entry)
                continue

            # 2) Envío
            try:
                resp_envio = enviar_lotes_hacienda_view(request, factura_id)
                sc_envio = getattr(resp_envio, "status_code", None)
                if sc_envio not in (200, 302):
                    contenido = getattr(resp_envio, "content", b"")
                    try:
                        detalle_envio = json.loads(contenido)
                    except Exception:
                        detalle_envio = contenido.decode(errors="ignore")
                    entry.update({
                        "mensaje": "Error en envío",
                        "detalle": detalle_envio
                    })
                    results.append(entry)
                    continue
                # parsear detalle de envío
                try:
                    detalle_envio = json.loads(resp_envio.content)
                except Exception:
                    detalle_envio = resp_envio.content.decode(errors="ignore")
                entry["detalle"] = detalle_envio
            except Exception as e:
                entry.update({
                    "mensaje": "Error inesperado al enviar",
                    "detalle": str(e)
                })
                results.append(entry)
                continue

            # 3) Verificar en BD
            try:
                factura = FacturaElectronica.objects.get(id=factura_id)
                if factura.recibido_mh:
                    entry["mensaje"] = "DTE enviado con éxito"
                else:
                    entry["mensaje"] = "No se pudo enviar el DTE"
            except FacturaElectronica.DoesNotExist:
                entry["mensaje"] = "No se encontró el DTE en la base"
            except Exception:
                entry["mensaje"] = "Error verificando estado del DTE"

            results.append(entry)

        return Response({"results": results}, status=status.HTTP_200_OK)

# AUTENTICAR CON MH Y ENVIAR LOS LOTES
class EnviarLotesHaciendaAPIView(APIView):
    """
    Autentica con MH y envía un DTE firmado (recepciondte),
    actualiza la FacturaElectronica con el sello recibido.
    """
    def post(self, request, format=None):
        factura_id = request.data.get("factura_id")
        if not factura_id:
            return Response(
                {"error": "Se requiere 'factura_id' en el body"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Cargar factura
        factura = get_object_or_404(FacturaElectronica, id=factura_id)

        # 2) Autenticación con MH
        nit = str(emisor_fe.nit)
        pwd = str(emisor_fe.clave_publica)
        auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MiAplicacionDjango/1.0"
        }
        auth_data = {"user": nit, "pwd": pwd}

        try:
            auth_resp = requests.post(auth_url, data=auth_data, headers=auth_headers, timeout=30)
            auth_body = auth_resp.json().get("body", {}) if auth_resp.status_code == 200 else {}
        except requests.RequestException as e:
            return Response(
                {"error": "Error de conexión con el servicio de autenticación", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if auth_resp.status_code != 200:
            return Response(
                {
                    "error": "Error en la autenticación",
                    "detalle": auth_body.get("message", auth_resp.text)
                },
                status=auth_resp.status_code
            )

        # Extraer token
        token = auth_body.get("token", "")
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        Token_data.objects.update_or_create(
            nit_empresa=nit,
            defaults={
                "password_hacienda": pwd,
                "token": token,
                "token_type": auth_body.get("tokenType", "Bearer"),
                "roles": auth_body.get("roles", []),
                "activado": True,
                "fecha_caducidad": timezone.now() + timedelta(days=1)
            }
        )

        # 3) Preparar el DTE firmado
        try:
            firmado = factura.json_firmado
            if isinstance(firmado, str):
                firmado = json.loads(firmado)
            documento_token = firmado.get("body", "").strip()
        except Exception as e:
            return Response(
                {"error": "Error al parsear el documento firmado", "detalle": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not documento_token:
            return Response(
                {"error": "El JSON firmado no contiene 'body' con el token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Envío a recepciondte
        envio_url = "https://api.dtes.mh.gob.sv/fesv/recepciondte"
        envio_headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "DjangoApp",
            "Content-Type": "application/json"
        }
        envio_json = {
            "ambiente": "01",
            "idEnvio": factura.id,
            "version": int(factura.json_original["identificacion"]["version"]),
            "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
            "documento": documento_token,
            "codigoGeneracion": str(factura.codigo_generacion)
        }

        try:
            envio_resp = requests.post(envio_url, json=envio_json, headers=envio_headers, timeout=30)
            try:
                resp_data = envio_resp.json()
            except ValueError:
                resp_data = {"raw": envio_resp.text or ""}
        except requests.RequestException as e:
            return Response(
                {"error": "Error de conexión con Hacienda", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        fecha_actual = obtener_fecha_actual() or datetime.now(pytz.timezone('America/El_Salvador'))

        # 5) Procesar respuesta
        if envio_resp.status_code == 200 and resp_data.get("selloRecibido"):
            # Actualizar factura
            factura.sello_recepcion = resp_data["selloRecibido"]
            factura.recibido_mh = True
            # Combinar respuestas
            factura.json_original = {
                **factura.json_original,
                "jsonRespuestaMh": resp_data
            }
            factura.estado = True
            factura.fecha_modificacion = fecha_actual.date()
            factura.hora_modificacion = fecha_actual.time()
            
            #Enviar correo
            if factura:
                enviar_correo_individual_view(request, factura.id, None, None)
                factura.envio_correo = True
            factura.save()

            return Response(
                {"mensaje": "Factura enviada con éxito", "respuesta": resp_data},
                status=status.HTTP_200_OK
            )

        # Error de envío
        factura.estado = False
        factura.fecha_modificacion = fecha_actual.date()
        factura.hora_modificacion = fecha_actual.time()
        factura.save()

        return Response(
            {
                "error": "Error al enviar la factura",
                "status": envio_resp.status_code,
                "detalle": resp_data
            },
            status=envio_resp.status_code
        )

# ASIGNA EL MOTIVO CONTINGENCIA
class MotivoContingenciaAPIView(APIView):
    """
    Asigna el motivo de contingencia a un EventoContingencia
    vinculado a una factura y devuelve el objeto actualizado.
    """
    def get(self, request, format=None):
        factura_id = request.query_params.get("factura_id")
        motivo     = request.query_params.get("motivo")
        if not factura_id or motivo is None:
            return Response(
                {"error": "Se requieren 'factura_id' y 'motivo' en los parámetros"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el evento asociado al lote de esa factura
        evento = EventoContingencia.objects.filter(
            lotes_contingencia__factura_id=factura_id
        ).first()
        if not evento:
            return Response(
                {"error": "No se encontró un evento asociado a esta factura."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar motivo y marcas de tiempo
        ahora = obtener_fecha_actual()
        evento.motivo_contingencia = motivo
        evento.fecha_modificacion    = ahora.date()
        evento.hora_modificacion     = ahora.time()
        evento.save()

        # Responder con el nuevo estado del evento
        return Response({
            "mensaje": "Motivo de contingencia asignado con éxito",
            "evento": {
                "id": evento.id,
                "codigo_generacion": evento.codigo_generacion,
                "motivo_contingencia": evento.motivo_contingencia,
                "fecha_modificacion": evento.fecha_modificacion,
                "hora_modificacion": evento.hora_modificacion
            }
        }, status=status.HTTP_200_OK)



######################################################
# DASHBOARD
######################################################

class TotalesPorTipoDTE(generics.ListAPIView):
    def get(self, request):
        data = (
            FacturaElectronica.objects.values('tipo_dte', 'tipo_dte__codigo' ).annotate(total=Count('id')).filter(recibido_mh=True) 
        )
        return Response({"totales_por_tipo": list(data)})
 
class TotalVentasAPIView(generics.ListAPIView):
    def get(self, request):
        resultado = (
            FacturaElectronica.objects
          .filter(recibido_mh=True)
            .aggregate(total_ventas=Sum('total_pagar'))
        )
         
         # Devuelve 0 si no hay resultados
        total = resultado['total_ventas'] or 0
 
        return Response({"total_ventas": total})

class TopClientes(APIView):
    def get(self, request):
        data = (
            FacturaElectronica.objects
          .filter(recibido_mh=True)
            .values('dtereceptor', 'dtereceptor__nombre')  # Agrupamos por cliente
            .annotate(total_ventas=Sum('total_pagar'))  # Sumamos total_pagar por cliente
            .order_by('-total_ventas')[:3]  # Top 3
        )
 
        return Response({"clientes": list(data)})
 
class TopProductosAPIView(generics.ListAPIView):
    def get(self, request):
        data = (
            DetalleFactura.objects
          .values('producto', 'producto__descripcion')  # Agrupamos por producto
            .annotate(total_vendido=Sum('cantidad'))  # Sumar cantidades
             .order_by('-total_vendido')[:3]  # Top 3
        )
 
        return Response({"productos": list(data)})

#@csrf_exempt
class EnviarCorreoIndividualAPIView(APIView):
    def post(self, request, factura_id, format=None):
        # print(f"Inicio envio de correos: pdf: {archivo_pdf}, json: {archivo_json}")
        documento_electronico = get_object_or_404(FacturaElectronica, id=factura_id).order_by('id').first()
        receptor = get_object_or_404(Receptor_fe, id=documento_electronico.dtereceptor_id)
        emisor = get_object_or_404(Emisor_fe, id=documento_electronico.dteemisor_id)
        #Correo receptor principal: juniorfran@hotmail.es
        
        # 2) Leer parámetros del body
        archivo_pdf = request.data.get('archivo_pdf')
        archivo_json = request.data.get('archivo_json')

        # Si no vienen los archivos como parámetro, buscar en las rutas
        print("antes>", archivo_pdf)

        if not archivo_pdf:
            print("RUTA_COMPROBANTES_PDF", RUTA_COMPROBANTES_PDF)
            ruta_pdf = os.path.join(RUTA_COMPROBANTES_PDF.ruta_archivo, documento_electronico.tipo_dte.codigo, "pdf")
            archivo_pdf = os.path.join(ruta_pdf, f"{documento_electronico.codigo_generacion}.pdf")
            if not os.path.exists(archivo_pdf):
                print(f"Archivo PDF no encontrado en {archivo_pdf}")
                
                html_content = render_to_string('documentos/factura_consumidor/template_factura.html', {"factura": documento_electronico})
                #Guardar archivo pdf
                pdf_signed_path = f"{RUTA_COMPROBANTES_PDF.ruta_archivo}{documento_electronico.tipo_dte.codigo}/pdf/{documento_electronico.codigo_generacion}.pdf"
                print("guardar pdf: ", pdf_signed_path)
                with open(pdf_signed_path, "wb") as pdf_file:
                    pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)
                    
                if pisa_status.err:
                    print(f"Error al crear el PDF en {pdf_signed_path}")
                else:
                    print(f"PDF guardado exitosamente en {pdf_signed_path}")
        
        if not archivo_json:
            ruta_json = RUTA_COMPROBANTES_JSON.ruta_archivo
            archivo_json = os.path.join(ruta_json, f"{documento_electronico.numero_control}.json")
            if not os.path.exists(archivo_json):
                print(f"Archivo JSON no encontrado en {archivo_json}")
                messages.error(request, "Archivo JSON no encontrado.")
        print(f"json: {archivo_json} pdf: {archivo_pdf}")
        if documento_electronico:
            
            # Renderizar el HTML del mensaje del correo
            email_html_content = f"""
            <p>Estimado/a {receptor.nombre} reciba un cordial saludo.</p>
            <p>Le notificamos que se ha generado el documento electrónico. A continuación, los detalles principales:</p>
            <ul>
                <li><strong>Código de generación:</strong> {str(documento_electronico.codigo_generacion).upper()}</li>
                <li><strong>Fecha de emisión:</strong> {documento_electronico.fecha_emision.strftime("%Y-%m-%d")}</li>
                <li><strong>Hora de emisión:</strong> {documento_electronico.hora_emision.strftime('%H:%M:%S')}</li>
                <li><strong>Estado:</strong> {"Procesado" if documento_electronico.recibido_mh and documento_electronico.sello_recepcion else "Contingencia" if documento_electronico.contingencia else ""}</li>
            </ul>
            
            <p>Adjuntamos el documento en formato PDF y JSON para su respaldo.</p>
            <p>Si tiene alguna consulta, estamos a su disposición.</p>
            
            Consulte el documento electrónico aquí: https://admin.factura.gob.sv/consultaPublica
            <BR>
            <BR>
            
            Atentamente, <BR>
            {emisor.nombre_razon_social} <BR>
            {emisor.email}
            """
            
            # Crear el correo electrónico con formato HTML
            email = EmailMessage(
                subject="Documento Electrónico "+ documento_electronico.tipo_dte.descripcion,
                body=email_html_content,
                from_email=request.settings.EMAIL_HOST_USER_FE,
                to=[receptor.correo],
            )
            email.content_subtype = "html"  # Indicar que el contenido es HTML
            
            # Adjuntar el archivo PDF
            try:
                with open(archivo_pdf, 'rb') as pdf_file_to_attach:
                    email.attach(
                        f"Documento_Electrónico_{receptor.nombre}.pdf",
                        pdf_file_to_attach.read(),
                        'application/pdf'
                    )
            except Exception as e:
                print(f"Error al abrir el archivo PDF: {e}")
                return Response(
                {"error": "Error al abrir el archivo PDF", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            # Adjuntar el archivo JSON
            try:
                with open(archivo_json, 'rb') as json_file_to_attach:
                    email.attach(
                        f"Documento_Electrónico_{receptor.nombre}.json",
                        json_file_to_attach.read(),
                        'application/json'
                    )
            except Exception as e:
                return Response(
                {"error": "Error al abrir el archivo JSON:", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            # Enviar el correo
            try:
                email.send(fail_silently=False)
                documento_electronico.envio_correo = True
                documento_electronico.save()
                print(f"Correo enviado a {receptor.correo}")
                return Response(
                    {"mensaje": "El correo fue enviado exitosamente a"},
                    status=status.HTTP_200_OK
                    )
            except Exception as e:
                documento_electronico.envio_correo = False
                documento_electronico.save()
                print(f"Error al enviar el correo a {receptor.correo}: {e}")
                return Response(
                    {"error": "Error al enviar el correo", "detalle": str(e)},
                    status=status.HTTP_502_BAD_GATEWAY
                )
    #return redirect('detalle_factura', factura_id=factura_id)