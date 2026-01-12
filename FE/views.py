from zoneinfo import ZoneInfo
from django.forms import modelform_factory
import openpyxl
import requests
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import messages
from openpyxl import Workbook
from math import ceil

from django.db.models import F, Value
from django.db.models.functions import Greatest

#importaciones para actividad economica
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#IMPORTACIONES DE DTE
import os
import json
import re
import time
import uuid
import requests
import unicodedata

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from decimal import ROUND_HALF_UP, ConversionSyntax, Decimal, getcontext
from FE.utils import _get_emisor_for_user
from intracoe import settings
from .models import FacturaSujetoExcluidoElectronica, Token_data, Ambiente, CondicionOperacion, DetalleFactura, FacturaElectronica, Modelofacturacion, NumeroControl, Emisor_fe, ActividadEconomica,  Receptor_fe, Tipo_dte, TipoMoneda, TiposDocIDReceptor, Municipio, EventoInvalidacion, TipoInvalidacion, TiposEstablecimientos, Descuento, FormasPago, Plazo, TipoGeneracionDocumento, TipoContingencia, EventoContingencia, TipoTransmision, LoteContingencia, representanteEmisor
from INVENTARIO.models import Almacen, DetalleDevolucionVenta, DevolucionVenta, MovimientoInventario, NotaCredito, Producto, TipoItem, Tributo, TipoUnidadMedida
from .forms import EmisorForm, ExcelUploadForm, RepresentanteEmisorForm
from django.db import transaction
from django.utils import timezone
import pandas as pd
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.core import serializers
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from num2words import num2words
import pytz
from django.db.models import Count
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from AUTENTICACION.models import ConfiguracionServidor, UsuarioEmisor
#from weasyprint import HTML, CSS

from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist

import json
from django.core.serializers.json import DjangoJSONEncoder

try:
    FIRMADOR_URL = ConfiguracionServidor.objects.filter(clave="firmador").first()
except (OperationalError, ObjectDoesNotExist):
    FIRMADOR_URL = None

try:
    CERT_PATH = ConfiguracionServidor.objects.filter(clave="certificado").first()
    CERT_PATH = CERT_PATH.url_endpoint if CERT_PATH else None
except (OperationalError, ObjectDoesNotExist, AttributeError):
    CERT_PATH = None

    
def get_config(clave, campo="url", default=None):
    """
    Obtiene un valor de ConfiguracionServidor de forma segura.
    - clave: clave en la tabla (ej: 'firmador', 'certificado')
    - campo: 'url', 'url_endpoint', 'valor', etc.
    - default: valor por defecto si no existe
    """
    try:
        conf = ConfiguracionServidor.objects.filter(clave=clave).first()
        if conf:
            return getattr(conf, campo, default)
    except (AttributeError, OperationalError, ObjectDoesNotExist):
        return default
    return default

# Estos valores ya no rompen migraciones
#FIRMADOR_URL     = get_config("firmador", campo="url")
#DJANGO_SERVER_URL = get_config("server_url", campo="url")
#CERT_PATH        = get_config("certificado", campo="url_endpoint")
# HACIENDA_URL_TEST = get_config("hacienda_url_test", campo="url_endpoint")
# HACIENDA_URL_PROD = get_config("hacienda_url_prod", campo="url_endpoint")

# Constantes estáticas no cambian
SCHEMA_PATH_fe_fc_v1 = "FE/json_schemas/fe-fc-v1.json"

COD_CONSUMIDOR_FINAL = "01"
COD_CREDITO_FISCAL = "03"

try:
    VERSION_EVENTO_INVALIDACION = ConfiguracionServidor.objects.filter(clave="version_evento_invalidacion").first().valor
except (AttributeError, OperationalError, ObjectDoesNotExist):
    VERSION_EVENTO_INVALIDACION = None

try:
    AMBIENTE = Ambiente.objects.get(codigo="01")
except (OperationalError, ObjectDoesNotExist):
    AMBIENTE = None

COD_FACTURA_EXPORTACION = "11"
COD_SUJETO_EXCLUIDO = "14"
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
TIPO_TRANSMISION_CONTINGENCIA = 2

try:
    RUTA_COMPROBANTES_PDF = ConfiguracionServidor.objects.filter(clave="ruta_comprobantes_dte").first()
except (OperationalError, ObjectDoesNotExist):
    RUTA_COMPROBANTES_PDF = None

try:
    RUTA_COMPROBANTES_JSON = ConfiguracionServidor.objects.filter(clave="ruta_comprobante_json").first()
except (OperationalError, ObjectDoesNotExist):
    RUTA_COMPROBANTES_JSON = None

try:
    RUTA_JSON_FACTURA = ConfiguracionServidor.objects.filter(clave="json_factura").first()
except (OperationalError, ObjectDoesNotExist):
    RUTA_JSON_FACTURA = None

try:
    URL_AUTH = ConfiguracionServidor.objects.filter(clave="url_autenticacion").first()
except (OperationalError, ObjectDoesNotExist):
    URL_AUTH = None

try:
    HEADERS = ConfiguracionServidor.objects.filter(clave="headers").first()
except (OperationalError, ObjectDoesNotExist):
    HEADERS = None

try:
    CONTENT_TYPE = ConfiguracionServidor.objects.filter(clave="content_type").first()
except (OperationalError, ObjectDoesNotExist):
    CONTENT_TYPE = None

try:
    INVALIDAR_DTE_URL = ConfiguracionServidor.objects.filter(clave="url_invalidar_dte").first()
except (OperationalError, ObjectDoesNotExist):
    INVALIDAR_DTE_URL = None

try:
    VERSION_EVENTO_CONTINGENCIA = ConfiguracionServidor.objects.filter(clave="version_evento_contingencia").first()
except (OperationalError, ObjectDoesNotExist):
    VERSION_EVENTO_CONTINGENCIA = None

try:
    FACTURAS_FIRMADAS_URL = ConfiguracionServidor.objects.filter(clave="json_facturas_firmadas").first()
except (OperationalError, ObjectDoesNotExist):
    FACTURAS_FIRMADAS_URL = None

try:
    HACIENDA_CONTINGENCIA_URL = ConfiguracionServidor.objects.filter(clave="hacienda_contingencia_url").first()
except (OperationalError, ObjectDoesNotExist):
    HACIENDA_CONTINGENCIA_URL = None

try:
    USER_AGENT = ConfiguracionServidor.objects.filter(clave="user_agent").first()
except (OperationalError, ObjectDoesNotExist):
    USER_AGENT = None

try:
    SCHEMA_JSON = ConfiguracionServidor.objects.filter(clave="schema_json").first()
except (OperationalError, ObjectDoesNotExist):
    SCHEMA_JSON = None

try:
    CONSULTAR_DTE = ConfiguracionServidor.objects.filter(clave="consulta_dte").first()
except (OperationalError, ObjectDoesNotExist):
    CONSULTAR_DTE = None

try:
    EMAIL_HOST_FE = ConfiguracionServidor.objects.filter(clave="email_host_fe").first()
except (OperationalError, ObjectDoesNotExist):
    EMAIL_HOST_FE = None

try:
    MONEDA_USD = TipoMoneda.objects.get(codigo="USD")
except (OperationalError, ObjectDoesNotExist):
    MONEDA_USD = None

try:
    UNI_MEDIDA_99 = TipoUnidadMedida.objects.get(codigo="99")
except (OperationalError, ObjectDoesNotExist):
    UNI_MEDIDA_99 = None

formas_pago = []
documentos_relacionados = []
tipo_dte_doc_relacionar = None
documento_relacionado = False
productos_ids_r = []
cantidades_prod_r = []
descuentos_r = []
tipo_documento_dte = "01"
productos_inventario = None


@login_required
def facturacion_generar_home(request):
    """
    Pantalla inicial para elegir el tipo de DTE a generar (Factura, CCF, Exportación, …).
    Usa la plantilla: templates/facturacion/generar/home.html
    """
    return render(request, 'facturacion/generar/home.html')

@login_required
def facturacion_correcciones_home(request):
    """
    Pantalla inicial para elegir el tipo de corrección (Nota de crédito o Nota de débito).
    Usa la plantilla: templates/facturacion/correcciones/home.html
    """
    return render(request, 'facturacion/correcciones/home.html')

@login_required
def facturacion_generar_home(request):
    """
    Pantalla inicial para elegir el tipo de DTE a generar (Factura, CCF, Exportación, …).
    Usa la plantilla: templates/facturacion/generar/home.html
    """
    return render(request, 'facturacion/generar/home.html')

#vistas para actividad economica
def cargar_actividades(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                # Carga el archivo Excel especificando índices de columna
                data = pd.read_excel(excel_file, usecols="A:B", header=None, names=['codigo', 'descripcion'])
                
                # Comprueba que los datos no estén vacíos
                if data.empty:
                    messages.error(request, 'El archivo está vacío.')
                    return render(request, 'actividad_economica/cargar_actividades.html', {'form': form})
                
                # Itera sobre cada fila y actualiza o crea entradas en la base de datos
                for _, row in data.iterrows():
                    ActividadEconomica.objects.update_or_create(
                        codigo=row['codigo'],
                        defaults={'descripcion': row['descripcion']}
                    )
                messages.success(request, 'Actividades económicas cargadas con éxito.')
                return redirect('actividad_economica_list')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
        else:
            messages.error(request, 'Por favor, verifica que el archivo esté en el formato correcto.')
    else:
        form = ExcelUploadForm()
    return render(request, 'actividad_economica/cargar_actividades.html', {'form': form})

def actividad_economica_list(request):
    actividades = ActividadEconomica.objects.all()
    # Paginación
    paginator = Paginator(actividades, 10)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'actividad_economica/list.html', {'actividades': page_obj})

# Detalle de una Actividad Económica
class ActividadEconomicaDetailView(DetailView):
    model = ActividadEconomica
    context_object_name = 'actividad'
    template_name = 'actividad_economica/detail.html'

# Crear una nueva Actividad Económica
class ActividadEconomicaCreateView(CreateView):
    model = ActividadEconomica
    fields = ['codigo', 'descripcion']
    template_name = 'actividad_economica/create.html'
    success_url = reverse_lazy('actividad_economica_list')

# Actualizar una Actividad Económica existente
class ActividadEconomicaUpdateView(UpdateView):
    model = ActividadEconomica
    fields = ['codigo', 'descripcion']
    template_name = 'actividad_economica/update.html'
    success_url = reverse_lazy('actividad_economica_list')

# Eliminar una Actividad Económica
class ActividadEconomicaDeleteView(DeleteView):
    model = ActividadEconomica
    context_object_name = 'actividad'
    template_name = 'actividad_economica/delete.html'
    success_url = reverse_lazy('actividad_economica_list')

def crear_tipo_dte(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        version = request.POST.get("version")

        if not codigo or not descripcion or not version:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

        tipo, created = Tipo_dte.objects.get_or_create(
            codigo=codigo,
            defaults={"descripcion": descripcion, "version": version}
        )
        if not created:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": f"El Tipo DTE {codigo} ya existe."}, status=400)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "id": tipo.id,
                "codigo": tipo.codigo,
                "descripcion": tipo.descripcion,
                "version": tipo.version,
            })

    tipos = Tipo_dte.objects.all()
    return render(request, "crear_tipo_dte.html", {"tipos": tipos})

########################################################################################################

schema_path = "FE/json_schemas/fe-fc-v1.json"

if SCHEMA_JSON and SCHEMA_JSON.url:
    try:
        with open(SCHEMA_JSON.url, "r", encoding="utf-8") as schema_file:
            factura_schema = json.load(schema_file)

        required_fields = factura_schema.get("required", [])
        properties = factura_schema.get("properties", {})

        form_fields = []
        for field in required_fields:
            field_type = properties.get(field, {}).get("type", "text")
            form_fields.append({"name": field, "type": field_type})

    except (FileNotFoundError, json.JSONDecodeError):
        factura_schema = {}
        form_fields = []

else:
    factura_schema = {}
    form_fields = []


##################################################################################################

def obtener_receptor(request, receptor_id):
    try:
        receptor = Receptor_fe.objects.get(id=receptor_id)
        data = {
            "tipo_documento": receptor.tipo_documento,
            "num_documento": receptor.num_documento,
            "nrc": receptor.nrc,
            "nombre": receptor.nombre,
            "direccion": receptor.direccion,
            "telefono": receptor.telefono,
            "correo": receptor.correo
        }
        print("nrc: ",receptor.nrc)
        return JsonResponse(data)
    except Receptor_fe.DoesNotExist:
        return JsonResponse({"error": "Receptor no encontrado"}, status=404)
    
# VISTA PARA OBTENER EL DOCUMENTO RELACIONADO Y MOSTRARLO EN MI TABLA

def obtener_factura_por_codigo(request):
    global documento_relacionado
    documento_relacionado = True
    global productos_ids_r 
    global cantidades_prod_r 
    global descuentos_r
    codigo_generacion = request.GET.get("codigo_generacion")
    print("-Codigo de generacion a relacionar: ", codigo_generacion)
    
    try:
        factura = FacturaElectronica.objects.get(codigo_generacion=codigo_generacion)
        #Verificar si el numero de documento a relacionar ya esta asociado a otro dte
        detalle = DetalleFactura.objects.filter(documento_relacionado=codigo_generacion)
        print("Detalle encontrado: ", detalle, "factura encontrada: ", factura)
        
        if detalle.exists():#Verificar que detalle no sea null ni vacio
            print("-El documento ya fue relacionado")
            return JsonResponse({"error": "El documento ya tiene una relación con otro Documento Tributario Electrónico." })
        else:
            if factura is not None and factura.estado and factura.sello_recepcion is not None and factura.sello_recepcion !="":
                detalles_list = []
                # Recorre cada detalle asociado a la factura usando el related_name "detalles"
                for detalle in factura.detalles.all():
                    print("-Recorrer detalles de la factura- cantidad: ", detalle.cantidad)
                    # Se asume que el precio_unitario incluye IVA y se calcula el precio neto e IVA unitario
                    neto_unitario = detalle.precio_unitario #/ Decimal('1.13')
                    iva_unitario = detalle.precio_unitario - neto_unitario
                    total_neto = neto_unitario * detalle.cantidad
                    total_iva = iva_unitario * detalle.cantidad
                    total_incl = detalle.precio_unitario * detalle.cantidad

                    detalles_list.append({
                        "producto_id": detalle.producto.id,
                        "producto": f"{detalle.producto.codigo} - {detalle.producto.descripcion}",
                        "cantidad": detalle.cantidad,
                        "precio_unitario": str(detalle.precio_unitario),
                        "neto_unitario": str(round(neto_unitario, 2)),
                        "iva_unitario": str(round(iva_unitario, 2)),
                        "total_neto": str(round(total_neto, 2)),
                        "total_iva": str(round(total_iva, 2)),
                        "total_incl": str(round(total_incl, 2)),
                        "descuento": str(detalle.descuento.porcentaje) if detalle.descuento else "",
                        "numero_documenmto_relacionado": str(factura.codigo_generacion)
                    })
                    id_productos=detalle.producto.id
                    
                    productos_ids_r.append(detalle.producto.id)
                    cantidades_prod_r.append(detalle.cantidad)
                    descuentos_r.append(detalle.descuento.porcentaje)
                    print(f"1. id prods relacionados: {productos_ids_r}, cantidades relacionadas: {cantidades_prod_r}, docs relacionados: {documentos_relacionados}, descuento seleccionado {descuentos_r} ")
                
                print("detalle: ",detalles_list)
                
                data = {
                    "codigo_generacion": str(factura.codigo_generacion),
                    "tipo_documento": factura.tipo_dte.descripcion if factura.tipo_dte else "",
                    "num_documento": factura.numero_control,
                    "fecha_emision": factura.fecha_emision.strftime("%Y-%m-%d"),
                    "fecha_vencimiento": factura.fecha_emision.strftime("%Y-%m-%d") if factura.fecha_emision else "",
                    "total": str(factura.total_pagar),
                    "descuento_global": factura.por_descuento,
                    "descuento_gravado": factura.descuento_gravado,
                    "monto_descuento": factura.total_descuento,
                    "total_gravadas": factura.total_gravadas,
                    "detalles": detalles_list  # Aquí se incluye el detalle de los productos
                }
                return JsonResponse(data)
    except FacturaElectronica.DoesNotExist:
        return JsonResponse({"error": "Factura no encontrada"}, status=404)


#########################################################################################################
# GENERACION DE DOCUMENTOS ELECTRONICOS
#########################################################################################################

# Función auxiliar para convertir números a letras (stub, cámbiala según tus necesidades)
porcentaje_descuento = Decimal("0.00")

def num_to_letras(numero):
    """
    Convierte un número a su representación en palabras en español,
    en el formato: "Diecinueve con 66/100 USD"
    """
    try:
        # Redondea a dos decimales
        numero = round(numero, 2)
        entero = int(numero)
        # Calcula la parte decimal (por ejemplo, 19.66 -> 66)
        decimales = int(round((numero - entero) * 100))
        # Convertir la parte entera a palabras
        palabras = num2words(entero, lang='es').capitalize()
        return f"{palabras} con {decimales:02d}/100 USD"
    except Exception as e:
        return "Conversión no disponible"

@login_required
def obtener_numero_control_ajax(request):
    global tipo_documento_dte
    global productos_inventario

    tipo_dte = request.GET.get('tipo_dte', '01')  # por defecto Factura

    # Guardar tipo en global
    tipo_documento_dte = tipo_dte
    productos_inventario = Producto

    # ✅ obtener emisor del usuario logueado
    emisor = _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({'error': 'No hay emisor configurado'}, status=400)

    estab = emisor.codigo_establecimiento or "0000"
    pv = emisor.codigo_punto_venta or "0001"

    print(f"Inicializando DTE Vista: tipo={tipo_dte}, estab={estab}, pv={pv}")

    # ✅ pasar estab y pv a la preview
    nuevo_numero = NumeroControl.preview_numero_control(tipo_dte, estab=estab, pv=pv)

    print("vista numero de control:", nuevo_numero)
    return JsonResponse({'numero_control': nuevo_numero})

def factura_list(request):
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
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    dtelist = paginator.get_page(page_number)
    
    # Obtener todos los tipos de factura para el select del filtro
    tipos_dte = Tipo_dte.objects.all()
    
    context = {
        'dtelist': dtelist,
        'tipos_dte': tipos_dte,
    }
    return render(request, 'documentos/dte_list.html', context)

@csrf_exempt
def export_facturas_excel(request):
    # Calcular el límite de las últimas 24 horas
    limite = datetime.now() - timedelta(hours=24)
    
    # Consultar las facturas emitidas antes de ese límite y sin evento de invalidación
    facturas = FacturaElectronica.objects.filter(
        fecha_emision__lt=limite,
        dte_invalidacion__isnull=True
    )
    
    # Crear el libro y la hoja de cálculo
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facturas Emitidas"
    
    # Definir la cabecera (ajusta los campos según tu modelo)
    cabecera = ["ID", "Número de Control", "Sello de Recepcion", "Fecha de Emisión", "Total a Pagar", "IVA"]
    ws.append(cabecera)
    
    # Recorrer las facturas y escribir los datos
    for factura in facturas:
        fila = [
            factura.id,
            factura.numero_control,
            factura.sello_recepcion,
            factura.fecha_emision.strftime("%Y-%m-%d %H:%M:%S") if factura.fecha_emision else "",
            factura.total_pagar,
            factura.total_iva
        ]
        print(factura.sello_recepcion)
        ws.append(fila)
    
    # Preparar la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="facturas_emitidas.xlsx"'
    wb.save(response)
    return response

def obtener_listado_productos_view(request):
    global tipo_documento_dte
    if "generar_ajuste" in request.path.lower():
        tipo_documento_dte = request.GET.get('tipo_documento_dte', '05')
    else:
        tipo_documento_dte = request.GET.get('tipo_documento_dte', '01')
        
    tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_documento_dte)
    productos = Producto.objects.all()
    tipoItems = TipoItem.objects.all()
    descuentos = Descuento.objects.all()
    
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
    # Comprobar si la solicitud es AJAX mediante el encabezado X-Requested-With
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'generar_dte.html', 
                    {
                        'productos': productos, 
                        'tipoItems': tipoItems,
                        'descuentos': descuentos
                    })

    # Si no es una solicitud AJAX, se devuelve la página completa
    context = {
        'productos': productos,
        'tipoItems': tipoItems,
        'descuentos': descuentos
    }
    return render(request, 'generar_dte.html', context)

def get_productos_para_tipo(request, tipo_codigo):
    try:
        tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_codigo)
    except Tipo_dte.DoesNotExist:
        # Siempre devolvemos dos valores
        messages.warning(
            request,
            f"No existe un Tipo DTE con código {tipo_codigo}. Por favor crea uno antes de continuar."
        )
        return [], None  # 👈 SIEMPRE dos valores

    productos = Producto.objects.all()
    return list(productos), tipo_dte_obj

# --------------------------------------------------------------------
# generar_factura_view
# --------------------------------------------------------------------
# ---------- Helpers ----------
def _dec(x, default="0.00"):
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal(default)

def _bool_from_str(s):
    return str(s).lower() in ("1", "true", "on", "yes")

def q2(d):  # 2 decimales HALF_UP
    return Decimal(d).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@csrf_exempt
@transaction.atomic
def generar_factura_view(request):
    req_id = str(uuid.uuid4())[:8]
    print("DTE: ====== INICIO generar_factura_view ======")
    print("DTE: method=", request.method, " content_type=", request.content_type)
    
    
    if request.method == 'GET':
        prefill = None
        if request.GET.get("from_cart") == "1":
            prefill = request.session.pop("facturacion_prefill", None)
            request.session.modified = True
            print("DTE: prefill recuperado =", prefill)

        # tipo_dte = globals().get('tipo_documento_dte', '01')
        tipo_dte = request.GET.get("tipo_documento_dte", '01')
        
        
        
        print("DTE: GET tipo_dte=", tipo_dte)
        if not tipo_dte:
            messages.error(request, "No se ha especificado el tipo de documento.")
            return redirect('crear_tipo_dte')

        productos, tipo_dte_obj = get_productos_para_tipo(request, tipo_dte)
        if not tipo_dte_obj:
            return redirect("crear_tipo_dte")
        print(f"DTE: Tipo DTE encontrado: {tipo_dte_obj.codigo} - {tipo_dte_obj.descripcion}")

        emisor_obj = _get_emisor_for_user(request.user, estricto=False)
        nuevo_numero = NumeroControl.preview_numero_control(
            tipo_dte,
            estab=(emisor_obj.codigo_establecimiento or "0000") if emisor_obj else "0000",
            pv=(emisor_obj.codigo_punto_venta or "0001") if emisor_obj else "0001",
        )
        
        context = {
            "prefill_factura": prefill,
            "numero_control": nuevo_numero,
            "codigo_generacion": str(uuid.uuid4()).upper(),
            "fecha_generacion": timezone.now().date(),
            "hora_generacion": timezone.now().strftime('%H:%M:%S'),
            "emisor": ({
                "nit": emisor_obj.nit,
                "nombre_razon_social": emisor_obj.nombre_razon_social,
                "direccion_comercial": emisor_obj.direccion_comercial,
                "telefono": emisor_obj.telefono,
                "email": emisor_obj.email,
                "imprime_termica": emisor_obj.imprime_termica,
            } if emisor_obj else None),
            "receptores": list(Receptor_fe.objects.values("id", "num_documento", "nombre")),
            "productos": productos,
            "tipo_dte_obj": tipo_dte_obj,
            "tipooperaciones": CondicionOperacion.objects.all(),
            "tipoDocumentos": Tipo_dte.objects.exclude(Q(codigo=COD_NOTA_CREDITO) | Q(codigo=COD_NOTA_DEBITO)),
            "tipoItems": TipoItem.objects.all(),
            "descuentos": Descuento.objects.all(),
            "formasPago": FormasPago.objects.all(),
            "tipoGenDocumentos": TipoGeneracionDocumento.objects.all(),
            "prefill_factura": json.dumps(prefill, ensure_ascii=False) if prefill else None,
            "dte_select": tipo_dte
        }
        print("DTE: Renderizar template generar_dte.html")
        print(f"DTE: Renderizar template generar_dte.html {context}")
        
        return render(request, "generar_dte.html", context)

    elif request.method == 'POST':
        
        # ---------- Parse body (JSON o form) ----------
        is_json = (request.content_type or '').startswith('application/json')
        if is_json:
            raw = request.body.decode('utf-8') if isinstance(request.body, (bytes, bytearray)) else (request.body or '')
            print("DTE: POST JSON len=", len(raw))
            if len(raw) < 300:
                print("DTE: POST JSON preview=", raw)
            try:
                data = json.loads(raw or '{}')
            except json.JSONDecodeError as e:
                print("DTE: JSONDecodeError:", e)
                return JsonResponse({'error': 'Cuerpo JSON inválido.'}, status=400)
        else:
            P = request.POST
            print("DTE: POST FORM keys=", list(P.keys()))
            def _g(name, default=''):
                return P.get(name, default)
            def _gl(name):
                return P.getlist(name)

            data = {
                'numero_control': _g('numero_control',''),
                'codigo_generacion': _g('codigo_generacion',''),
                'receptor_id': _g('receptor_id') or None,
                'condicion_operacion': _g('condicion_operacion') or 1,
                'tipo_documento_seleccionado': _g('tipo_documento_seleccionado') or '01',
                'observaciones': _g('observaciones',''),

                'retencion_iva': _bool_from_str(_g('ret_iva_sw','')),
                'porcentaje_retencion_iva': _g('ret_iva_pct','0'),
                'retencion_renta': _bool_from_str(_g('ret_renta_sw','')),
                'porcentaje_retencion_renta': _g('ret_renta_pct','0'),

                'descuento_global_input': _g('descuento_global_input','0'),
                'descuento_gravado': _g('descuento_gravado','0'),
                'monto_descuento': _g('monto_descuento','0'),
                'saldo_favor_input': _g('saldo_favor_input','0'),
                'no_gravado': _bool_from_str(_g('no_gravado','')),

                # Ítems del template (hidden)
                'productos_ids': _gl('item_id[]'),
                'cantidades': _gl('item_cantidad[]'),
                'precios': _gl('item_precio[]'),
                'descuento_select': _gl('item_descuento[]'),
                'iva_linea': _gl('item_iva[]'),

                # Pago
                'metodo_pago': _g('metodo_pago','EFECTIVO'),
                'dias_credito': _g('dias_credito') or None,
                'fecha_vencimiento': _g('fecha_vencimiento') or None,
                'notas_pago': _g('notas_pago',''),
                'formas_pago_id': _gl('formas_pago_id[]'),
            }

        # Defaults exportación (por compatibilidad)
        data.setdefault("flete_exportacion", "0.00")
        data.setdefault("seguro_exportacion", "0.00")
        data.setdefault("otros_gastos_exportacion", "0.00")

        try:
            print("DTE: ==== INICIO PROCESO FACTURA ====")
            items_permitidos = 2000

            tipo_dte = data.get("tipo_documento_seleccionado") or "01"
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            print("DTE: tipo_dte=", tipo_dte)

            emisor_obj = _get_emisor_for_user(request.user, estricto=False)
            if not emisor_obj:
                return JsonResponse({"error": "No hay emisor asignado a tu usuario. Configúralo antes de facturar."}, status=400)

            estab = emisor_obj.codigo_establecimiento or "0000"
            pv    = emisor_obj.codigo_punto_venta or "0001"

            numero_control = NumeroControl.obtener_numero_control(tipo_dte, estab=estab, pv=pv)
            codigo_generacion = data.get('codigo_generacion') or str(uuid.uuid4()).upper()
            print("DTE: numero_control asignado=", numero_control)
            print("DTE: codigo_generacion=", codigo_generacion)

            receptor_id = data.get('receptor_id')
            print("DTE: receptor_id=", receptor_id)
            if not receptor_id:
                return JsonResponse({"error": "Seleccione un cliente (receptor)."}, status=400)
            try:
                receptor = Receptor_fe.objects.get(id=receptor_id)
            except Receptor_fe.DoesNotExist:
                return JsonResponse({"error": "Receptor no encontrado."}, status=404)

            observaciones = data.get('observaciones', '')
            print("DTE: observaciones.len=", len(observaciones))

            tipooperacion_id = data.get("condicion_operacion", 1)
            porcentaje_retencion_iva = _dec(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = bool(data.get("retencion_iva", False))
            porcentaje_retencion_renta = _dec(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = bool(data.get("retencion_renta", False))
            print(f"DTE: ret_iva={retencion_iva} pct={porcentaje_retencion_iva}  ret_renta={retencion_renta} pct={porcentaje_retencion_renta}")

            descuento_global = _dec(data.get("descuento_global_input", "0"))  # %
            base_imponible_checkbox = bool(data.get("no_gravado", False))
            saldo_favor_in = data.get("saldo_favor_input", "0")
            saldo_favor = _dec(saldo_favor_in or "0")
            if saldo_favor > Decimal("0.00"):
                saldo_favor = saldo_favor * Decimal("-1")
            else:
                saldo_favor = Decimal("0.00")
            print("DTE: descuento_global%=", descuento_global, " base_imponible=", base_imponible_checkbox, " saldo_favor=", saldo_favor)

            # Ítems del form
            productos_ids = data.get('productos_ids') or []
            cantidades    = data.get('cantidades') or []
            precios       = data.get('precios') or []
            descs         = data.get('descuento_select') or []
            ivas_linea    = data.get('iva_linea') or []
            print("DTE: items recibidos n=", len(productos_ids))
            print("DTE: ids=", productos_ids)
            print("DTE: qty=", cantidades)
            print("DTE: pu =", precios)
            print("DTE: des=", descs)
            print("DTE: iva=", ivas_linea)

            if not productos_ids:
                return JsonResponse({"error": "Debes agregar al menos un producto."}, status=400)

            tipomodelo_obj = Modelofacturacion.objects.get(codigo="1")
            tipotransmision_obj = TipoTransmision.objects.get(codigo="1")
            tipooperacion_obj = CondicionOperacion.objects.get(id=tipooperacion_id) if tipooperacion_id else None
            tipo_moneda_obj = MONEDA_USD

            factura = FacturaElectronica.objects.create(
                version="1.0",
                tipo_dte=tipo_dte_obj,
                numero_control=numero_control,
                codigo_generacion=codigo_generacion,
                tipomodelo=tipomodelo_obj,
                tipocontingencia=None,
                motivocontin=None,
                tipomoneda=tipo_moneda_obj,
                dteemisor=emisor_obj,
                dtereceptor=receptor,
                json_original={},
                firmado=False,
                base_imponible=base_imponible_checkbox,
                tipotransmision=tipotransmision_obj,
                flete_exportacion=Decimal("0.00"),
                seguro_exportacion=Decimal("0.00"),
            )
            print("DTE: Factura creada id=", factura.id)

            # ---------- Normalizar filas ----------
            rows = []
            n = len(productos_ids)
            for i in range(n):
                pid = (productos_ids[i] or "").strip()
                if not pid:
                    print(f"DTE: fila {i}: sin producto, se omite")
                    continue
                try:
                    producto = Producto.objects.get(id=pid)
                except Producto.DoesNotExist:
                    print(f"DTE: fila {i}: producto id={pid} no existe, se omite")
                    continue

                qty = int(cantidades[i]) if i < len(cantidades) and str(cantidades[i]).strip() else 1
                pu  = _dec(precios[i])   if i < len(precios)    and str(precios[i]).strip()   else _dec(producto.preunitario or "0")
                iva_on = _bool_from_str(ivas_linea[i]) if i < len(ivas_linea) else False
                desc_pct = _dec(descs[i]) if i < len(descs) and str(descs[i]).strip() else Decimal("0")
                if desc_pct < 0: desc_pct = Decimal("0")
                if desc_pct > 100: desc_pct = Decimal("100")

                tipo_item_linea = producto.tipo_item or (TipoItem.objects.filter(codigo="1").first() or TipoItem.objects.first())
                if not tipo_item_linea:
                    return JsonResponse({"error": f"No hay Tipo de Ítem para el producto {producto.codigo} y no existe default."}, status=400)

                if base_imponible_checkbox or (str(tipo_item_linea.codigo) == str(COD_TIPO_ITEM_OTROS)):
                    try:
                        um = UNI_MEDIDA_99
                    except NameError:
                        um = TipoUnidadMedida.objects.get(codigo="99")
                    qty = 1
                else:
                    um = producto.unidad_medida or TipoUnidadMedida.objects.get(codigo="99")

                rows.append({
                    "producto": producto,
                    "qty": qty,
                    "pu": pu,                 # NETO
                    "iva_on": iva_on,
                    "desc_pct": desc_pct,     # %
                    "tipo_item": tipo_item_linea,
                    "um": um,
                })
                print(f"DTE: row+  pid={producto.id} cod={producto.codigo} qty={qty} pu={pu} iva={iva_on} desc%={desc_pct} um={um.codigo} tipoItem={tipo_item_linea.codigo}")

            if not rows:
                return JsonResponse({"error": "No se pudo construir el detalle de la factura."}, status=400)

            # Merge duplicados
            before_merge = len(rows)
            merged = {}
            for r in rows:
                key = (r["producto"].id, str(q2(r["pu"])), r["iva_on"], str(q2(r["desc_pct"])), r["um"].codigo, r["tipo_item"].codigo)
                if key not in merged:
                    merged[key] = r.copy()
                else:
                    merged[key]["qty"] += r["qty"]
            rows = list(merged.values())
            print(f"DTE: merge items antes={before_merge} despues={len(rows)}")

            if len(rows) > items_permitidos:
                return JsonResponse({"error": f"Cantidad máxima de ítems permitidos: {items_permitidos}"}, status=400)

            # ---------- Cálculo por línea (y guardar detalle) ----------
            total_gravada = Decimal("0.00")
            total_iva = Decimal("0.00")
            sub_total = Decimal("0.00")
            cuerpo_documento = []

            is_ccf = (str(tipo_dte_obj.codigo) == "03")
            is_fe  = (str(tipo_dte_obj.codigo) == "01")

            for idx, r in enumerate(rows, start=1):
                producto = r["producto"]
                cantidad = r["qty"]
                precio_unit = r["pu"]              # NETO
                aplica_iva = r["iva_on"]
                desc_pct = r["desc_pct"]           # %
                tipo_item_linea = r["tipo_item"]
                um = r["um"]

                base = (precio_unit * cantidad)
                monto_desc = q2(base * (desc_pct / Decimal("100"))) if desc_pct > 0 else Decimal("0.00")
                gravada = base - monto_desc
                iva_line = q2(gravada * Decimal("0.13")) if aplica_iva else Decimal("0.00")
                total_line = gravada + iva_line

                print(f"DTE: calc[{idx}] cod={producto.codigo} qty={cantidad} pu={precio_unit} base={q2(base)} desc={monto_desc} gravada={q2(gravada)} iva={iva_line} total={q2(total_line)}")

                # Guardar detalle BD
                desc_obj = None
                if desc_pct > 0:
                    desc_obj = Descuento.objects.filter(porcentaje=desc_pct).first()

                DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    unidad_medida=um,
                    precio_unitario=q2(precio_unit),
                    descuento=desc_obj,
                    tiene_descuento=bool(desc_pct > 0),
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=q2(gravada),
                    pre_sug_venta=q2(precio_unit),
                    no_gravado=Decimal("0.00"),
                    saldo_favor=saldo_favor
                )

                total_gravada += q2(gravada)
                total_iva += q2(iva_line)
                sub_total += q2(gravada)

                # tipoItem válido (1..4)
                try:
                    cod_tipo_item_raw = int(tipo_item_linea.codigo)
                except Exception:
                    cod_tipo_item_raw = 1
                cod_tipo_item = cod_tipo_item_raw if cod_tipo_item_raw in (1, 2, 3, 4) else 1

                # Reglas tributos por ítem
                codTributo = None
                tributos   = ["20"] if (aplica_iva and gravada > 0) else None
                if is_ccf:
                    # En CCF, codTributo a nivel ítem debe ir None
                    codTributo = None
                else:
                    # En FE puedes dejar codTributo=None y tributos=["20"] si aplica
                    codTributo = None

                cuerpo = {
                    "numItem": idx,
                    "tipoItem": cod_tipo_item,
                    "numeroDocumento": None,
                    "codigo": str(producto.codigo),
                    "codTributo": codTributo,            # None en CCF
                    "descripcion": str(producto.descripcion),
                    "cantidad": float(cantidad),
                    "uniMedida": int(um.codigo) if str(um.codigo).isdigit() else 59,
                    "precioUni": float(q2(precio_unit)), # NETO
                    "montoDescu": float(q2(monto_desc)),
                    "ventaNoSuj": 0.0,
                    "ventaExenta": 0.0,
                    "ventaGravada": float(q2(gravada)),
                    "tributos": tributos,                 # ["20"] si gravada; None si no
                    "psv": float(q2(precio_unit)),
                    "noGravado": 0.0,
                }
                if is_fe:
                    cuerpo["ivaItem"] = float(q2(iva_line))

                cuerpo_documento.append(cuerpo)

            print(f"DTE: ACUM sub_total={sub_total} total_iva={total_iva} total_gravada={total_gravada}")

            # ---------- Retenciones ----------
            DecimalRetIva = Decimal("0.00")
            DecimalRetRenta = Decimal("0.00")
            if retencion_iva and porcentaje_retencion_iva > 0:
                for r in rows:
                    base_linea = q2((r["pu"] * r["qty"]) * (Decimal("1") - (r["desc_pct"] / Decimal("100"))))
                    ret = q2(base_linea * (porcentaje_retencion_iva / Decimal("100")))
                    DecimalRetIva += ret
                print("DTE: ret IVA =", DecimalRetIva)

            if retencion_renta and porcentaje_retencion_renta > 0:
                for r in rows:
                    base_linea = q2((r["pu"] * r["qty"]) * (Decimal("1") - (r["desc_pct"] / Decimal("100"))))
                    ret = q2(base_linea * (porcentaje_retencion_renta / Decimal("100")))
                    DecimalRetRenta += ret
                print("DTE: ret Renta =", DecimalRetRenta)

            # Totales finales
            total_operaciones = q2(sub_total)  # solo bases gravadas
            total_pagar_final = q2(total_operaciones + total_iva - DecimalRetIva - DecimalRetRenta)
            print(f"DTE: RESUMEN total_operaciones={total_operaciones} total_iva={total_iva} retIVA={DecimalRetIva} retRenta={DecimalRetRenta} -> total_pagar={total_pagar_final}")

            # Relacionados
            tipo_doc_relacionar = data.get("documento_seleccionado", None)
            documento_relacionado = data.get("documento_relacionado", None)
            if tipo_doc_relacionar == COD_DOCUMENTO_RELACIONADO_NO_SELEC:
                tipo_doc_relacionar, documento_relacionado = None, None

            # ---------- Actualiza Factura ----------
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = q2(total_gravada)
            factura.sub_total_ventas = q2(total_gravada)
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = float(Decimal("0.00"))
            factura.por_descuento = q2(descuento_global)
            factura.total_descuento = float(Decimal("0.00"))
            factura.sub_total = q2(sub_total)
            factura.iva_retenido = float(DecimalRetIva)
            factura.retencion_renta = float(DecimalRetRenta)
            factura.total_operaciones = float(total_operaciones)
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = float(total_pagar_final)
            factura.total_letras = num_to_letras(total_pagar_final)
            factura.total_iva = float(q2(total_iva))
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = float(Decimal("0.00"))
            factura.tipo_documento_relacionar = tipo_doc_relacionar
            factura.documento_relacionado = documento_relacionado
            factura.save()
            print("DTE: Factura actualizada totales OK")

            # ==== VARIABLES PARA generar_json ====
            ambiente_obj = AMBIENTE
            emisor = emisor_obj

            try:
                iva_item_total = sum(
                    (d.iva_item or Decimal("0.00")) for d in factura.detalles.all()
                ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            except Exception:
                iva_item_total = Decimal(str(factura.total_iva or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            nombre_responsable = data.get("nombre_responsable")
            documento_responsable = data.get("documento_responsable")
            formas_pago = None
            documentos_relacionados = []
            contingencia = False

            # ---------- Generar JSON ----------
            factura_json = generar_json(
                ambiente_obj,
                tipo_dte_obj,
                factura,
                emisor,
                receptor,
                cuerpo_documento,
                observaciones,
                iva_item_total,
                base_imponible_checkbox,
                saldo_favor,
                documentos_relacionados,
                contingencia,
                total_gravada,
                nombre_responsable,
                documento_responsable,
                formas_pago
            )

            # ==== NORMALIZAR RESUMEN.pagos (CAT-018) ===
            res = factura_json.setdefault('resumen', {})
            _total_pagar = Decimal(str(res.get('totalPagar', factura.total_pagar or 0))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            metodo_ui = (data.get('metodo_pago') or 'EFECTIVO').strip().upper()
            fp = FormasPago.objects.filter(Q(descripcion__iexact=metodo_ui) | Q(codigo__iexact=metodo_ui)).first()
            if fp and str(fp.codigo).strip():
                try:
                    codigo_pago = f"{int(fp.codigo):02d}"
                except Exception:
                    codigo_pago = str(fp.codigo).zfill(2)
            else:
                ALIAS = {'EFECTIVO': '01', 'TARJETA': '03', 'TRANSFERENCIA': '04', 'CREDITO': '08'}
                codigo_pago = ALIAS.get(metodo_ui, '01')

            pago = {
                "codigo": codigo_pago,
                "montoPago": float(_total_pagar),
            }
            ref = (data.get('num_pago_ref') or data.get('notas_pago') or '').strip()
            pago["referencia"] = ref if ref else None

            cond_op = str(data.get('condicion_operacion') or getattr(factura.condicion_operacion, 'codigo', '1')).strip()
            if cond_op == '2' or codigo_pago == '08':
                raw_dias = data.get('dias_credito')
                try:
                    dias = int(raw_dias)
                except (TypeError, ValueError):
                    dias = 0
                if dias >= 365 and dias % 365 == 0:
                    periodo = '03'; cantidad = min(dias // 365, 99)
                elif dias >= 30 and dias % 30 == 0:
                    periodo = '02'; cantidad = min(dias // 30, 99)
                else:
                    periodo = '01'; cantidad = min(max(dias, 0), 99)
                pago["periodo"] = periodo
                pago["plazo"] = str(cantidad).zfill(2)
            else:
                pago["periodo"] = None
                pago["plazo"] = None

            npe = (data.get('num_pago_electronico') or '').strip()
            res["numPagoElectronico"] = (npe if npe else None)
            res["pagos"] = [pago]

            print("DTE: RESUMEN.pagos ->", res["pagos"])
            print("DTE: RESUMEN.numPagoElectronico ->", res["numPagoElectronico"])

            # Persistir JSON
            factura.json_original = factura_json
            factura.save()
            print("DTE: JSON generado")

            base_path = getattr(RUTA_JSON_FACTURA, "path", None) or getattr(RUTA_JSON_FACTURA, "url", "")
            json_path = os.path.join(base_path, f"{factura.numero_control}.json")
            try:
                os.makedirs(os.path.dirname(json_path), exist_ok=True)
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(factura_json, f, indent=4, ensure_ascii=False)
                print("DTE: JSON guardado en:", json_path)
            except Exception as fs_e:
                print("DTE: Error guardando JSON en disco:", fs_e)

            print("DTE: ====== FIN generar_factura_view OK ======")

            # ---------- FIRMA ----------
            print("DTE: ==== INICIO FIRMA (función existente) ====")
            try:
                resp_firma = firmar_factura_view(request, factura.id, interno=True)
                print("STATUS CODE", resp_firma,  "code", resp_firma.status_code)
                if hasattr(resp_firma, "status_code") and int(resp_firma.status_code) >= 400:
                    return JsonResponse({
                        "mostrar_modal": True,
                        "titulo": "Error al firmar el DTE",
                        "mensaje": "No se pudo firmar el DTE, desea guardar el DTE sin firmar?",
                        "detalles": getattr(resp_firma, "content", b"").decode("utf-8", errors="ignore")[:2000],
                        "factura_id": factura.id,
                        "redirect": reverse('detalle_factura', args=[factura.id]),
                        "puede_guardar": True,
                        "puede_contingencia": False, #como fallo no se manda a contingencia
                        "enviar_mh_url": reverse('enviar_factura_hacienda', args=[factura.id]),
                    }, status=400)
                
            except Exception as e:
                print("DTE: *** ERROR firmando ***", e)
                return JsonResponse({
                    "mostrar_modal": True,
                    "titulo": "No se pudo firmar el DTE",
                    "mensaje": "Ocurrió un error durante la firma. ¿Deseas guardar la factura sin enviarla a Hacienda?",
                    "detalles": str(e),
                    "factura_id": factura.id,
                    "redirect": reverse('detalle_factura', args=[factura.id]),
                    "puede_guardar": True,                # <- NUEVO
                    "puede_contingencia": False,
                    "enviar_mh_url": reverse('enviar_factura_hacienda', args=[factura.id]),
                }, status=200)
            
            # ---------- ENVÍO ----------
            print("DTE: ==== INICIO ENVÍO a MH (función existente) ====")
            try:
                resp_envio = enviar_factura_hacienda_view(request, factura.id, uso_interno=True)
                if hasattr(resp_envio, "status_code") and int(resp_envio.status_code) >= 400:
                    return JsonResponse({
                        "mostrar_modal": True,
                        "titulo": "Error al enviar el DTE a MH",
                        "mensaje": "No se pudo enviar el DTE a MH, desea guardar el DTE sin enviar?",
                        "detalles": getattr(resp_envio, "content", b"").decode("utf-8", errors="ignore")[:2000],
                        "factura_id": factura.id,
                        "redirect": reverse('detalle_factura', args=[factura.id]),
                        "puede_guardar": True,
                        "puede_contingencia": True,
                        "enviar_mh_url": reverse('enviar_factura_hacienda', args=[factura.id]),
                    } , status=400)
            except Exception as e:
                print("DTE: *** ERROR enviando a MH ***", e)
                return JsonResponse({
                    "mostrar_modal": True,
                    "titulo": "No se pudo enviar el DTE a MH",
                    "mensaje": "Ocurrió un error durante el envío a MH. ¿Deseas guardar la factura sin enviarla?",
                    "detalles": str(e),
                    "factura_id": factura.id,
                    "redirect": reverse('detalle_factura', args=[factura.id]),
                    "puede_guardar": True,
                    "puede_contingencia": True,
                    "enviar_mh_url": reverse('enviar_factura_hacienda', args=[factura.id]),
                    }, status=200)

            print("DTE: ====== FIN generar+firmar+enviar OK ======")

            # Respuesta final
            if is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    "mensaje": "Factura generada, firmada y enviado a MH",
                    "factura_id": factura.id,
                    "numero_control": factura.numero_control,
                    "redirect": reverse('detalle_factura', args=[factura.id]),
                    "print_url": reverse('factura_termica', args=[factura.id]) + "?autoprint=1",
                })
            else:
                return redirect('detalle_factura', factura.id)

        except Exception as e:
            print("DTE: *** EXCEPCION ***", repr(e))
            return JsonResponse({"error": str(e)}, status=400)

    print("DTE: Metodo no permitido")
    return JsonResponse({"error": "Método no permitido"}, status=405)
# --------------------------------------------------------------------

@login_required
def select_tipo_facturas_mes_home(request):
    """
    Controlador maestro para el proceso de reenvío por lote.
    1. Si no hay filtros GET: Muestra la pantalla de selección (Mes/Año + DTE).
    2. Si hay filtros GET: Muestra la tabla de documentos pendientes (Listado).
    """
    tipo_dte = request.GET.get('tipo_documento_dte')
    mes_filtro = request.GET.get('mes')
    year_filtro = request.GET.get('year')

    print("ifffffffffffffffff")
    print("mes_filtro", mes_filtro)

    
    # === Lógica para mostrar la PANTALLA DE SELECCIÓN (Paso 1) ===
    if not tipo_dte or not mes_filtro or not year_filtro:
        
        now = timezone.now()
        current_year = now.year
        current_month = now.month

        print("current_month", current_month)
        print("current_year", current_year)
        
        mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        # 1. Preparar la lista de meses para el selector
        meses = []
        for i in range(1, 13):
            # mes_nombre = date(current_year, i, 1).strftime('%B').capitalize()
            meses.append({'id': str(i).zfill(2), 'nombre': mes_nombre[i-1]}) # Usamos zfill(2) para el formato 01, 02...
            
        # 2. Preparar la lista de años (ej. últimos 3 años)
        years = [str(y) for y in range(current_year, current_year - 3, -1)]
        print("meses", mes_filtro or str(current_month).zfill(2))

        context = {
            'meses': meses,
            # Se usan los valores GET o los valores actuales como defecto
            'current_mes': mes_filtro or str(current_month).zfill(2), 
            'years': years,
            'current_year': year_filtro or str(current_year), 
            # Aquí podrías pasar la lista de todos los tipos de DTE disponibles para las tarjetas si fuera dinámico
        }
        
        # Renderiza la plantilla de selección
        return render(request, 'facturacion/generar/home_reenvio_mes.html', context)

    
@login_required
def listar_documentos_pendientes(request):
    # La vista DEBE usar request.GET para obtener los filtros enviados por AJAX
    tipo_dte = request.GET.get('tipo_documento_dte')
    mes_filtro = request.GET.get('mes')
    year_filtro = request.GET.get('year')
    cliente_filtro = request.GET.get('cliente_filtro')
    
    documentos_pendientes = FacturaElectronica.objects.filter(
        tipo_dte__codigo=tipo_dte,
        sello_recepcion=None
    )
    
    clientes_disponibles = documentos_pendientes.values('dtereceptor__num_documento', 'dtereceptor__nombre').distinct()
    
    clientes_list = [
        {'num_documento': c['dtereceptor__num_documento'], 'nombre': c['dtereceptor__nombre']}
        for c in clientes_disponibles if c['dtereceptor__num_documento'] is not None and c['dtereceptor__nombre'] is not None
    ]
    
    print(" >>> CLIENTES DISPONIBLES ", clientes_disponibles)
    print(" >>> CLIENTES clientes_list ", clientes_list)
    
    print("Lista facturas pendientes de envio: ", documentos_pendientes)
    print("Mes filtro", mes_filtro)
    
    # 1. 📅 Filtrar por AÑO
    if year_filtro and year_filtro.isdigit():
        try:
            year_int = int(year_filtro)
            documentos_pendientes = documentos_pendientes.filter(
                fecha_emision__year=year_int
            )
            print(f"DEBUG: Aplicado filtro YEAR: {year_int}")
        except ValueError:
            # Esto maneja si isdigit() pasa pero int() falla (aunque es raro)
            pass
            
    # 2. 🗓️ Filtrar por MES
    if mes_filtro and mes_filtro.isdigit():
        try:
            mes_int = int(mes_filtro)
            # Los meses en DB son 1-12. El filtro debe ser 1-12
            if 1 <= mes_int <= 12: 
                documentos_pendientes = documentos_pendientes.filter(
                    fecha_emision__month=mes_int
                )
                print(f"DEBUG: Aplicado filtro MONTH: {mes_int}")
            else:
                print(f"DEBUG: Mes inválido: {mes_int}")
        except ValueError:
            pass
    if cliente_filtro:
        documentos_pendientes = documentos_pendientes.filter(
            dtereceptor__num_documento=cliente_filtro
        )
        print(f"DEBUG: Aplicado filtro CLIENTE: {cliente_filtro}")
    
    # 3. Optimización y ordenamiento
    documentos_pendientes = documentos_pendientes.prefetch_related(
        'detalles',
        'detalles__producto' 
    ).order_by('-fecha_emision')

    context = {
        'documentos_pendientes': documentos_pendientes, # <--- Usar la lista serializada
        'tipo_dte': tipo_dte,
        'mes': mes_filtro,
        'clientes_list': clientes_list,
        'cliente_seleccionado': cliente_filtro,
        'year': year_filtro,
    }
    
    return render(request, 'facturacion/generar/documentos_pendientes_modal.html', context)

# --------------------------------------------------------------------
# Asegura precisión suficiente en cálculos intermedios
getcontext().prec = 28

# Utilidades de redondeo
Q2  = Decimal("0.01")
Q6  = Decimal("0.000001")
D13 = Decimal("1.13")
IVA = Decimal("0.13")

def _to_dec(x, default="0"):
    if x is None or x == "":
        return Decimal(default)
    # Evita binarios: siempre desde str
    return Decimal(str(x))

def _q2(x: Decimal) -> Decimal:
    return x.quantize(Q2, rounding=ROUND_HALF_UP)

def _q6(x: Decimal) -> Decimal:
    return x.quantize(Q6, rounding=ROUND_HALF_UP)

def _none_if_blank(v):
    return None if (v is None or (isinstance(v, str) and v.strip() == "")) else v

def _normaliza_pagos(formas_pago, condicion_operacion_codigo, total_pagar):
    """
    Devuelve una lista de dicts [{codigo, montoPago, referencia, periodo, plazo}], 
    usando None cuando no aplique. 
    Evita strings vacíos que MH marca como 'valor inválido'.
    """
    pagos = []
    fp_iter = formas_pago or []

    def _extrae(v, *alts):
        # extrae v de dict/objeto
        if isinstance(v, dict):
            return v
        if hasattr(v, "__dict__"):
            d = {}
            for k in alts:
                d[k] = getattr(v, k, None)
            return d
        return v

    # Contado u "otro": se esperan montos > 0 por forma de pago.
    if str(condicion_operacion_codigo) in ("1", "3"):
        for fp in fp_iter:
            d = _extrae(fp, "codigo", "montoPago", "referencia", "periodo", "plazo")
            codigo     = str(d.get("codigo") or d.get("forma_pago") or "01")
            montoPago  = _to_dec(d.get("montoPago") or d.get("monto") or 0)
            referencia = _none_if_blank(d.get("referencia"))
            # En contado/otro NO deben enviarse valores para crédito
            pagos.append({
                "codigo": codigo,
                "montoPago": float(_q2(montoPago)),
                "referencia": referencia,
                "periodo": None,
                "plazo": None,
            })

        # Si no recibimos formas de pago pero es contado, asume 100% efectivo.
        if not pagos:
            pagos = [{
                "codigo": "01",          # Billetes y monedas
                "montoPago": float(_q2(_to_dec(total_pagar))),
                "referencia": None,
                "periodo": None,
                "plazo": None,
            }]

    # Crédito: monto por forma de pago suele ser 0.00, con plazo/período opcionales.
    elif str(condicion_operacion_codigo) == "2":
        # Toma el primer registro si viene alguno para heredar plazo/período/referencia.
        base = {}
        if fp_iter:
            d0 = _extrae(fp_iter[0], "codigo", "montoPago", "referencia", "periodo", "plazo")
            base = {
                "referencia": _none_if_blank(d0.get("referencia")),
                "plazo": _none_if_blank(d0.get("plazo")),
                "periodo": _none_if_blank(d0.get("periodo")),
            }
        pagos = [{
            "codigo": str(base.get("codigo") or "99"),  # 99-otros, o el que te envíen
            "montoPago": 0.00,
            "referencia": base.get("referencia"),
            "periodo": base.get("periodo"),
            "plazo": base.get("plazo"),
        }]
    else:
        # Fallback seguro
        pagos = [{
            "codigo": "99",
            "montoPago": float(_q2(_to_dec(total_pagar))),
            "referencia": None,
            "periodo": None,
            "plazo": None,
        }]

    return pagos


# --------------------------------------------------------------------
# generar_json
# --------------------------------------------------------------------
def generar_json(
    ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento,
    observaciones, iva_item_total, base_imponible_checkbox, saldo_favor,
    documentos_relacionados, contingencia, total_gravada,
    nombre_responsable, doc_responsable, formas_pago=None
):
    print("-Inicio llenar json")

    is_fe  = str(tipo_dte_obj.codigo) == "01"  # Factura Electrónica
    is_ccf = str(tipo_dte_obj.codigo) == "03"  # Crédito Fiscal (CCF)

    try:
        # -------- Defaults / saneamientos --------
        saldo_favor = _to_dec(saldo_favor, "0.00")
        montoExtension = Decimal("25000")

        # -------- Identificación --------
        json_identificacion = {
            "version": int(tipo_dte_obj.version),
            "ambiente": str(ambiente_obj.codigo),
            "tipoDte": str(tipo_dte_obj.codigo),
            "numeroControl": str(factura.numero_control),
            "codigoGeneracion": str(factura.codigo_generacion),
            "tipoModelo": int(factura.tipomodelo.codigo),
            "tipoOperacion": int(factura.tipotransmision.codigo),
            "tipoContingencia": None if not contingencia else int(contingencia.codigo),
            "motivoContin": None,
            "fecEmi": str(factura.fecha_emision),
            "horEmi": factura.hora_emision.strftime("%H:%M:%S"),
            "tipoMoneda": str(factura.tipomoneda.codigo) if getattr(factura, "tipomoneda", None) else "USD",
        }

        # -------- Relacionados / Otros --------
        json_documento_relacionado = documentos_relacionados or None
        json_otros_documentos = None

        # -------- Emisor --------
        json_emisor = {
            "nit": str(emisor.nit),
            "nrc": str(emisor.nrc),
            "nombre": str(emisor.nombre_razon_social),
            "codActividad": str(emisor.actividades_economicas.first().codigo) if emisor.actividades_economicas.exists() else "",
            "descActividad": str(emisor.actividades_economicas.first().descripcion) if emisor.actividades_economicas.exists() else "",
            "nombreComercial": str(emisor.nombre_comercial),
            "tipoEstablecimiento": str(emisor.tipoestablecimiento.codigo) if emisor.tipoestablecimiento else "",
            "direccion": {
                "departamento": str(emisor.municipio.departamento.codigo),
                "municipio": str(emisor.municipio.codigo),
                "complemento": emisor.direccion_comercial,
            },
            "telefono": str(emisor.telefono),
            "correo": str(emisor.email),
            "codEstableMH": str(getattr(emisor, "codigo_establecimiento", "") or "M001"),
            "codEstable": "0001",
            "codPuntoVentaMH": str(getattr(emisor, "codigo_punto_venta", "") or "P001"),
            "codPuntoVenta": "0001",
        }

        # -------- Receptor --------
        json_receptor = {
            "nombre": str(receptor.nombre),
            "codActividad": str(receptor.actividades_economicas.first().codigo) if receptor.actividades_economicas.exists() else "",
            "descActividad": str(receptor.actividades_economicas.first().descripcion) if receptor.actividades_economicas.exists() else "",
            "direccion": {
                "departamento": str(receptor.municipio.departamento.codigo),
                "municipio": str(receptor.municipio.codigo),
                "complemento": receptor.direccion or "",
            },
            "telefono": receptor.telefono or "",
            "correo": receptor.correo or "",
        }
        # nrc puede ser Null
        json_receptor["nrc"] = str(receptor.nrc) if getattr(receptor, "nrc", None) not in (None, "None", "") else None

        # FE: tipoDocumento/numDocumento
        if is_fe:
            if getattr(receptor, "tipo_documento", None):
                json_receptor["tipoDocumento"] = str(receptor.tipo_documento.codigo)
            else:
                json_receptor["tipoDocumento"] = ""
            json_receptor["numDocumento"] = str(receptor.num_documento)

        # -------- Cuerpo del Documento --------
        items = []
        iva_total_por_items = Decimal("0.00")
        total_no_suj = Decimal("0.00")
        total_exenta = Decimal("0.00")
        total_gravada_calc = Decimal("0.00")
        total_no_gravado = Decimal("0.00")
        sub_total_ventas = Decimal("0.00")

        for raw in (cuerpo_documento or []):
            cantidad   = _to_dec(raw.get("cantidad", 0))
            precio_uni = _to_dec(raw.get("precioUni", 0))
            desc_item  = _to_dec(raw.get("montoDescu", 0))
            venta_ns   = _to_dec(raw.get("ventaNoSuj", 0))
            venta_ex   = _to_dec(raw.get("ventaExenta", 0))
            venta_gr   = _to_dec(raw.get("ventaGravada", 0))
            no_grav    = _to_dec(raw.get("noGravado", 0))

            if venta_gr == 0 and venta_ns == 0 and venta_ex == 0:
                venta_gr = (precio_uni * cantidad - desc_item)

            # IVA informativo para FE
            iva_item = _q2(_q6((venta_gr / D13) * IVA)) if (venta_gr > 0 and is_fe) else Decimal("0.00")

            psv = _to_dec(raw.get("psv", precio_uni))

            # En CCF, no enviar codTributo por ítem; tributos=["20"] si es gravada
            if is_ccf:
                numero_doc_linea  = None
                cod_tributo_linea = None
                tributos_linea    = ["20"] if venta_gr > 0 else None
            else:
                numero_doc_linea  = raw.get("numeroDocumento", None)
                cod_tributo_linea = raw.get("codTributo", None)
                tributos_linea    = raw.get("tributos", ["20"] if venta_gr > 0 else None)

            tipo_item_raw = int(raw.get("tipoItem", 1))
            tipo_item_ok = tipo_item_raw if tipo_item_raw in (1, 2, 3, 4) else 1

            item = {
                "numItem": int(raw.get("numItem", len(items) + 1)),
                "tipoItem": tipo_item_ok,
                "numeroDocumento": numero_doc_linea,
                "codigo": raw.get("codigo", None),
                "codTributo": cod_tributo_linea,    # None en CCF
                "descripcion": raw.get("descripcion", ""),
                "cantidad": float(_q6(cantidad)),
                "uniMedida": int(raw.get("uniMedida", 59)),
                "precioUni": float(_q6(precio_uni)),
                "montoDescu": float(_q6(desc_item)),
                "ventaNoSuj": float(_q6(venta_ns)),
                "ventaExenta": float(_q6(venta_ex)),
                "ventaGravada": float(_q6(venta_gr)),
                "tributos": tributos_linea,         # ["20"] si gravada; None si no
                "psv": float(_q6(psv)),
                "noGravado": float(_q6(no_grav)),
            }
            if is_fe:
                item["ivaItem"] = float(_q6(iva_item))

            items.append(item)

            iva_total_por_items += iva_item
            total_no_suj        += venta_ns
            total_exenta        += venta_ex
            total_gravada_calc  += venta_gr
            total_no_gravado    += no_grav
            sub_total_ventas    += (venta_ns + venta_ex + venta_gr)

        # -------- Resumen --------
        desc_no_suj  = _to_dec(getattr(factura, "descuen_no_sujeto", 0))
        desc_exenta  = _to_dec(getattr(factura, "descuento_exento", 0))
        desc_gravada = _to_dec(getattr(factura, "descuento_gravado", 0))
        por_desc     = _to_dec(getattr(factura, "por_descuento", 0))
        total_desc   = desc_no_suj + desc_exenta + desc_gravada

        sub_total = sub_total_ventas - total_desc

        iva_reten  = _to_dec(getattr(factura, "iva_retenido", 0))
        ret_renta  = _to_dec(getattr(factura, "retencion_renta", 0))

        # IVA consolidado solo para CCF
        iva_consolidado = _q2(total_gravada_calc * IVA) if is_ccf else Decimal("0.00")

        # En CCF el MTO = subTotal + IVA; en FE (sin otros tributos), MTO = subTotal
        monto_total_operacion = sub_total + (iva_consolidado if is_ccf else Decimal("0.00"))

        total_a_pagar = monto_total_operacion - iva_reten - ret_renta + total_no_gravado
        if total_a_pagar < Decimal("0.00"):
            total_a_pagar = Decimal("0.00")

        condicion_operacion_codigo = (
            int(factura.condicion_operacion.codigo)
            if getattr(factura, "condicion_operacion", None)
            and str(factura.condicion_operacion.codigo).isdigit()
            else 1
        )
        if saldo_favor is not None and saldo_favor != "" and saldo_favor > 0:
            condicion_operacion_codigo = 1

        pagos = _normaliza_pagos(formas_pago or getattr(factura, "formas_Pago", []), condicion_operacion_codigo, total_a_pagar)

        json_resumen = {
            "totalNoSuj":          float(_q2(total_no_suj)),
            "totalExenta":         float(_q2(total_exenta)),
            "totalGravada":        float(_q2(total_gravada_calc)),
            "subTotalVentas":      float(_q2(sub_total_ventas)),
            "descuNoSuj":          float(_q2(desc_no_suj)),
            "descuExenta":         float(_q2(desc_exenta)),
            "descuGravada":        float(_q2(desc_gravada)),
            "porcentajeDescuento": float(_q2(por_desc)),
            "totalDescu":          float(_q2(total_desc)),
            "subTotal":            float(_q2(sub_total)),
            "ivaRete1":            float(_q2(iva_reten)),
            "reteRenta":           float(_q2(ret_renta)),
            "montoTotalOperacion": float(_q2(monto_total_operacion)),
            "totalNoGravado":      float(_q2(total_no_gravado)),
            "totalPagar":          float(_q2(total_a_pagar)),
            "totalLetras":         str(getattr(factura, "total_letras", "")),
            "saldoFavor":          float(_q2(saldo_favor)),
            "condicionOperacion":  int(condicion_operacion_codigo),
            "pagos":               pagos,
            "numPagoElectronico":  _none_if_blank(getattr(factura, "num_pago_electronico", None)),
            "tributos":            None,
        }

        # FE: totalIva permitido (informativo). CCF: NO
        if is_fe:
            json_resumen["totalIva"] = float(_q2(iva_total_por_items))

        # Solo CCF: incluir IVA consolidado como tributo "20"
        if is_ccf and iva_consolidado > 0:
            json_resumen["tributos"] = [{
                "codigo": "20",
                "descripcion": "Impuesto al Valor Agregado 13%",
                "valor": float(_q2(iva_consolidado)),
            }]

        # -------- Extensión --------
        json_extension = {
            "nombEntrega": None,
            "docuEntrega": None,
            "nombRecibe": None,
            "docuRecibe": None,
            "observaciones": observaciones if (observaciones is not None and len(observaciones) > 0) else "Generado por Sistema Django",
            "placaVehiculo": None,
        }

        # -------- Ajustes por CCF --------
        if is_ccf:
            json_receptor["nit"] = str(receptor.num_documento)
            json_receptor["nombreComercial"] = str(getattr(receptor, "nombreComercial", "") or "")
            json_resumen["ivaPerci1"] = float(_q2(_to_dec(getattr(factura, "iva_percibido", 0))))

            if base_imponible_checkbox is True:
                # Si marcaste base imponible (no gravado), no envíes tributos
                json_resumen["tributos"] = None

            if _to_dec(json_resumen["montoTotalOperacion"]) >= montoExtension:
                json_extension["nombEntrega"] = str(nombre_responsable or "")
                json_extension["docuEntrega"] = str(doc_responsable or "")

        # -------- Construcción final --------
        json_completo = {
            "identificacion":       json_identificacion,
            "documentoRelacionado": json_documento_relacionado,
            "emisor":               json_emisor,
            "receptor":             json_receptor,
            "otrosDocumentos":      json_otros_documentos,
            "ventaTercero":         None,
            "cuerpoDocumento":      items,
            "resumen":              json_resumen,
            "extension":            json_extension,
            "apendice":             None,
        }

        return json_completo

    except Exception as e:
        print(f"Error al generar el json de la factura: {e}")
        from django.http import JsonResponse
        return JsonResponse({"error": str(e)}, status=400)
# --------------------------------------------------------------------


def generar_json_doc_ajuste(ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento, observaciones, documentos_relacionados, contingencia, total_gravada):
    print("-Inicio llenar json")
    try:
        
        #Resumen tributos
        tributo = Tributo.objects.get(codigo="20")
        
        #Llenar json
        json_identificacion = {
            "version": int(tipo_dte_obj.version),
            "ambiente":  str(ambiente_obj.codigo),
            "tipoDte": str(tipo_dte_obj.codigo),
            "numeroControl": str(factura.numero_control),
            "codigoGeneracion": str(factura.codigo_generacion),
            "tipoModelo": int(factura.tipomodelo.codigo),
            "tipoOperacion": int(factura.tipotransmision.codigo),
            "tipoContingencia": None,
            "motivoContin": None,
            "fecEmi": str(factura.fecha_emision),
            "horEmi": factura.hora_emision.strftime('%H:%M:%S'),
            "tipoMoneda": str(factura.tipomoneda.codigo) if factura.tipomoneda else "USD"
        }
        
        json_emisor = {
            "nit": str(emisor.nit),
            "nrc": str(emisor.nrc),
            "nombre": str(emisor.nombre_razon_social),
            "codActividad": str(emisor.actividades_economicas.first().codigo) if emisor.actividades_economicas.exists() else "",
            "descActividad": str(emisor.actividades_economicas.first().descripcion) if emisor.actividades_economicas.exists() else "",
            "nombreComercial": str(emisor.nombre_comercial),
            "tipoEstablecimiento": str(emisor.tipoestablecimiento.codigo) if emisor.tipoestablecimiento else "",
            "direccion": {
                "departamento": str(emisor.municipio.departamento.codigo), #"05",
                "municipio": str(emisor.municipio.codigo), #"19",
                "complemento": emisor.direccion_comercial
            },
            "telefono": str(emisor.telefono),
            "correo": str(emisor.email)
        }
        
        json_receptor = {
            "nit": str(receptor.num_documento),
            "nombre": str(receptor.nombre),            
            "codActividad": str(receptor.actividades_economicas.first().codigo) if receptor.actividades_economicas.exists() else "", #"24310",
            "descActividad": str(receptor.actividades_economicas.first().descripcion) if receptor.actividades_economicas.exists() else "", #"undición de hierro y acero",
            "nombreComercial": str(receptor.nombreComercial),
            "direccion": {
                "departamento": str(receptor.municipio.departamento.codigo), #"05",
                "municipio": str(receptor.municipio.codigo), #"19",
                "complemento": receptor.direccion or ""
            },
            "telefono": receptor.telefono or "",
            "correo": receptor.correo or "",
        }
        
        json_resumen = {
            "totalNoSuj": float(abs(factura.total_no_sujetas)),
            "totalExenta": float(abs(factura.total_exentas)),
            "totalGravada": float(abs(factura.total_gravadas)),
            "subTotalVentas": float(abs(factura.sub_total_ventas)),
            "descuNoSuj": float(abs(factura.descuen_no_sujeto)),
            "descuExenta": float(abs(factura.descuento_exento)),
            "descuGravada": float(abs(factura.descuento_gravado)),
            "totalDescu": float(abs(factura.total_descuento)),
            "subTotal": float(abs(factura.sub_total)),
            "ivaPerci1": float(abs(factura.iva_percibido)),
            "ivaRete1": float(abs(factura.iva_retenido)),
            "reteRenta": float(abs(factura.retencion_renta)),
            "montoTotalOperacion": float(abs(factura.total_operaciones)),
            "totalLetras": factura.total_letras,
            "condicionOperacion": int(factura.condicion_operacion.codigo) if factura.condicion_operacion and factura.condicion_operacion.codigo.isdigit() else 1
        }
        
        #Requerido cuando el monto es mayor o igual a $11,428.57
        json_extension = {
            "nombEntrega": None,
            "docuEntrega": None,
            "nombRecibe": None,
            "docuRecibe": None,
            "observaciones": observaciones
        }
        
        json_apendice = None
        
        #Modificacion de json en base al tipo dte a generar
        if receptor is not None:
            nrc_receptor = None
            if receptor.nrc is not None and receptor.nrc !="None":
                nrc_receptor = str(receptor.nrc)
            json_receptor["nrc"] = nrc_receptor
        
        #Calcular el valor total del tributo
        subTotalVentas = total_gravada
        valorTributo = ( Decimal(subTotalVentas) * Decimal(tributo.valor_tributo) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        json_resumen["tributos"] = [
            {
            "codigo": str(tributo.codigo),
            "descripcion": str(tributo.descripcion),
            "valor": float(valorTributo)
            }
        ]

        if tipo_dte_obj.codigo == COD_NOTA_DEBITO:
            json_resumen["numPagoElectronico"] = None
            print("num pago: ", json_resumen["numPagoElectronico"])
        
        print("Cuerpo documento: ", cuerpo_documento)
        json_completo = {
            "identificacion": json_identificacion,
            "documentoRelacionado": documentos_relacionados,
            "emisor": json_emisor,
            "receptor": json_receptor,
            "ventaTercero": None,
            "cuerpoDocumento": cuerpo_documento,
            "resumen": json_resumen,
            "extension": json_extension,
            "apendice": json_apendice
        }
        print("Json ajuste: ", json.dumps(json_completo))
        return json_completo
    except Exception as e:
            print(f"Error al generar el json de la factura: {e}")
            return JsonResponse({"error": str(e)}, status=400)

def generar_json_sujeto(
        ambiente_obj, 
        tipo_dte_obj, 
        factura, 
        emisor, 
        receptor, 
        cuerpo_documento, 
        observaciones, 
        contingencia,
        total_operaciones, 
        total_descuento, 
        total_pagar, 
        descuento_global,
        sub_total,
        formas_pago=None
    ):
    
    cod_act_receptor  = ""
    desc_act_receptor = ""
    
    actividades = getattr(receptor, "actividades_economicas", None)
    if actividades and hasattr(actividades, "exists") and actividades.exists():
        primera = actividades.first()
        cod_act_receptor  = str(primera.codigo)
        desc_act_receptor = str(primera.descripcion)
    print("-Inicio llenar json sujeto")
    try:
        # if saldo_favor is None or saldo_favor == "":
        #     saldo_favor = Decimal("0.00")

        if formas_pago is None:
            formas_pago = factura.formas_Pago or []
        
        #Llenar json
        json_identificacion = {
            "version": tipo_dte_obj.version,
            "ambiente":  ambiente_obj.codigo,
            "tipoDte": str(tipo_dte_obj.codigo),
            "numeroControl": str(factura.numero_control),
            "codigoGeneracion": str(factura.codigo_generacion),
            "tipoModelo": int(factura.tipomodelo.codigo),
            "tipoOperacion": int(factura.tipotransmision.codigo),
            "tipoContingencia": None,
            "motivoContin": None,
            "fecEmi": str(factura.fecha_emision),
            "horEmi": factura.hora_emision.strftime('%H:%M:%S'),
            "tipoMoneda": str(factura.tipomoneda.codigo) if factura.tipomoneda else "USD"
        }
        
        json_emisor = {
            "nit": str(emisor.nit),
            "nrc": str(emisor.nrc),
            "nombre": str(emisor.nombre_razon_social),
            "codActividad": str(emisor.actividades_economicas.first().codigo) if emisor.actividades_economicas.exists() else "",
            "descActividad": str(emisor.actividades_economicas.first().descripcion) if emisor.actividades_economicas.exists() else "",
            "direccion": {
                "departamento": str(emisor.municipio.departamento.codigo), #"05",
                "municipio": str(emisor.municipio.codigo), #"19",
                "complemento": emisor.direccion_comercial
            },
            "telefono": str(emisor.telefono),
            "correo": str(emisor.email),
            "codEstableMH": str(emisor.codigo_establecimiento or "M001"),
            "codEstable": "0001",
            "codPuntoVentaMH": str(emisor.codigo_punto_venta or "P001"),
            "codPuntoVenta": "0001",
        }
        
        total_ops = Decimal(total_operaciones).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        json_sujeto_excluido = {
            "tipoDocumento": str(receptor.tipo_documento.codigo),
            "numDocumento": str(str(receptor.num_documento)),
            "nombre": str(receptor.nombre),
            "codActividad":  cod_act_receptor,   # código de la primera actividad
            "descActividad": desc_act_receptor, 
            "direccion": {
                "departamento": str(receptor.municipio.departamento.codigo), #"05",
                "municipio": str(receptor.municipio.codigo), #"19",
                "complemento": receptor.direccion or ""
            },
            "telefono": receptor.telefono or "",
            "correo": receptor.email or "",
        }

        print("formas_pago ---", formas_pago)

        # 5) Retenciones
        ret_iva   = Decimal(factura.iva_retenido).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        ret_renta = Decimal(factura.retencion_renta).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


        json_resumen = {
            "totalCompra": float(total_ops),
            "descu":       float(descuento_global),
            "totalDescu":  float(total_descuento),
            "subTotal":    float(sub_total),
            "ivaRete1":    float(ret_iva),     # si aplica; si no, queda 0.00
            "reteRenta":   float(ret_renta),   # si aplica; si no, queda 0.00
            "totalPagar":  float(total_pagar),
            "totalLetras": factura.total_letras,
            "condicionOperacion": int(factura.condicion_operacion.codigo) if factura.condicion_operacion and factura.condicion_operacion.codigo.isdigit() else 1,
            "pagos":       formas_pago,
            "observaciones": observaciones,
        }
    
        print("json resumen:", json_resumen)
        
        json_apendice = None

        #Verificar que el monto consolidado de formas de pago aplique para el total a pagar
        f_pagos = json_resumen["pagos"]
        total_pagar_resumen = Decimal(str(json_resumen["totalPagar"]))
        monto_total_fp = Decimal("0.00")
        print("pagos", f_pagos)
        
        for fp in f_pagos:
            monto_total_fp += Decimal(fp["montoPago"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
        if monto_total_fp.compare(Decimal("0.00")) > 0 and monto_total_fp.compare(total_pagar_resumen) < 0:
            errorFormaPago = JsonResponse({"error": "El pago parcial es inferior al pago total", "Pago recibido": monto_total_fp})
        
        json_completo = {
                "identificacion": json_identificacion,
                "emisor": json_emisor,
                "sujetoExcluido": json_sujeto_excluido,
                "cuerpoDocumento": cuerpo_documento,
                "resumen": json_resumen,
                "apendice": json_apendice
            }
        return json_completo
    except Exception as e:
            print(f"Error al generar el json de la factura: {e}")
            return JsonResponse({"error": str(e)}, status=400)

#VISTAS PARA FIRMAR Y GENERAR EL SELLO DE RECEPCION CON HACIENDA
@csrf_exempt
def firmar_factura_view(request, factura_id, interno=False):
    #CERT_PATH        = get_config("certificado", campo="url_endpoint")
    #FIRMADOR_URL = get_firmador_url()
    #Bloquear creacion de eventos por reintentos
    crear_evento = request.GET.get('crear_evento', 'false').lower() == 'true'
    print(f"-Inicio firma DTE: {factura_id}, interno: {interno}: crear evento: {crear_evento}")

    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    emisor = factura.dteemisor or _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({"error": "No se encontró emisor para firmar este DTE."}, status=400)

    contingencia = True
    intento = 1
    intentos_max = 3
    tipo_contingencia_obj = None
    contingencia_creada = False
    response = None
    response_data = {}
    fecha_actual = obtener_fecha_actual()
    firma = True
    motivo_otro = False
    mostrar_modal = False

    # Reintentos desde sesión (inicializar si no existe)
    intentos_modal = request.session.get('intentos_reintento', 0)
    print("Intentos modal: ", intentos_modal)

    # Verificar si la factura ya ha sido firmada
    if factura.firmado:
        # Si la factura ya está firmada, no mostrar modal y no continuar con los reintentos
        return redirect(
            f"{reverse('detalle_factura', args=[factura_id])}?mostrar_modal=0&firma=1&envio_mh=0&firmado=1"
        )
    # Intentos automáticos
    while intento <= intentos_max and not factura.firmado and intentos_modal <=2:
        print(f"Inicio Intento {intento} de {intentos_max}")
        token_data = Token_data.objects.filter(activado=True).first()
        print(f"token_data:   {token_data} ")
        
        if not token_data:
            print(f"NO HAY TOKEN:   {token_data} ")
            
            return JsonResponse({"error": "No hay token activo."}, status=401)

        if not os.path.exists(CERT_PATH):
            print("sssssss: ")
            print(f"sssssss: {CERT_PATH}")
            
            return JsonResponse({"error": "Certificado no encontrado."}, status=400)

        try:
            if isinstance(factura.json_original, dict):
                dte_json_str = json.dumps(factura.json_original, separators=(',', ':'))
            else:
                json_obj = json.loads(factura.json_original)
                dte_json_str = json.dumps(json_obj, separators=(',', ':'))
        except Exception as e:
            return JsonResponse({"error": "JSON inválido", "detalle": str(e)}, status=400)
        
        # Antes de la llamada al firmador, se parsea una sola vez a objeto:
        if isinstance(factura.json_original, dict):
            dte_json_obj = factura.json_original
        else:
            dte_json_obj = json.loads(factura.json_original)

        payload = {
            "nit": emisor.nit,
            "activo": True,
            "passwordPri": emisor.clave_privada,
            "dteJson": dte_json_obj,
        }
        
        print("payload-------------- ", payload)

        try:
            print("dentro try-------------- ")
            
            response = requests.post(FIRMADOR_URL.url_endpoint, json=payload, headers={"Content-Type": CONTENT_TYPE.valor})
            print("Response envio: ", response)
            print("Response envio status: ", response.status_code)
            try:
                response_data = response.json()
            except Exception as e:
                response_data = {"error": "No se pudo parsear JSON", "detalle": response.text}
                print("Error al decodificar JSON:", e)
                
            print("Response data firma: ", response_data)
            if response.status_code == 200 and response_data.get("status") == "OK":
                print("Se firmo el documento")
                factura.json_firmado = response_data
                factura.firmado = True
                factura.save()
                request.session['intentos_reintento'] = 0  # Resetear intentos
                request.session.modified = True
                contingencia = False
                motivo_otro = False
                mostrar_modal = False
                crear_evento = False
                break
            else:
                print("Response firma status error 1: ", response)
                print("Firma | Ocurrio un error al firmar la factura")
                motivo_otro = False
                if response.status_code in [500, 502, 503, 504, 408]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                elif response.status_code in [408, 499]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                elif response.status_code in [503, 504]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                else:  # Otro- 400, 500, 502
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                    motivo_otro = True  # Activar motivo_otro en errores graves
                    mensaje = f"Error en el envío de la factura: {response.status_code}"
                    print("Error mh: ", mensaje)
                intento += 1
                time.sleep(1) 
                print("Response firma status error 2: ", response)
        except requests.exceptions.RequestException as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
            intento += 1
            time.sleep(1) 
            print("Excepción general:", str(e))
        except requests.exceptions.ConnectionError:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            intento += 1
            time.sleep(1) 
        except requests.exceptions.Timeout:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            intento += 1
            time.sleep(1) 
        except Exception as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
            motivo_otro = True
            intento += 1
            time.sleep(1) 
            print("Error inesperado emisor:", str(e))
    
    # Si fallaron todos los intentos
    if contingencia:
        print(f"Tipo de contingencia: {tipo_contingencia_obj}, Contingencia creada: {contingencia_creada}, crear evento: {crear_evento}")
        if not contingencia_creada and crear_evento:
            print("Crear contingencia-lote")
            finalizar_contigencia_view(request)

            factura.estado = False
            factura.contingencia = True
            factura.tipomodelo = Modelofacturacion.objects.get(codigo="2")
            factura.tipotransmision = TipoTransmision.objects.get(codigo="2")
            factura.fecha_modificacion = fecha_actual.date()
            factura.hora_modificacion = fecha_actual.time()
            factura.json_original["identificacion"]["tipoModelo"] = int(factura.tipomodelo.codigo)
            factura.json_original["identificacion"]["tipoOperacion"] = int(factura.tipotransmision.codigo)
            factura.save()

            lote_contingencia_dte_view(request, factura_id, tipo_contingencia_obj)
            contingencia_creada = True

        # Incrementar reintentos solo si falló la firma
        print(f"Intentos de reintento (antes de incrementar): {intentos_modal}")
        if intentos_modal < 3:
            intentos_modal += 1
            request.session['intentos_reintento'] = intentos_modal
            request.session.modified = True

        # Decidir si mostrar el modal dependiendo de los intentos
        mostrar_modal = intentos_modal < 3
        print(f"Intentos: {intentos_modal}, sesion: {request.session['intentos_reintento']}, Mostrar modal: {mostrar_modal}, motivo: {motivo_otro}")
    
    # Firma exitosa
    print("Response data: ", response_data)
    if response and response.status_code == 200 and response_data.get("status") == "OK":
        json_signed_path = f"{FACTURAS_FIRMADAS_URL.url}{factura.codigo_generacion}.json"
        os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
        with open(json_signed_path, "w", encoding="utf-8") as json_file:
            json.dump(response_data, json_file, indent=4, ensure_ascii=False)
    print("-Fin firma DTE:", factura_id)
    
    if interno:
        if response:
            return JsonResponse(response_data, status=response.status_code)
        else:
            return JsonResponse({"error": "No hubo respuesta del firmador"}, status=500)
    else:
        return redirect(
            f"{reverse('detalle_factura', args=[factura_id])}?"
            f"mostrar_modal={'1' if mostrar_modal else '0'}"
            f"&firma={'1' if firma else '0'}"
            f"&envio_mh=0"
            f"&intentos_modal={intentos_modal}"
            f"&motivo_otro={'1' if motivo_otro else '0'}"
            f"&firmado={'1' if factura.firmado else '0'}"
            f"&recibido_mh=0"
        )

@csrf_exempt
@require_POST
def enviar_factura_hacienda_view(request, factura_id, uso_interno=False, consolidacion=False):
    HACIENDA_URL_PROD = get_config("hacienda_url_prod", campo="url_endpoint")
    #Bloquear creacion de eventos por reintentos
    crear_evento = request.GET.get('crear_evento', 'false').lower() == 'true'
    print("Inicio enviar factura a MH: crear evento: ", crear_evento)

    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    
    emisor = factura.dteemisor or _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({"error": "No se encontró emisor para firmar este DTE."}, status=400)
    
    contingencia = True
    intento = 1
    intentos_max = 3 #Intentos para envio del dte a MH
    tipo_contingencia_obj = None
    mensaje = None
    # Banderas para verificar si ya se creo una contingencia
    contingencia_creada = False
    error_autenticacion = None
    error_envio = None
    
    fecha_actual = obtener_fecha_actual()
    envio_mh = True
    motivo_otro = False
    mostrar_modal = False
    
    # Reintentos desde sesión (inicializar si no existe)
    intentos_modal = request.session.get('intentos_reintento', 0)
    print("Intento modal: ", intentos_modal)
    
    

    # Paso 1: Autenticación contra el servicio de Hacienda
    nit_empresa = str(emisor.nit) #"06142811001040"
    pwd = str(emisor.clave_publica) #"Q#3P9l5&@aF!gT2sA"#llave publica
    auth_url = URL_AUTH.url_endpoint
    auth_headers = {
        "Content-Type": HEADERS.url_endpoint,
        "User-Agent": HEADERS.valor
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}
    auth_response = None
    response_data = None
    envio_response = None

    print("Inicio response autenticacion")
    while intento <= intentos_max and not factura.recibido_mh and intentos_modal <=2:
        print(f"Intento {intento} de {intentos_max}")
        try:
            #---Autenticacion
            auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
            
            if auth_response.status_code == 200:
                auth_response_data = auth_response.json()
                estado_response = auth_response_data.get("estado", None)
            
                token_body = auth_response_data.get("body", {})
                token = token_body.get("token")
                token_type = token_body.get("tokenType", "Bearer")
                roles = token_body.get("roles", [])
                if token and token.startswith("Bearer "):
                    token = token[len("Bearer "):]
                
                # Guardar o actualizar el token en la base de datos
                Token_data.objects.update_or_create(
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
                motivo_otro = False
                #crear_evento = False
                print("Autenticacion exitosa")
                break
            else:
                # Manejo de errores según el código de estado de la respuesta
                motivo_otro = False
                if auth_response.status_code in [500, 502, 503, 504, 408]: #503, 504
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                elif auth_response.status_code in [408, 499]: #500, 503
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                elif auth_response.status_code in [503, 504]: #503, 504
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                else:#Otro- 400, 500, 502
                    mensaje = f"Error en la autenticación: {auth_response.status_code}"
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                    motivo_otro = True 
                # Intentar nuevamente
                error_autenticacion = f"Error en la autenticación: {auth_response.status_code}"
                print("Error autenticación: ", error_autenticacion)
                time.sleep(1) # Esperar antes del siguiente intento
                intento += 1
                contingencia = True
        except requests.exceptions.RequestException as e:
            # Manejo de excepción de red
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
            time.sleep(1) 
            intento += 1
            error_autenticacion = str(e)
            print("Error: ", error_autenticacion)
        except requests.exceptions.ConnectionError:
            #Error de red del emisor
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_autenticacion = f"Error de conexion: {auth_response.status_code}"
            print("Error: ", error_autenticacion)
        except requests.exceptions.Timeout:
            #Error del emisor
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_autenticacion = f"e agoto el tiempo de espera: {auth_response.status_code}"
            print("Error: ", error_autenticacion)
        except Exception as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
            motivo_otro = True
            error_autenticacion = str(e)
            print(f"Ocurrió un error inesperado: {e}")
    
    # Si la autenticación falló después de los intentos, detener el flujo
    print("CONTINGENCIA: ", contingencia, "crear evento", crear_evento)
    #---Envio del dte
    if contingencia == False:
        intento = 1
        while intento <= intentos_max and not factura.recibido_mh and intentos_modal <=2:
            try:
                # Paso 2: Enviar la factura firmada a Hacienda
                token_data_obj = Token_data.objects.filter(activado=True).first()
                if not token_data_obj or not token_data_obj.token:
                    return JsonResponse({"error": "No hay token activo para enviar la factura"}, status=401)

                codigo_generacion_str = str(factura.codigo_generacion)

                # --- Validación y limpieza del documento firmado ---
                documento_str = factura.json_firmado
                if not isinstance(documento_str, str):
                    documento_str = json.dumps(documento_str)

                # Eliminar posibles caracteres BOM y espacios innecesarios
                documento_str = documento_str.lstrip('\ufeff').strip()

                try:
                    if isinstance(factura.json_firmado, str):
                        firmado_data = json.loads(factura.json_firmado)
                    else:
                        firmado_data = factura.json_firmado
                except Exception as e:
                    return JsonResponse({
                        "error": "Error al parsear el documento firmado",
                        "detalle": str(e)
                    }, status=400)

                documento_token = firmado_data.get("body", "")
                if not documento_token:
                    return JsonResponse({
                        "error": "El documento firmado no contiene el token en 'body'"
                    }, status=400)

                documento_token = documento_token.strip()  # Limpiar espacios innecesarios

                envio_json = {
                    "ambiente": AMBIENTE.codigo,  # "00" para Pruebas; "01" para Producción
                    "idEnvio": factura.id,
                    "version": int(factura.json_original["identificacion"]["version"]),
                    "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
                    "documento": documento_token,  # Enviamos solo el JWT firmado
                    "codigoGeneracion": codigo_generacion_str
                }

                envio_headers = {
                    "Authorization": f"Bearer {token_data_obj.token}",
                    "User-Agent": USER_AGENT.valor,
                    "Content-Type": CONTENT_TYPE.valor
                }
                
                print("Inicio envio response: ")
                envio_response = requests.post(
                    HACIENDA_URL_PROD,
                    json=envio_json,
                    headers=envio_headers
                )
                print("Response enviado: ")

                print("Envio response status code:", envio_response.status_code)
                print("Envio response headers:", envio_response.headers)
                print("Envio response text:", envio_response.text)
                sello_recibido = None
                
                try:
                    response_data = envio_response.json() if envio_response.text.strip() else {}
                    sello_recibido = response_data.get("selloRecibido", None)
                except ValueError as e:
                    response_data = {"raw": envio_response.text or "No content"}
                    print("Error al decodificar JSON en envío:", e)
                        
                if envio_response.status_code == 200 and sello_recibido is not None:
                    factura.sello_recepcion = response_data.get("selloRecibido", "")
                    factura.recibido_mh=True
                    #Guardar respuesta de MH en json_original
                    json_response_data = {
                        "jsonRespuestaMh": response_data
                    }
                    json_original = factura.json_original
                    
                    #Combinar jsons
                    json_nuevo = json_original | json_response_data
                    #Convertir diccionario en json
                    json_respuesta_mh = json.dumps(json_nuevo)
                    #Al convertir un diccionario en json se guarda como un string, por lo que se debe convertir a json (loads)
                    json_original_campo = json.loads(json_respuesta_mh)
                    factura.json_original = json_original_campo
                    factura.estado=True
                    factura.contingencia = False
                    factura.envio_correo = False
                    factura.save()
                    contingencia = False
                    motivo_otro = False
                    mostrar_modal = False
                    crear_evento = False
                    # crear el movimeinto de inventario
                    # Se asume que la factura tiene una relación a sus detalles, 
                    # donde se encuentran los productos y cantidades
                    for detalle in factura.detalles.all():
                        if detalle is not None and detalle.producto.almacenes.exists():
                            almacen = detalle.producto.almacenes.first() or Almacen.objects.first()
                            MovimientoInventario.objects.create(
                                producto=detalle.producto,
                                almacen=almacen,
                                tipo='Salida',
                                cantidad=detalle.cantidad,
                                referencia=f"Factura {factura.codigo_generacion}",
                            )
                            # ¡El stock baja solo gracias al signal!
                        
                    #Si la factura fue recibida por mh detener los eventos en contingencia activos
                    finalizar_contigencia_view(request)
                    break
                else:
                    if envio_response.status_code in [500, 502, 503, 504, 408]: #503, 504
                        print("Error al conectarse al servidor: ", envio_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                    elif envio_response.status_code in [408, 499]: #500, 503
                        print("Error al conectarse al servidor: ", envio_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                    elif envio_response.status_code in [503, 504]: #503, 504
                        print("Error al conectarse al servidor: ", envio_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                    else:#Otro- 400, 500, 502
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                        motivo_otro = True
                        mensaje = f"Error en el envío de la factura: {envio_response.status_code}"
                        print("Error en el envio de la factura: # intento de envio: ", intento)
                        
                    # Esperar antes de siguiente intento
                    error_envio = f"Error en el envío de la factura: {envio_response.status_code}"
                    time.sleep(1) 
                    intento += 1
                    contingencia = True
                    # return JsonResponse({
                    #     "mensaje": error_envio,
                    #     "estado": response_data.get("estado", ""),
                    #     "respuesta": response_data.get("descripcionMsg", "")
                    # })

            except requests.exceptions.RequestException as e:
                error_envio = str(e)
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                time.sleep(1) 
                intento += 1
                print("Error: ", error_envio)
                #return JsonResponse({"error": "Error de conexión al enviar la factura"}, status=500)
            except requests.exceptions.ConnectionError:
                #Error de red del emisor
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
                time.sleep(1) 
                intento += 1
                error_envio = f"Error de conexion: {envio_response.status_code}"
                print("Error: ", error_envio)
            except requests.exceptions.Timeout:
                #Error del emisor
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
                time.sleep(1) 
                intento += 1
                error_envio = f"Se agoto el tiempo de espera: {envio_response.status_code}"
                print("Error: ", error_envio)
            except Exception as e:
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                motivo_otro = True
                error_envio = str(e)
                print(f"Ocurrió un error inesperado: {error_envio}")
                intento += 1
                time.sleep(1) 
    
    # Si la autenticación o el envio fallaron despues de los intentos
    print(f"error auth: {error_autenticacion}, error envio: {error_envio}, crear evento: {crear_evento}")
    if (error_autenticacion or error_envio or crear_evento):
        # Solo crear contingencia si al menos uno de los flujos falló
        if not contingencia_creada and crear_evento :
            print("Crear contingencias y lotes(envio mh)")
            #Verificar si existen contingencias activas
            finalizar_contigencia_view(request)
            
            #Actualizar facturaElectronica
            factura.estado=False
            factura.contingencia = True
            factura.tipomodelo = Modelofacturacion.objects.get(codigo="2") #Cuando es imposible enviar el documento asignar el tipo de modelo "Diferido"
            factura.tipotransmision = TipoTransmision.objects.get(codigo="2") #Cuando es un evento en contingencia guardar tipo de transmision "2-Transmision por Contingencia"
            factura.fecha_modificacion = fecha_actual.date()
            factura.hora_modificacion = fecha_actual.time()
            factura.json_original["identificacion"]["tipoModelo"] = int(factura.tipomodelo.codigo)
            factura.json_original["identificacion"]["tipoOperacion"] = int(factura.tipotransmision.codigo)
            factura.save()
            
            lote_contingencia_dte_view(request, factura_id, tipo_contingencia_obj)
            contingencia_creada = True  #Indica que la contingencia fue creada
        
        # Incrementar reintentos solo si falló la firma
        intentos_modal += 1
        request.session['intentos_reintento'] = intentos_modal
        request.session.modified = True

        # Decidir si mostrar el modal dependiendo de los intentos
        mostrar_modal = intentos_modal < 3
        #return render(request, "documentos/factura_consumidor/template_factura.html", {"factura": factura})
        
    # Envio factura exitosa
    print("Envio response: ", envio_response)
    if (envio_response and envio_response.status_code == 200 and response_data and response_data.get("selloRecibido") is not None) or (contingencia and crear_evento):
        print("Crear archivos")
        #Buscar json
        # Construir la ruta completa al archivo JSON esperado
        json_signed_path = os.path.join(RUTA_JSON_FACTURA.url, f"{factura.numero_control}.json")

        # Verificar si el archivo JSON existe
        if os.path.exists(json_signed_path):
            with open(json_signed_path, "r", encoding="utf-8") as json_file:
                response_data = json.load(json_file)
        else:
            print(f"No se encontró el archivo JSON para la factura: {factura.numero_control}")
        
        # Verificar si el archivo PDF existe
        pdf_signed_path = os.path.join(RUTA_COMPROBANTES_PDF.url, factura.tipo_dte.codigo, 'pdf', f"{str(factura.codigo_generacion).upper()}.pdf")
        os.makedirs(os.path.dirname(pdf_signed_path), exist_ok=True)
        if os.path.exists(pdf_signed_path):
            print("PDF ya existe, devolviendo archivo existente: %s", pdf_signed_path)
            try:
                with open(pdf_signed_path, "rb", encoding="utf-8") as pdf_file:
                    filename=os.path.basename(pdf_signed_path)
            except Exception as e:
                print(f"Error abriendo el archivo PDF existente: {e}")
        else:
            #1.Crear HTML
            html_content = render_to_string('documentos/factura_consumidor/template_factura.html', {"factura": factura}, request=request)

            #Guardar archivo pdf
            print("guardar pdf: ", pdf_signed_path)
            with open(pdf_signed_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)
                
            if pisa_status.err:
                print(f"Error al crear el PDF en {pdf_signed_path}")
            else:
                print(f"PDF guardado exitosamente en {pdf_signed_path}")
            
        
        #Enviar correo
        if factura:
            if factura.contingencia == False and factura.envio_correo == False:
                # enviar_correo_individual_view(request, factura_id, pdf_signed_path, json_signed_path)
                factura.envio_correo = True
            elif factura.contingencia and factura.sello_recepcion is None and factura.envio_correo_contingencia == False :
                # enviar_correo_individual_view(request, factura_id, pdf_signed_path, json_signed_path)
                factura.envio_correo_contingencia = True
            elif factura.contingencia and factura.sello_recepcion and factura.envio_correo == False:
                # enviar_correo_individual_view(request, factura_id, pdf_signed_path, json_signed_path)
                factura.envio_correo = True
            factura.save()
        
        print("-Fin envio DTE:", factura_id)
    if uso_interno:
        if envio_response:
            return JsonResponse(response_data, status=envio_response.status_code)
        else:
            return JsonResponse({"error": "No hubo respuesta del firmador"}, status=500)
    else:
        return redirect(
            f"{reverse('detalle_factura', args=[factura_id])}?"
            f"mostrar_modal={'1' if mostrar_modal else '0'}"
            f"&firma=0"
            f"&envio_mh={'1' if envio_mh else '0'}"
            f"&intentos_modal={intentos_modal}"
            f"&motivo_otro={'1' if motivo_otro else '0'}"
            f"&firmado=0"
            f"&recibido_mh={'1' if factura.firmado else '0'}"
        )
    return JsonResponse({"mensaje": "Factura procesada con éxito"})

    """if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # Obtener los datos del formulario
        data = json.loads(request.body)
        
        # Paso 1: Llamar a la función de generación de factura
        response_generar = generar_factura_view(request)
        if response_generar.status_code != 201:
            return response_generar
        data_generar = json.loads(response_generar.content)
        factura_id = data_generar.get("factura_id")
        
        if not factura_id:
            return JsonResponse({"error": "Error al generar la factura."}, status=400)

        # Paso 2: Llamar a la función de firma de factura
        response_firmar = firmar_factura_view(request, factura_id)
        if response_firmar.status_code != 302:
            return response_firmar
        
        # # Paso 3: Llamar a la función de envío a Hacienda
        # response_enviar = enviar_factura_hacienda_view(request, factura_id)

        # Devolver respuesta final
        detalle = json.loads(response_firmar.content)
        return JsonResponse({
            "mensaje": "Factura generada, firmada y enviada a Hacienda exitosamente",
            "factura_id": factura_id,
            "detalle": detalle
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)"""

# def detalle_factura(request, factura_id):
#     factura = get_object_or_404(FacturaElectronica, id=factura_id)

#     mostrar_modal = request.GET.get('mostrar_modal') == '1'
#     intentos_modal = int(request.GET.get('intentos_modal', 0))
    
#     firma = request.GET.get('firma')
#     envio_mh = request.GET.get('envio_mh')
#     motivo_otro = request.GET.get('motivo_otro', '0')

#     print(f"Detalle | Modal: {mostrar_modal}, firma: {firma}, envio: {envio_mh}, intentos: {intentos_modal}, motivo_otro: {motivo_otro}")

#     return render(request, 'documentos/factura_consumidor/template_factura.html', {
#         'factura': factura,
#         'mostrar_modal': mostrar_modal,
#         'intentos_modal': intentos_modal,
#         'motivo_otro': int(motivo_otro),
#         'firma': firma,
#         'envio_mh': envio_mh,
#         'firmado': factura.firmado,  # ← agregado
#     })

@login_required
def factura_termica(request, factura_id):
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    return render(request, "documentos/factura_consumidor/template_factura_termica.html", {
        "factura": factura,
    })

@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(FacturaElectronica, id=factura_id)

    mostrar_modal = request.GET.get('mostrar_modal') == '1'
    intentos_modal = int(request.GET.get('intentos_modal', 0))
    firma = request.GET.get('firma')
    envio_mh = request.GET.get('envio_mh')
    motivo_otro = request.GET.get('motivo_otro', '0')

    # Verificamos si el emisor tiene activada la impresión térmica
    usa_termica = bool(getattr(factura.dteemisor, "imprime_termica", False))

    print(
        f"Detalle | Modal: {mostrar_modal}, firma: {firma}, envio: {envio_mh}, "
        f"intentos: {intentos_modal}, motivo_otro: {motivo_otro}, termica={usa_termica}"
    )

    # Elegimos template según configuración
    if usa_termica:
        template_name = "documentos/factura_consumidor/template_factura_termica.html"
    else:
        template_name = "documentos/factura_consumidor/template_factura.html"

    return render(request, template_name, {
        "factura": factura,
        "mostrar_modal": mostrar_modal,
        "intentos_modal": intentos_modal,
        "motivo_otro": int(motivo_otro),
        "firma": firma,
        "envio_mh": envio_mh,
        "firmado": factura.firmado,
        
    })

#########################################################################################################
# EVENTO DE INVALIDACION DE DTE
#########################################################################################################

#  HELPERS / UTILIDADES

def _ahora():
    return timezone.now()

def _build_json_invalidacion(factura: FacturaElectronica,
                             tipo_invalidacion: TipoInvalidacion,
                             solicita: str,  # "emisor" o "receptor"
                             codigo_generacion_evento: str) -> dict:
    """
    Arma el JSON del evento de invalidación cumpliendo reglas:
    - fecAnula / horAnula en hora local SV (America/El_Salvador)
    - No antes de la fecha/hora de emisión
    - No en el futuro
    """
    # --- Hora local de SV
    tz_sv = ZoneInfo("America/El_Salvador")
    now_local = timezone.now().astimezone(tz_sv)

    # --- Emisión (combina fecha + hora de la factura)
    # Ajusta si tus campos son strings; aquí asumo date + time nativos
    try:
        emision_date = factura.fecha_emision  # date
        emision_time = factura.hora_emision   # time
        emision_dt_local = datetime.combine(emision_date, emision_time, tzinfo=tz_sv)
    except Exception:
        # Si por alguna razón hora_emision es str:
        # emision_dt_local = datetime.fromisoformat(f"{factura.fecha_emision}T{factura.hora_emision}").astimezone(tz_sv)
        emision_dt_local = now_local - timedelta(minutes=1)

    # --- Clamp: entre [emisión + 1s, ahora - 1s] para evitar futuros
    lower = emision_dt_local + timedelta(seconds=1)
    upper = now_local - timedelta(seconds=1)
    if upper <= lower:
        # Si acabamos de emitir, usa lower (1s después de emisión)
        evento_dt = lower
    else:
        evento_dt = min(max(now_local, lower), upper)

    # Datos base
    emisor = factura.dteemisor
    receptor = factura.dtereceptor
    tipo_est = emisor.tipoestablecimiento

    json_identificacion = {
        "version": int(VERSION_EVENTO_INVALIDACION),
        "ambiente": str(AMBIENTE.codigo),
        "codigoGeneracion": str(codigo_generacion_evento).upper(),
        "fecAnula": evento_dt.date().isoformat(),            # YYYY-MM-DD
        "horAnula": evento_dt.strftime("%H:%M:%S"),          # HH:MM:SS (hora local)
    }

    json_emisor = {
        "nit": str(emisor.nit),
        "nombre": str(emisor.nombre_razon_social),
        "tipoEstablecimiento": str(tipo_est.codigo) if tipo_est else "",
        "nomEstablecimiento": str(tipo_est.descripcion) if tipo_est else "",
        "codEstableMH": str(emisor.codigo_establecimiento or "M001"),
        "codEstable": "0001",
        "codPuntoVentaMH": str(emisor.codigo_punto_venta or "P001"),
        "codPuntoVenta": "0001",
        "telefono": str(emisor.telefono or ""),
        "correo": str(emisor.email or ""),
    }

    json_documento = {
        "tipoDte": str(factura.tipo_dte.codigo),
        "codigoGeneracion": str(factura.codigo_generacion).upper(),
        "selloRecibido": str(factura.sello_recepcion or ""),
        "numeroControl": str(factura.numero_control),
        "fecEmi": str(factura.fecha_emision),
        "tipoDocumento": str(receptor.tipo_documento.codigo) if receptor and receptor.tipo_documento else "",
        "numDocumento": str(receptor.num_documento or ""),
        "nombre": str(receptor.nombre or ""),
        "telefono": str(receptor.telefono or ""),
        "correo": str(receptor.correo or ""),
        "codigoGeneracionR": None,
    }

    # Monto IVA requerido para FE/CCF/FEX
    if factura.tipo_dte.codigo in (COD_CONSUMIDOR_FINAL, COD_CREDITO_FISCAL, COD_FACTURA_EXPORTACION):
        try:
            json_documento["montoIva"] = float(Decimal(str(factura.total_iva)))
        except Exception:
            json_documento["montoIva"] = 0.0
    else:
        json_documento["montoIva"] = None

    json_motivo = {
        "tipoAnulacion": int(tipo_invalidacion.codigo),
        "motivoAnulacion": str(tipo_invalidacion.descripcion),
        "nombreResponsable": str(emisor.nombre_razon_social),
        "tipDocResponsable": str(emisor.tipo_documento.codigo),
        "numDocResponsable": str(emisor.nit),
    }

    # Quién solicita
    if (solicita or "").lower() == "emisor":
        json_motivo["nombreSolicita"] = str(emisor.nombre_razon_social)
        json_motivo["tipDocSolicita"] = str(emisor.tipo_documento.codigo)
        json_motivo["numDocSolicita"] = str(emisor.nit)
    else:
        json_motivo["nombreSolicita"] = str(receptor.nombre or "")
        json_motivo["tipDocSolicita"] = str(receptor.tipo_documento.codigo) if receptor and receptor.tipo_documento else ""
        json_motivo["numDocSolicita"] = str(receptor.num_documento or "")

    return {
        "identificacion": json_identificacion,
        "emisor": json_emisor,
        "documento": json_documento,
        "motivo": json_motivo
    }


@csrf_exempt
def obtener_token_view(request):
    if request.method == "GET":
        try:
            token, token_type = _obtener_token_hacienda()
            return JsonResponse({
                "token_type": token_type,
                "token": token
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

def _obtener_token_hacienda():
    """Autentica y retorna (token, token_type). Lanza excepción con texto claro si falla."""
    emisor = Emisor_fe.objects.first()
    if not emisor:
        raise Exception("No hay emisor configurado.")

    auth_headers = {
        "Content-Type": HEADERS.url_endpoint,
        "User-Agent": HEADERS.valor
    }
    auth_data = {"user": str(emisor.nit), "pwd": str(emisor.clave_publica)}
    resp = requests.post(URL_AUTH.url_endpoint, data=auth_data, headers=auth_headers)

    try:
        data = resp.json()
    except ValueError:
        raise Exception(f"Autenticación MH: respuesta no JSON: {resp.text}")

    if resp.status_code != 200:
        raise Exception(f"Autenticación MH: {data.get('message','Error no especificado')} (HTTP {resp.status_code})")

    body = data.get("body", {})
    token = body.get("token", "")
    token_type = body.get("tokenType", "Bearer")
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    Token_data.objects.update_or_create(
        nit_empresa=str(emisor.nit),
        defaults={
            'password_hacienda': str(emisor.clave_publica),
            'token': token,
            'token_type': token_type,
            'roles': body.get("roles", []),
            'activado': True,
            'fecha_caducidad': timezone.now() + timedelta(days=1)
        }
    )
    return token, token_type

def _firmar_evento_invalidacion(evento: EventoInvalidacion):
    """
    Envía el JSON del evento al firmador.
    Devuelve (ok: bool, respuesta_json: dict)
    """
    if not os.path.exists(CERT_PATH):
        return False, {"error": f"Certificado no encontrado en {CERT_PATH}"}

    emisor = Emisor_fe.objects.first()
    if not emisor:
        return False, {"error": "No hay emisor configurado."}

    # Normalizar a dict
    try:
        if isinstance(evento.json_invalidacion, dict):
            dte_json_obj = evento.json_invalidacion
        else:
            raw = (evento.json_invalidacion or "").lstrip("\ufeff").strip()
            dte_json_obj = json.loads(raw) if raw else {}
    except Exception as e:
        return False, {"error": "JSON de invalidación inválido", "detalle": str(e)}

    payload = {
        "nit": str(emisor.nit),
        "activo": True,
        "passwordPri": str(emisor.clave_privada),
        "dteJson": dte_json_obj,  # IMPORTANTE: dict, no string
    }
    headers = {"Content-Type": CONTENT_TYPE.valor}

    resp = requests.post(FIRMADOR_URL.url_endpoint, json=payload, headers=headers)
    try:
        data = resp.json()
    except Exception:
        data = {"error": "No se pudo parsear JSON", "detalle": resp.text}

    ok = (resp.status_code == 200 and data.get("status") == "OK")
    return ok, data


#  1) CREAR/ACTUALIZAR INVALIDACIÓN
@csrf_exempt
def invalidacion_dte_view(request, factura_id):
    print("ANU: ====== INICIO invalidacion_dte_view ======")
    print(f"ANU: factura_id={factura_id}")

    try:
        factura = get_object_or_404(FacturaElectronica, id=factura_id)
        codigo_generacion_evento = str(uuid.uuid4()).upper()
        # dinámico si lo tomas de un form
        tipo_invalidacion = TipoInvalidacion.objects.get(codigo="2")   # p.e. Rescindir/Anular
        solicita = (request.POST.get("solicita") or request.GET.get("solicita") or "receptor").lower()

        # Obtén/crea el evento
        evento = EventoInvalidacion.objects.filter(factura__codigo_generacion=factura.codigo_generacion).first()
        if not evento:
            evento = EventoInvalidacion.objects.create(
                codigo_generacion=codigo_generacion_evento,
                factura=factura,
                tipo_invalidacion=tipo_invalidacion,
                motivo_anulacion=tipo_invalidacion.descripcion,
                codigo_generacion_r=None,
                solicita_invalidacion=solicita
            )
            print(f"ANU: EventoInvalidacion creado id={evento.id}")
        else:
            # Actualiza datos base
            evento.tipo_invalidacion = tipo_invalidacion
            evento.motivo_anulacion = tipo_invalidacion.descripcion
            evento.codigo_generacion_r = None
            evento.solicita_invalidacion = solicita
            # Mantener su código de generación si ya existe, si no, asignar nuevo
            if not evento.codigo_generacion:
                evento.codigo_generacion = codigo_generacion_evento
            evento.save()
            print(f"ANU: EventoInvalidacion actualizado id={evento.id}")

        # Construye JSON (dict) y guarda
        json_inv = _build_json_invalidacion(factura, tipo_invalidacion, solicita, str(evento.codigo_generacion))
        evento.json_invalidacion = json_inv
        # Guarda quien solicita (para tus columnas auxiliares)
        evento.nombre_solicita = json_inv["motivo"].get("nombreSolicita", "")
        evento.tipo_documento_solicita = json_inv["motivo"].get("tipDocSolicita", "")
        evento.numero_documento_solicita = json_inv["motivo"].get("numDocSolicita", "")
        evento.save()

        print("ANU: JSON de invalidación generado y guardado")
        return redirect(reverse('detalle_factura', args=[factura_id]))

    except Exception as e:
        print("ANU: *** ERROR ***", e)
        return JsonResponse({"error": str(e)}, status=400)

#  2) FIRMAR INVALIDACIÓN
@csrf_exempt
def firmar_factura_anulacion_view(request, factura_id):
    print("ANU: ====== INICIO firmar_factura_anulacion_view ======")
    print(f"ANU: factura_id={factura_id}  method={request.method}")

    evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
    if not evento:
        # Si aún no existe, créalo rápido con defaults
        factura = get_object_or_404(FacturaElectronica, id=factura_id)
        tipo_invalidacion = TipoInvalidacion.objects.get(codigo="2")
        solicita = (request.POST.get("solicita") or request.GET.get("solicita") or "receptor").lower()
        evento = EventoInvalidacion.objects.create(
            codigo_generacion=str(uuid.uuid4()).upper(),
            factura=factura,
            tipo_invalidacion=tipo_invalidacion,
            motivo_anulacion=tipo_invalidacion.descripcion,
            solicita_invalidacion=solicita
        )
        evento.json_invalidacion = _build_json_invalidacion(
            factura, tipo_invalidacion, solicita, str(evento.codigo_generacion)
        )
        evento.save()
        print(f"ANU: EventoInvalidacion creado id={evento.id}")

    ok, firma_resp = _firmar_evento_invalidacion(evento)
    # siempre persistimos la respuesta del firmador
    evento.json_firmado = firma_resp
    evento.save(update_fields=["json_firmado"])

    if ok:
        evento.firmado = True
        evento.save(update_fields=["firmado"])
        # opcional: persistir a disco
        try:
            json_signed_path = os.path.join(
                FACTURAS_FIRMADAS_URL.url,
                f"{str(evento.codigo_generacion).upper()}.json"
            )
            os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
            with open(json_signed_path, "w", encoding="utf-8") as jf:
                json.dump(firma_resp, jf, indent=4, ensure_ascii=False)
            print(f"ANU: JSON firmado guardado en {json_signed_path}")
        except Exception as ex:
            print("ANU: WARN guardando firmado:", ex)

        print("ANU: Firma OK -> redirect detalle")
        return redirect(reverse('detalle_factura', args=[factura_id]))

    print("ANU: *** ERROR FIRMADOR ***", firma_resp)
    return JsonResponse({"error": "Error al firmar la invalidación", "detalle": firma_resp}, status=400)

#  3) ENVIAR INVALIDACIÓN A MH
@csrf_exempt
def enviar_factura_invalidacion_hacienda_view(request, factura_id):
    print("ANU: ====== INICIO enviar_factura_invalidacion_hacienda_view ======")
    print(f"ANU: factura_id={factura_id}")

    try:
        # token
        token, token_type = _obtener_token_hacienda()

        # evento
        evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
        if not evento:
            return JsonResponse({"error": "No existe EventoInvalidacion para la factura."}, status=404)
        if not evento.firmado:
            return JsonResponse({"error": "El evento de invalidación no está firmado."}, status=400)

        # parse firmado
        try:
            firmado_data = evento.json_firmado if isinstance(evento.json_firmado, dict) else json.loads(evento.json_firmado)
        except Exception as e:
            return JsonResponse({"error": "json_firmado inválido", "detalle": str(e)}, status=400)

        documento_token = (firmado_data or {}).get("body", "")
        if not documento_token:
            return JsonResponse({"error": "El firmado no trae 'body' (JWT) para enviar."}, status=400)

        envio_json = {
            "ambiente": str(AMBIENTE.codigo),  # "00" pruebas / "01" prod
            "idEnvio": int(evento.id),
            "version": int(evento.json_invalidacion["identificacion"]["version"]),
            "documento": str(documento_token)   # SOLO el JWT, tal cual (¡no upper!)
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT.valor,
            "Content-Type": CONTENT_TYPE.valor
        }

        resp = requests.post(INVALIDAR_DTE_URL.url_endpoint, headers=headers, json=envio_json)
        print("ANU: envio.status=", resp.status_code)
        print("ANU: envio.text=", resp.text)

        try:
            data = resp.json() if resp.text.strip() else {}
        except ValueError:
            data = {"raw": resp.text or "No content"}

        if resp.status_code == 200:
            evento.sello_recepcion = data.get("selloRecibido", "")
            evento.recibido_mh = True
            # Anexar respuesta MH al JSON original del evento
            base = evento.json_invalidacion if isinstance(evento.json_invalidacion, dict) else {}
            evento.json_invalidacion = {**base, "jsonRespuestaMh": data}
            evento.estado = True
            evento.save()

            # Reingreso a inventario (si corresponde a tu modelo de negocio)
            factura = evento.factura
            try:
                devolucion = DevolucionVenta.objects.create(
                    num_factura=factura.numero_control,
                    motivo="Devolución automática por invalidación",
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
                    
            except Exception as inv_ex:
                print("ANU: WARN reingreso inventario:", inv_ex)

            return JsonResponse({"mensaje": "Invalidación enviada y recibida por MH", "respuesta": data})

        # Error MH
        evento.estado = False
        evento.save(update_fields=["estado"])
        return JsonResponse({"error": "Error al invalidar en MH", "status": resp.status_code, "detalle": data},
                            status=resp.status_code)

    except Exception as e:
        print("ANU: *** ERROR ***", e)
        return JsonResponse({"error": str(e)}, status=400)


#############################################################################
# Invalidación Sujeto excluido
#############################################################################
@csrf_exempt    
def invalidacion_dte_sujeto_excluido_view(request, factura_id):
    # Generar json, firmar, enviar a MH
    codigo_generacion_invalidacion = str(uuid.uuid4()).upper()
    print("-Codigo generacion evento invalidacion ", codigo_generacion_invalidacion)
    factura_invalidar = FacturaSujetoExcluidoElectronica.objects.get(id=factura_id)  # Buscar DTE a invalidar

    # Tipo Invalidacion (se asume código "2" como ejemplo)
    tipo_invalidacion = TipoInvalidacion.objects.get(codigo="2")
    # Quién solicita invalidar el DTE: emisor o receptor (este valor es dinámico)
    solicitud = "receptor"
    
    try: 
        if factura_invalidar is not None:
            print("-Factura a invalidar encontrada", factura_invalidar)
            # Buscar si la factura ya tiene un evento de invalidación
            evento_invalidacion = EventoInvalidacion.objects.filter(
                facturaSujetoExcluido__codigo_generacion=factura_invalidar.codigo_generacion
            ).first()
            print("-Evento invalidacion: ", evento_invalidacion)
            # Si no existe, se crea el registro; de lo contrario, se actualiza
            if evento_invalidacion is None:
                evento_invalidacion = EventoInvalidacion.objects.create(
                    codigo_generacion=codigo_generacion_invalidacion,
                    facturaSujetoExcluido=factura_invalidar,
                    tipo_invalidacion=tipo_invalidacion,
                    motivo_anulacion=tipo_invalidacion.descripcion,
                    solicita_invalidacion=solicitud,
                )
            else:
                evento_invalidacion.tipo_invalidacion = tipo_invalidacion
                evento_invalidacion.motivo_anulacion = tipo_invalidacion.descripcion
                evento_invalidacion.codigo_generacion_r = factura_invalidar.codigo_generacion
                evento_invalidacion.solicita_invalidacion = solicitud
                evento_invalidacion.save()
            
            fecha_actual = obtener_fecha_actual()
            # Armar el JSON de identificación
            json_identificacion_inv = {
                "version": int(VERSION_EVENTO_INVALIDACION),  # Version vigente, por ejemplo 2
                "ambiente": str(AMBIENTE.codigo),  # O el valor que corresponda
                "codigoGeneracion": str(evento_invalidacion.codigo_generacion).upper(),
                "fecAnula": str(fecha_actual.strftime('%Y-%m-%d')),
                "horAnula": str(datetime.now().strftime('%H:%M:%S'))
            }
            
            # Armar JSON para "emisor"
            tipo_establecimiento = TiposEstablecimientos.objects.get(
                codigo=evento_invalidacion.facturaSujetoExcluido.dteemisor.tipoestablecimiento.codigo
            )
            json_emisor_inv = {
                "nit": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nit),
                "nombre": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nombre_razon_social),
                "tipoEstablecimiento": str(tipo_establecimiento.codigo),
                "nomEstablecimiento": str(tipo_establecimiento.descripcion),
                "codEstableMH": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.codigo_establecimiento or "M001"),
                "codEstable": "0001",
                "codPuntoVentaMH": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.codigo_punto_venta or "P001"),
                "codPuntoVenta": "0001",
                "telefono": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.telefono),
                "correo": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.email)
            }
            
            # Armar JSON para "documento"
            json_documento_inv = {
                "tipoDte": str(evento_invalidacion.facturaSujetoExcluido.tipo_dte.codigo),
                "codigoGeneracion": str(factura_invalidar.codigo_generacion).upper(),
                "selloRecibido": str(factura_invalidar.sello_recepcion),
                "numeroControl": str(factura_invalidar.numero_control),
                "fecEmi": str(factura_invalidar.fecha_emision),
                "tipoDocumento": str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.tipo_documento.codigo),
                "numDocumento": str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.num_documento),
                "nombre": str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.nombre),
                "telefono": str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.telefono),
                "correo": str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.email) 
            }
            
            # Armar JSON para "motivo"
            json_motivo_inv = {
                "tipoAnulacion": int(evento_invalidacion.tipo_invalidacion.codigo),
                "motivoAnulacion": str(evento_invalidacion.motivo_anulacion),
                "nombreResponsable": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nombre_razon_social),
                "tipDocResponsable": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.tipo_documento.codigo),
                "numDocResponsable": str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nit),
            }
            
            # Ajustes según el DTE a invalidar
            tipo_dte_invalidar = evento_invalidacion.facturaSujetoExcluido.tipo_dte.codigo
            if tipo_dte_invalidar in [COD_CONSUMIDOR_FINAL, COD_CREDITO_FISCAL, COD_FACTURA_EXPORTACION]:
                json_documento_inv["montoIva"] = float(factura_invalidar.total_operaciones)
            else:
                json_documento_inv["montoIva"] = None
            
            if int(evento_invalidacion.tipo_invalidacion.codigo) == COD_TIPO_INVALIDACION_RESCINDIR and \
                tipo_dte_invalidar not in [COD_NOTA_CREDITO, COD_COMPROBANTE_LIQUIDACION]:
                json_documento_inv["codigoGeneracionR"] = None
            else:
                json_documento_inv["codigoGeneracionR"] = None
                print("codGeneracionR", json_documento_inv["codigoGeneracionR"])       
            
            # Asignar información de quién solicita la invalidación según selección (emisor o receptor)
            if solicitud == EMI_SOLICITA_INVALIDAR_DTE:
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nombre_razon_social)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dteemisor.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dteemisor.nit)
            elif solicitud == REC_SOLICITA_INVALIDAR_DTE:
                
                
                
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.nombre)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.facturaSujetoExcluido.dtesujetoexcluido.num_documento)
            
            # Armado del JSON completo
            json_completo = {
                "identificacion": json_identificacion_inv,
                "emisor": json_emisor_inv,
                "documento": json_documento_inv,
                "motivo": json_motivo_inv
            }
            
            # Se convierte a JSON (opcional) y se almacena en el campo correspondiente
            evento_invalidacion.json_invalidacion = json_completo
            print("-Json invalidacion modificado: ", json_completo)
            evento_invalidacion.nombre_solicita = json_motivo_inv["nombreSolicita"]
            evento_invalidacion.tipo_documento_solicita = json_motivo_inv["tipDocSolicita"]
            evento_invalidacion.numero_documento_solicita = json_motivo_inv["numDocSolicita"]
            evento_invalidacion.save()
        else:
            return JsonResponse({
                "error": "Error DTE a invalidar no encontrado",
                "detalle": "La factura no existe"
            }) 
        return redirect(reverse('detalle_factura', args=[factura_id]))
    except Exception as e:
        nuevo_codigo_generacion = str(uuid.uuid4()).upper()
        print(f"Error al generar el evento de invalidación: {e}")
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
def firmar_factura_sujeto_excluido_anulacion_view(request, factura_id):

    """
    Firma la factura y, si ya está firmada, la envía a Hacienda.
    """
    print("-Inicio firma invalidacion DTE - id factura ", factura_id)
    #Buscar factura a firmar
    evento_invalidacion = EventoInvalidacion.objects.filter(facturaSujetoExcluido__id=factura_id).first()
    #invalidacion = evento_invalidacion

    token_data = Token_data.objects.filter(activado=True).first()
    if not token_data:
        return JsonResponse({"error": "No hay token activo registrado en la base de datos."}, status=401)

    if not os.path.exists(CERT_PATH):
        return JsonResponse({"error": "No se encontró el certificado en la ruta especificada."}, status=400)
    
    # Verificar y formatear el JSON original de la factura
    try:
        if isinstance(evento_invalidacion.json_invalidacion, dict):
            dte_json_str = json.dumps(evento_invalidacion.json_invalidacion, separators=(',', ':'))
        else:
            json_obj = json.loads(evento_invalidacion.json_invalidacion)
            dte_json_str = json.dumps(json_obj, separators=(',', ':'))
    except Exception as e:
        return JsonResponse({
            "error": "El JSON original de la factura no es válido",
            "detalle": str(e)
        }, status=400)
    
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    emisor = factura.dteemisor or _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({"error": "No se encontró emisor para firmar este DTE."}, status=400)
    
        # Construir el payload con los parámetros requeridos
    payload = {
        "nit": emisor.nit,   # Nit del contribuyente
        "activo": True,            # Indicador activo
        "passwordPri": emisor.clave_privada,   # Contraseña de la llave privada
        "dteJson": evento_invalidacion.json_invalidacion    # JSON del DTE como cadena
    }

    headers = {"Content-Type": CONTENT_TYPE.valor}

    try:
        response = requests.post(FIRMADOR_URL.url_endpoint, json=payload, headers=headers)
        
        # Capturamos la respuesta completa
        try:
            response_data = response.json()
        except Exception as e:
            # En caso de error al parsear el JSON, se guarda el texto crudo
            response_data = {"error": "No se pudo parsear JSON", "detalle": response.text}
        
        # Guardar toda la respuesta en la factura para depuración (incluso si hubo error)
        evento_invalidacion.json_firmado = response_data
        evento_invalidacion.firmado = True
        evento_invalidacion.save()

        # Verificar si la firma fue exitosa
        if response.status_code == 200 and response_data.get("status") == "OK":
            # (Opcional) Guardar el JSON firmado en un archivo
            json_signed_path = f"{FACTURAS_FIRMADAS_URL.url}{evento_invalidacion.codigo_generacion}.json"
            os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
            with open(json_signed_path, "w", encoding="utf-8") as json_file:
                json.dump(response_data, json_file, indent=4, ensure_ascii=False)
            print("-Fin firma invalidacion DTE - id factura ", factura_id)
            #enviar_factura_invalidacion_hacienda_view(factura_id)
            return redirect(reverse('detalle_factura', args=[factura_id]))
        else:
            # Se devuelve el error completo recibido
            return JsonResponse({"error": "Error al firmar la factura", "detalle": response_data}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Error de conexión con el firmador", "detalle": str(e)}, status=500)

@csrf_exempt
def enviar_factura_sujeto_excluido_invalidacion_hacienda_view(request, factura_id):
    print("-Inicio enviar invalidacion a MH")

    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    emisor = factura.dteemisor or _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({"error": "No se encontró emisor para firmar este DTE."}, status=400)


    # Paso 1: Autenticación contra el servicio de Hacienda
    nit_empresa = emisor.nit
    pwd = emisor.clave_publica
    auth_url = URL_AUTH.url_endpoint
    auth_headers = {
        "Content-Type": HEADERS.url_endpoint,
        "User-Agent": HEADERS.valor
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}

    #try:
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
    try:
        auth_response_data = auth_response.json()
    except ValueError:
        return JsonResponse({
            "error": "Error al decodificar la respuesta de autenticación",
            "detalle": auth_response.text
        }, status=500)
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
    else:
        return JsonResponse({
            "error": "Error en la autenticación",
            "detalle": auth_response_data.get("message", "Error no especificado")
        }, status=auth_response.status_code)
    #except requests.exceptions.RequestException as e:
        #return JsonResponse({
            #"error": "Error de conexión con el servicio de autenticación",
            #"detalle": str(e)
        #}, status=500)

    # Paso 2: Enviar la factura firmada a Hacienda
    #factura = get_object_or_404(FacturaElectronica, id=factura_id)
    evento_invalidacion = EventoInvalidacion.objects.filter(facturaSujetoExcluido__id=factura_id).first()
    # if not factura.firmado:
    #     return JsonResponse({"error": "La factura no está firmada"}, status=400)

    token_data_obj = Token_data.objects.filter(activado=True).first()
    if not token_data_obj or not token_data_obj.token:
        return JsonResponse({"error": "No hay token activo para enviar la factura"}, status=401)

    # --- Validación y limpieza del documento firmado ---
    documento_str = evento_invalidacion.json_firmado
    if not isinstance(documento_str, str):
        documento_str = json.dumps(documento_str)

    # Eliminar posibles caracteres BOM y espacios innecesarios
    documento_str = documento_str.lstrip('\ufeff').strip().upper()
    print("Json invalidacion firmado: ", documento_str)

    try:
        if isinstance(evento_invalidacion.json_firmado, str):
            firmado_data = json.loads(evento_invalidacion.json_firmado)
        else:
            firmado_data = evento_invalidacion.json_firmado
    except Exception as e:
        return JsonResponse({
            "error": "Error al parsear el documento firmado",
            "detalle": str(e)
        }, status=400)

    documento_token = firmado_data.get("body", "")
    if not documento_token:
        return JsonResponse({
            "error": "El documento firmado no contiene el token en 'body'"
        }, status=400)

    documento_token = documento_token.strip()  # Limpiar espacios innecesarios

    envio_json = {
        "ambiente": "01",  # "00" para Pruebas; "01" para Producción
        "idEnvio": int(evento_invalidacion.id),
        "version": int(evento_invalidacion.json_invalidacion["identificacion"]["version"]),
        "documento": str(documento_token) #Enviamos solo el JWT firmado
    }

    envio_headers = {
        "Authorization": str(f"Bearer {token_data_obj.token}"),
        "User-Agent": USER_AGENT.valor,
        "Content-Type": CONTENT_TYPE.valor
    }
        
    try:
        envio_response = requests.post(
            INVALIDAR_DTE_URL.url_endpoint,
            headers=envio_headers,
            json=envio_json
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
            print("Respuesta MH ", envio_response.status_code)
            evento_invalidacion.sello_recepcion = response_data.get("selloRecibido", "")
            evento_invalidacion.recibido_mh=True
            #Guardar respuesta de MH en json_original
            json_response_data = {
                "jsonRespuestaMh": response_data
            }
            json_original = evento_invalidacion.json_invalidacion
            
            #Combinar jsons
            json_nuevo = json_original | json_response_data
            #Convertir diccionario en json
            json_respuesta_mh = json.dumps(json_nuevo)
            #Al convertir un diccionario en json se guarda como un string, por lo que se debe convertir a json (loads)
            json_original_campo = json.loads(json_respuesta_mh)
            evento_invalidacion.json_invalidacion = json_original_campo
            evento_invalidacion.estado=True
            evento_invalidacion.save()
            print("-Fin enviar invalidacion a MH")
            respuestaMh = json_response_data["jsonRespuestaMh"]["descripcionMsg"]
            print("-Detalle RespuestaMH ", json_response_data["jsonRespuestaMh"]["descripcionMsg"])

            # ---------------------------------------------------
            #  AGREGAR EL PRODUCTO AL INVENTARIO (Entrada)
            # ---------------------------------------------------
            factura = evento_invalidacion.facturaSujetoExcluido  # asumiendo ForeignKey desde EventoInvalidacion
             # Crear la devolución de venta
            # devolucion = DevolucionVenta.objects.create(
            #     num_factura=factura.numero_control,
            #     motivo="Devolución automática por invalidación múltiple",
            #     estado="Aprobada",
            #     usuario=request.user.username if request.user.is_authenticated else None
            # )
            # for detalle in factura.detalles.all():
            #     DetalleDevolucionVenta.objects.create(
            #         devolucion=devolucion,
            #         producto=detalle.producto,
            #         cantidad=detalle.cantidad,
            #         motivo_detalle="Reingreso automático por invalidación"
            #     )
            #     if detalle is not None and detalle.producto.almacenes.exists():
            #         almacen = detalle.producto.almacenes.first() or Almacen.objects.first()
            #         MovimientoInventario.objects.create(
            #             producto=detalle.producto,
            #             almacen=almacen,
            #             tipo='Entrada',
            #             cantidad=detalle.cantidad,
            #             referencia=f"Invalidación Factura {factura.codigo_generacion}",
            #         )
                            
            #     # Ajuste de stock atómico
            #     Producto.objects.filter(pk=detalle.producto.pk).update(
            #         stock=F('stock') + detalle.cantidad
            #     )

            return JsonResponse({
                "mensaje": "Factura invalidada con éxito",
                "respuesta": response_data
            })

        else:
            evento_invalidacion.estado=False
            evento_invalidacion.save()
            print("-Detalle RespuestaMH ", response_data["descripcionMsg"])
            return JsonResponse({
                "error": "Error al invalidar la factura",
                "status": envio_response.status_code,
                "detalle": response_data
            }, status=envio_response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Error de conexión con Hacienda",
            "detalle": str(e)
        }, status=500)

#############################################################################

@csrf_exempt
def invalidar_varias_dte_view(request):
    if request.method == "POST":
        # Se espera recibir una lista de IDs en el parámetro 'factura_ids'
        factura_ids = request.POST.getlist('factura_ids')
        results = []
        for factura_id in factura_ids:
            try:
                # Llamar a la función de invalidación del DTE
                response_evento_invalidacion = invalidacion_dte_view(request, factura_id)
                if response_evento_invalidacion.status_code != 302:
                    results.append({
                        "factura_id": factura_id,
                        "mensaje": "Error en invalidación",
                        "detalle": response_evento_invalidacion.content.decode()
                    })
                    continue

                # Llamar a la función de firma
                response_firma = firmar_factura_anulacion_view(request, factura_id)
                if response_firma.status_code != 302:
                    results.append({
                        "factura_id": factura_id,
                        "mensaje": "Error en firma",
                        "detalle": response_firma.content.decode()
                    })
                    continue

                # Llamar a la función de envío
                response_envio = enviar_factura_invalidacion_hacienda_view(request, factura_id)
                
                # Consultar el estado final del evento de invalidación
                evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
                if evento:
                    if evento.estado:
                        mensaje = "Factura invalidada con éxito"

                        factura = get_object_or_404(FacturaElectronica, id=factura_id)
                        # Crear la devolución de venta
                        devolucion = DevolucionVenta.objects.create(
                            num_factura=factura.numero_control,
                            motivo="Devolución automática por invalidación múltiple",
                            estado="Aprobada",
                            usuario=request.user.username if request.user.is_authenticated else None
                        )
                        # Registrar cada detalle y reingresar stock
                        for detalle in factura.detalles.all():
                            DetalleDevolucionVenta.objects.create(
                                devolucion=devolucion,
                                producto=detalle.producto,
                                cantidad=detalle.cantidad,
                                motivo_detalle="Reingreso automático por invalidación"
                            )
                            if detalle is not None and detalle.producto.almacenes.exists():
                                almacen = detalle.producto.almacenes.first() or Almacen.objects.first()
                                MovimientoInventario.objects.create(
                                    producto=detalle.producto,
                                    almacen=almacen,
                                    tipo='Entrada',
                                    cantidad=detalle.cantidad,
                                    referencia=f"Reingreso invalidación Factura {factura.numero_control}"
                                )
                                
                                print("INVALIDAR VARIAS DTE " )
                                # Ajuste de stock atómico
                                Producto.objects.filter(pk=detalle.producto.pk).update(
                                    stock=F('stock') + detalle.cantidad
                                )

                    else:
                        mensaje = "No se pudo invalidar la factura"
                else:
                    mensaje = "No se encontró el evento de invalidación"

                try:
                    detalle = json.loads(response_envio.content)
                except Exception:
                    detalle = response_envio.content.decode()
                
                results.append({
                    "factura_id": factura_id,
                    "mensaje": mensaje,
                    "detalle": detalle
                })
            except Exception as e:
                results.append({
                    "factura_id": factura_id,
                    "mensaje": "Error inesperado",
                    "detalle": str(e)
                })
        return JsonResponse({"results": results})
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def invalidar_dte_unificado_view(request, factura_id):
    try:
        factura = get_object_or_404(FacturaElectronica, id=factura_id)

        # ✅ Verificar si ya tiene un evento de invalidación
        if factura.dte_invalidacion.exists():
            evento = factura.dte_invalidacion.first()
            return JsonResponse({
                "mensaje": "La factura ya se encuentra invalidada",
                "detalle": {
                    "codigoGeneracion": str(evento.codigo_generacion),
                    "fecha_anulacion": evento.fecha_anulacion,
                    "hora_anulacion": evento.hora_anulacion,
                    "motivo": evento.motivo_anulacion,
                    "recibido_mh": evento.recibido_mh,
                    "sello": evento.sello_recepcion,
                    "estado": evento.estado,
                    "json_invalidacion": evento.json_invalidacion,
                    "json_firmado": evento.json_firmado,
                }
            })
        
        response_evento_invalidacion = invalidacion_dte_view(request, factura_id)
        if response_evento_invalidacion.status_code != 302 :
            return response_evento_invalidacion
        
        # ---------------------------------
        # Paso 2: Llamar a la función de firma de la factura de invalidación
        # ---------------------------------
        response_firma = firmar_factura_anulacion_view(request, factura_id)
        if response_firma.status_code != 302:
            return response_firma
        
        # ---------------------------------
        # Paso 3: Llamar a la función que envía la factura firmada a Hacienda
        # ---------------------------------
        response_envio = enviar_factura_invalidacion_hacienda_view(request, factura_id)
        
        # ---------------------------------
        # Consultar el estado final y preparar el mensaje de respuesta
        # ---------------------------------
        evento = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
        if evento:
            if evento.estado:
                mensaje = "Factura invalidada con éxito"
            else:
                mensaje = "No se pudo invalidar la factura"
        else:
            mensaje = "No se encontró el evento de invalidación para la factura"
        
        try:
            detalle = json.loads(response_envio.content)
        except Exception:
            detalle = response_envio.content.decode()
        
        return JsonResponse({
            "mensaje": mensaje,
            "detalle": detalle
        })
    
    except Exception as e:
        print("Error en el proceso unificado:", e)
        return JsonResponse({"error": str(e)}, status=400)


#############################################################################################################
# VISTAS COMPLEMENTARIAS AJAX
######################################################################################

def seleccion_descuento_ajax(request):
    descuento_porcentaje = request.GET.get("descuento_id")
    print("-Descuento url: ", descuento_porcentaje)
    return JsonResponse({'descuento': descuento_porcentaje})

def agregar_formas_pago_ajax(request):
    print("-Fromas de pago view: ", request)
    #data = request.data
    global formas_pago
    formas_pago = []
    
    try:
        formas_pago_id = request.GET.get("fp_id")#request.GET.get("fp_id")
        num_referencia = request.GET.get("num_ref", None)
        
        if num_referencia == "":
            num_referencia = None
            
        monto_fp = request.GET.get("monto_fp", 0)#request.GET.get("monto_fp", "0")
        periodo_plazo = request.GET.get("periodo", None)
        condicion_operacion = request.GET.get("condicion_op", 1)

        saldo_favor = request.GET.get("saldo_favor_input", "0")
        tiene_saldoF = False
        
        monto = Decimal("0.00")
        formaPago = None
        
        if formas_pago_id is not None and formas_pago_id !=[]:
            for fp in formas_pago_id:
                try:
                    formaPago = FormasPago.objects.get(id=fp)
                    if saldo_favor is not None and saldo_favor !="":
                        saldo = Decimal(saldo_favor)
                        if  saldo.compare(Decimal("0.00")) > 0:
                            tiene_saldoF = True
                            formaPago = FormasPago.objects.get(codigo="99")
                    else:
                        saldo_favor = Decimal("0.00")
                except ConversionSyntax:
                    print(f"Error: '{saldo}' no es un valor decimal válido.")
                
                if formaPago is not None:
                    formas_pago_json  = {
                        "codigo": str(formaPago.codigo),
                        "montoPago": float(monto_fp),
                        "referencia": str(num_referencia),
                        "plazo": None
                    }
                    
                    if tiene_saldoF:
                        formas_pago_json["codigo"] = str(formaPago.codigo)
                    if condicion_operacion is not None and int(condicion_operacion) > 0 and int(condicion_operacion) == int(ID_CONDICION_OPERACION):
                        formas_pago_json["codigo"] = None
                        formas_pago_json["montoPago"] = float(monto)
                        formas_pago_json["plazo"] = str(Plazo.objects.get(id=1).codigo) #Plazo por días
                        formas_pago_json["periodo"] = int(periodo_plazo)
                    else:
                        formas_pago_json["periodo"] = None
                        
                    if formas_pago_json["codigo"] == "01": #Forma d pago billetes y monedas
                        formas_pago_json["referencia"] = None
                    
                    formas_pago.append(formas_pago_json)
                    
                    return JsonResponse({"No Permitido": "El monto ingresado es mayor que el total a pagar" })
            print("-Formas de pago seleccionadas: ", formas_pago)
        
        return JsonResponse({'formasPago': formas_pago})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

def agregar_formas_pago_api(request):
    print("-Fromas de pago api: ", request)
    data = request.data
    global formas_pago
    formas_pago = []
    
    try:
        formas_pago_id = data.get("fp_id", [])
        print("-Id forma de pago: ", formas_pago_id)
        num_referencia = data.get("num_ref", None)
        
        if num_referencia == "":
            num_referencia = None
            
        monto_fp = data.get("monto_fp", 0)#request.GET.get("monto_fp", "0")
        periodo_plazo = data.get("periodo", None)
        condicion_operacion = data.get("condicion_operacion", 0)

        saldo_favor = data.get("saldo_favor_input", None)
        tiene_saldoF = False
        
        monto = Decimal("0.00")
        formaPago = None
        
        print("-Inicio formas de pago: ", formas_pago_id)
        if formas_pago_id is not None and formas_pago_id !=[]:
            print("recorrer formas de pago seleccionadas")
            for fp in formas_pago_id:
                try:
                    formaPago = FormasPago.objects.get(id=fp)
                    print("Saldo favor = ", saldo_favor)
                    if saldo_favor is not None and saldo_favor !="":
                        saldo = Decimal(saldo_favor)
                        if  saldo.compare(Decimal("0.00")) > 0:
                            tiene_saldoF = True
                            formaPago = FormasPago.objects.get(codigo="99")
                    else:
                        saldo_favor = Decimal("0.00")
                    print("Forma de pago encontrada: ", formaPago)
                except ConversionSyntax:
                    print(f"Error: '{saldo}' no es un valor decimal válido.")
                
                print("-Generar json fp: ", formaPago)
                if formaPago is not None:
                    formas_pago_json  = {
                        "codigo": str(formaPago.codigo),
                        "montoPago": float(monto_fp),
                        "referencia": str(num_referencia),
                        "plazo": None
                    }
                
                    if tiene_saldoF:
                        formas_pago_json["codigo"] = str(formaPago.codigo)
                    if condicion_operacion is not None and int(condicion_operacion) > 0 and int(condicion_operacion) == int(ID_CONDICION_OPERACION):
                        formas_pago_json["codigo"] = None
                        formas_pago_json["montoPago"] = float(monto)
                        formas_pago_json["plazo"] = str(Plazo.objects.get(id=1).codigo) #Plazo por días
                        formas_pago_json["periodo"] = int(periodo_plazo)
                    else:
                        formas_pago_json["periodo"] = None
                        
                    if formas_pago_json["codigo"] == "01": #Forma d pago billetes y monedas
                        formas_pago_json["referencia"] = None
                    
                    formas_pago.append(formas_pago_json)
                    print("-Agregar forma pago: ", formas_pago)
                    return formas_pago
                    
            print("-Formas de pago seleccionadas: ", formas_pago)
        
        return Response({'formasPago': formas_pago})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    
def agregar_docs_relacionados_ajax(request):
    #NC y ND permiten relacionar los documenos: 03 y 07
    try:
        print("-Inicio generar documentos relaciondos")
        global tipo_dte_doc_relacionar
        
        #tipo_dte = request.GET.get("tipo_dte", None)
        tipo_doc_relacionar = request.GET.get("tipo_doc", None)
        numero_documento = request.GET.get("num_documento", None)
        
        global documentos_relacionados
        
        docs_permitidos = 50
        #tipo_dte_ob = Tipo_dte.objects.get(codigo=tipo_dte)
        factura_relacionar = None
        tipo_documento = None
        
        #Si supera el limite de documentos relacionados detener el proceso
        if documentos_relacionados is not None and documentos_relacionados !=[]:
            for idx, docR in enumerate(documentos_relacionados, start=1):
                if idx > docs_permitidos:
                    return JsonResponse({"error": "Limite de documentos relacionados: " }, {docs_permitidos})
                
                #No permitir relacionar documentos de diferentes tipos, es decir, si es NC no se pueden asociar CCF y NR al mismo tiempo
                
            print("Documentos relacionados agregados: ", idx)
        
        #Buscar documento relacionado
        if tipo_doc_relacionar:
            if tipo_doc_relacionar == RELACIONAR_DOC_FISICO:
                # Q permite realizar busqueda por varios campos
                #factura_relacionar = FacturaElectronica.objects.get( Q(numero_control=numero_documento) & (Q(tipo_dte.codigo == "03") | Q(tipo_dte.codigo == "07")) )
                factura_relacionar = FacturaElectronica.objects.get( numero_control=numero_documento )
            else:#documento electronico
                #factura_relacionar = FacturaElectronica.objects.get( Q(codigo_generacion=numero_documento) & (Q(tipo_dte.codigo == "03") | Q(tipo_dte.codigo == "07")) )
                factura_relacionar = FacturaElectronica.objects.get( codigo_generacion=numero_documento )
        
        #Si existe el documento generar estructura de documentos relacionados
        if factura_relacionar is not None and factura_relacionar.estado and factura_relacionar.sello_recepcion is not None and factura_relacionar.sello_recepcion !="":
            tipo_documento = factura_relacionar.tipo_dte.codigo
            tipo_dte_doc_relacionar = tipo_documento
            #Crear json
            documento_relacionado_json  = {
                "tipoDocumento": str(tipo_documento) if str(tipo_documento) else None,
                "tipoGeneracion": int(tipo_doc_relacionar),
                "numeroDocumento": str(numero_documento),
                "fechaEmision": str(factura_relacionar.fecha_emision)
            }
            documentos_relacionados.append(documento_relacionado_json)
            print("-Lista documentos relacionados: ", documentos_relacionados)
            
            #Generar vista
            #Convertir json a diccionario para acceder a los campos
            json_doc_relacionado = factura_relacionar.json_original
            total_pagar_doc_r = json_doc_relacionado["resumen"]["totalPagar"]
            print("Total a pagar del documento relacionado: ", total_pagar_doc_r)
            #eturn render(request, 'generar_dte.html', {'total_pagar_doc_r: ', total_pagar_doc_r})

        elif factura_relacionar is None:
            notificar_respuesta = "Error: Documento a relacionar no encontrado."
        else:
            notificar_respuesta = "Verifica que el DTE este vigente para poder relacionarlo."
            
        return JsonResponse(render(request, 'generar_dte_ajuste.html', {'total_pagar_doc_r: ', total_pagar_doc_r}))
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    
######################################################
# GENERACION DE NOTA DE CREDITO Y DEBITO
######################################################
@csrf_exempt
@transaction.atomic
def generar_documento_ajuste_view(request):
    print("Inicio generar dte ajuste (NC - ND)")
    cod_generacion = str(uuid.uuid4()).upper()
        
    if request.method == 'GET':
        global productos_ids_r
        productos_ids_r = []
        
        global cantidades_prod_r
        cantidades_prod_r = []
        
        global documentos_relacionados 
        documentos_relacionados = []
        
        global descuentos_r
        descuentos_r = []
    
        #tipo_dte = request.GET.get('tipo_dte', '05')
        global tipo_documento_dte
        tipo_dte = tipo_documento_dte
        emisor_obj = _get_emisor_for_user(request.user, estricto=False)
        if emisor_obj:
            nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
        else:
            nuevo_numero = ""
        codigo_generacion = cod_generacion
        fecha_generacion = timezone.now().date()
        hora_generacion = timezone.now().strftime('%H:%M:%S')

        emisor_data = {
            "nit": emisor_obj.nit if emisor_obj else "",
            "nombre_razon_social": emisor_obj.nombre_razon_social if emisor_obj else "",
            "direccion_comercial": emisor_obj.direccion_comercial if emisor_obj else "",
            "telefono": emisor_obj.telefono if emisor_obj else "",
            "email": emisor_obj.email if emisor_obj else "",
        } if emisor_obj else None

        receptores = Receptor_fe.objects.values("id", "num_documento", "nombre")
        #productos = Producto.objects.all()
        productos = obtener_listado_productos_view(request)
        tipooperaciones = CondicionOperacion.objects.all()
        tipoDocumentos = Tipo_dte.objects.filter( Q(codigo=COD_NOTA_CREDITO) | Q(codigo=COD_NOTA_DEBITO))
        tipoItems = TipoItem.objects.all()
        descuentos = Descuento.objects.all()
        formasPago = FormasPago.objects.all()
        tipoGeneracionDocumentos = TipoGeneracionDocumento.objects.all()

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
        return render(request, "generar_dte_ajuste.html", context)

    elif request.method == 'POST':
        try:
            items_permitidos = 2000
            data = json.loads(request.body)
            docsRelacionados = []#Acumular los documentos relacionados
            contingencia = False
            # Datos básicos
            numero_control = data.get('numero_control', '')
            codigo_generacion = data.get('codigo_generacion', '')
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
            
            tipo_doc_relacionar = data.get("documento_seleccionado", [])
            documento_relacionado = data.get("documento_relacionado", [])
            if documento_relacionado is None or documento_relacionado == []:
                documento_relacionado = None
            porcentaje_descuento = data.get("descuento_select", "0")
            porcentaje_descuento_producto = 0
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
            facturasRelacionadas = data.get("facturas_relacionadas", [])
            #Descuento gravado
            descu_gravado = data.get("descuento_gravado", "0")
            #Total descuento = descuento por item + descuento global gravado
            monto_descuento = data.get("monto_descuento", "0")
            print(f"monto descuento gravado = {descu_gravado}")
            
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
            #Obtener el descuento agregado en los productos
            descuentos_aplicados = data.get("descuento_select", [])
            
            if productos_ids_r is not None and len(productos_ids_r)>0:
                for idProd in productos_ids_r:
                    productos_ids.append(idProd)
                
            if cantidades_prod_r is not None and len(cantidades_prod_r)>0:
                for c in cantidades_prod_r:
                    cantidades.append(c)
            
            if descuentos_r is not None and len(descuentos_r)>0:
                for d in descuentos_r:
                    descuentos_aplicados.append(d)
            print("descuento aplicado: ", descuentos_aplicados)
            # En este caso, se asume que el descuento por producto es 0 (se aplica globalmente)
            
            if numero_control:
                numero_control = NumeroControl.obtener_numero_control(tipo_dte)
                print(numero_control)
            if not codigo_generacion:
                codigo_generacion = str(uuid.uuid4()).upper()

            # Obtener emisor
            emisor_obj = _get_emisor_for_user(request.user, estricto=False)
            if not emisor_obj:
                return JsonResponse({"error": "No hay emisores registrados en la base de datos"}, status=400)
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
            ambiente_obj = AMBIENTE
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            tipo_item_obj = TipoItem.objects.get(codigo=tipo_item)

            tipomodelo_obj = Modelofacturacion.objects.get(codigo="1")
            tipotransmision_obj = TipoTransmision.objects.get(codigo="1")
            tipooperacion_obj = CondicionOperacion.objects.get(id=tipooperacion_id) if tipooperacion_id else None
            tipo_moneda_obj = MONEDA_USD

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
                base_imponible=base_imponible_checkbox,
                tipotransmision=tipotransmision_obj
            )

            # Inicializar acumuladores globales
            total_gravada = Decimal("0.00")  # Suma de totales netos
            total_iva = Decimal("0.00")       # Suma de totales IVA
            total_pagar = Decimal("0.00")     # Suma de totales con IVA
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
            
            #Campos DTE
            tributo_valor = None

            # Recorrer productos para crear detalles (realizando el desglose)
            for index, prod_id in enumerate(productos_ids):

                try:
                    producto = Producto.objects.get(id=int(prod_id))
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
                    
                print("descuentos items: ", descuentos_aplicados)
                porcentaje_descuento_producto = descuentos_aplicados[index] if index < len(descuentos_aplicados) else 1
                # El precio del producto ya incluye IVA 
                precio_incl = producto.preunitario
                precio_tiene_iva = bool(producto.precio_iva)     # bandera del producto
                
                #Campo tributos
                #if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS: 
                    # Codigo del tributo (tributos.codigo)
                tributoIva = Tributo.objects.get(codigo="20")#IVA este codigo solo aplica a ventas gravadas(ya que estan sujetas a iva)
                tributo_valor = tributoIva.valor_tributo
                tributos = [str(tributoIva.codigo)]
                
                if tributo_valor is None:
                    tributo_valor = Decimal("0.00")
                #Campo precioUni
                if base_imponible_checkbox is True:
                    precio_neto = float(0.00)
                else: 
                    #Cuando no es FE quitarle iva al precio si se aplico desde el producto
                    if producto.precio_iva:
                        neto_unitario = (precio_incl / Decimal("1.13") ).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = neto_unitario
                    else:
                        neto_unitario = (precio_incl).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                        precio_inc_neto = neto_unitario
                    precio_neto = (neto_unitario * cantidad).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    #total_iva_item = ( precio_neto * Decimal("0.13") ).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    precio_neto = (precio_neto * Decimal(tributo_valor)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    
                precio_neto = Decimal(precio_neto)          
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                
                print("descuento:. ", porcentaje_descuento_producto)
                if porcentaje_descuento_producto:
                    porcentaje_descuento_item = Descuento.objects.get(porcentaje=(porcentaje_descuento_producto))
                else:
                    porcentaje_descuento_item = Descuento.objects.first()
                    
                descuento_porcentaje = (porcentaje_descuento_item.porcentaje / 100).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                if porcentaje_descuento_item.porcentaje > Decimal("0.00"):
                    descuento_aplicado=True
                else:
                    descuento_aplicado = False
                
                # Totales por ítem
                #Campo Ventas gravadas
                if monto_descuento:
                    monto_descuento = Decimal(monto_descuento).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    monto_descuento = Decimal("0.00")
                #Descuento a ventas gravadas
                if descu_gravado is None or descu_gravado == "":
                    descu_gravado = Decimal("0.00")
                
                descuento_item = (precio_neto * descuento_porcentaje).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_neto = (precio_neto - descuento_item).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                #Calcular IVA
                total_iva_item = ( total_neto * Decimal("0.13") ).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)

                #Campo codTributo
                cuerpo_documento_tributos = []
                tributo = None
                if producto.tributo is None:
                    seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                    return JsonResponse({"error": "Seleccionar tributo para el producto" })
                
                #Tributo sujeto iva (asociado al prod)
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    tributo = Tributo.objects.get(codigo=producto.tributo.codigo)
                    precio_neto = (precio_neto * Decimal(tributo.valor_tributo)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                    
                print("-Crear detalle factura")
                detalle = DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    unidad_medida=unidad_medida_obj,
                    precio_unitario=precio_inc_neto, # Se almacena el precio bruto (con IVA)
                    descuento=porcentaje_descuento_item,
                    tiene_descuento = descuento_aplicado,
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=(total_neto),  # Total neto
                    pre_sug_venta=(precio_inc_neto),
                    no_gravado=Decimal("0.00"),
                    saldo_favor=Decimal("0.00"),
                    tipo_documento_relacionar = tipo_doc_relacionar,
                    documento_relacionado = documento_relacionado
                )
                #resumen.totalGravado y subTotalVentas
                total_gravada += total_neto
                if descu_gravado:
                    descuento_gravado = (total_gravada * Decimal(descu_gravado) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                #Si el producto tiene porcentaje gobal restarlo al subtotal
                sub_total_item = Decimal("0")
                if descuento_global:
                    porc_descuento_global = (total_gravada * Decimal(descuento_global) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                sub_total_item = (total_gravada - descuento_gravado - porc_descuento_global).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                print(f"IVA Item = {total_iva_item}, iva unitario = {iva_unitario}, cantidad = {cantidad}, total neto = {total_neto} ")
                
                sub_total = sub_total_item
                
                #Calcular el valor del tributo
                if tributo_valor is not None:
                    valorTributo = ( Decimal(total_gravada) * Decimal(tributo_valor) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_operaciones = ((sub_total + valorTributo + DecimalIvaPerci) - DecimalRetIva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    total_operaciones = (sub_total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                total_con_iva = (total_operaciones - DecimalIvaPerci - DecimalRetIva - DecimalRetRenta - total_no_gravado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                total_iva += (total_iva_item).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print("total iva= ", total_iva, "total iva item= ", total_iva_item)
                #total_pagar += total_con_iva
                total_pagar = total_con_iva
                
                # Actualizamos manualmente los campos calculados
                detalle.total_sin_descuento = (total_neto).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.iva = (total_iva_item).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.total_con_iva = (total_con_iva).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                detalle.iva_item = (total_iva_item).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)  # Guardamos el total IVA para este detalle
                detalle.save()
                
                print("-Aplicar tributo sujeto iva")
                """valor_porcentaje = Decimal(porcentaje_descuento_item.porcentaje)
                
                if valor_porcentaje.compare(Decimal("0.00")) > 0:
                    descuento_item += porcentaje_descuento_item.porcentaje
                print("-Total desc gravado: ", descuento_item)"""
                
            # Calcular retenciones (globales sobre el total neto de cada detalle)
            if retencion_iva and porcentaje_retencion_iva > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_iva:
                        DecimalRetIva += (detalle.total_sin_descuento * porcentaje_retencion_iva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if retencion_renta and porcentaje_retencion_renta > 0:
                for detalle in factura.detalles.all():
                    if str(detalle.producto.id) in productos_retencion_renta:
                        DecimalRetRenta += (detalle.total_sin_descuento * porcentaje_retencion_renta / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            # Redondear totales globales
            total_iva = total_iva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_pagar = total_pagar.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            #Sino se ha seleccionado ningun documento a relacionar enviar null los campos
            if tipo_doc_relacionar == COD_DOCUMENTO_RELACIONADO_NO_SELEC:
                tipo_doc_relacionar = None
                documento_relacionado = None
            print(f"Tipo de doc a relacionar: {tipo_doc_relacionar} numero de documento: {documento_relacionado}")
            # Actualizar totales en la factura
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = (total_gravada).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.sub_total_ventas = (total_gravada).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = float(descuento_gravado)
            factura.por_descuento = porc_descuento_global #Decimal("0.00")
            factura.total_descuento = float(monto_descuento)
            factura.sub_total = (sub_total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            factura.iva_retenido = float(DecimalRetIva)
            factura.retencion_renta = float(DecimalRetRenta)
            factura.total_operaciones = float(total_operaciones) #total_gravada
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = float(total_pagar)
            factura.total_letras = num_to_letras(total_pagar)
            factura.total_iva = float(total_iva)
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = float(DecimalIvaPerci)
            factura.tipo_documento_relacionar = tipo_doc_relacionar
            factura.documento_relacionado = documento_relacionado.upper()
            factura.save()

            # Construir el cuerpoDocumento para el JSON con desglose
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                
                #Items permitidos 2000
                if idx > items_permitidos:
                    return JsonResponse({"error": "Cantidad máxima de ítems permitidos " }, {items_permitidos})
                else:
                    codTributo = None 
                    tributo_valor = None
                    cuerpo_documento_tributos = []
                    if det.producto.tributo is None:
                        seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                        return JsonResponse({"error": "Seleccionar tributo para el producto" })
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
                                    "numeroDocumento": str(det.documento_relacionado.upper()),
                                    "cantidad": float(det.cantidad), 
                                    "codigo": str(det.producto.codigo),
                                    "codTributo": codTributo,
                                    "uniMedida": int(det.unidad_medida.codigo),
                                    "descripcion": str(tributo.descripcion),
                                    "precioUni": float(abs(det.precio_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))),
                                    "montoDescu": float( abs(( (det.precio_unitario * det.cantidad) * (Decimal(det.descuento.porcentaje) / Decimal("100")))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) ), #float(descuento_item.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                                    "ventaNoSuj": float(0.0),
                                    "ventaExenta": float(0.0),
                                    "ventaGravada": float( abs(det.ventas_gravadas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) ),
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
                            "numeroDocumento": str(det.documento_relacionado.upper()),
                            "cantidad": float(det.cantidad), 
                            "codigo": str(det.producto.codigo),
                            "codTributo": codTributo,
                            "uniMedida": int(det.unidad_medida.codigo), 
                            "descripcion": str(det.producto.descripcion),
                            "precioUni": float(abs(det.precio_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))),
                            "montoDescu": float(abs( ( ((det.precio_unitario * det.cantidad) * (Decimal(det.descuento.porcentaje)) / Decimal("100")) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) )), #float(descuento_item.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),#float(det.descuento),
                            "ventaNoSuj": float(abs(det.ventas_no_sujetas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))),
                            "ventaExenta": float(abs(det.ventas_exentas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))),
                            "ventaGravada": float(abs(det.ventas_gravadas.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))),
                            "tributos": tributos
                        })
                                        
                    if cuerpo_documento_tributos is None:
                        cuerpo_documento.append(cuerpo_documento_tributos)

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
                        return JsonResponse({"error": "Limite de documentos relacionados: " }, {docs_permitidos})
                    
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
                
            print("1. Cuerpo documento: ", cuerpo_documento)
            factura_json = generar_json_doc_ajuste(
                ambiente_obj, tipo_dte_obj, factura, emisor, receptor,
                cuerpo_documento, observaciones, documentos_relacionados, contingencia, total_gravada
            )
            
            factura.json_original = factura_json
            factura.save()
            
            # Si acabamos de generar una Nota de Crédito, registramos la devolución al cliente:
            if tipo_dte_obj.codigo == COD_NOTA_CREDITO:
                # 1) Crear la devolución de venta
                devolucion = DevolucionVenta.objects.create(
                    num_factura=factura.numero_control,
                    motivo="Devolución generada por Nota de Crédito",
                    estado="Aprobada",
                    usuario=request.user.username if request.user.is_authenticated else None
                )
                # 2) Registrar cada detalle de devolución y el reingreso de stock
                for det in factura.detalles.all():
                    # 2a) Detalle de la devolución
                    DetalleDevolucionVenta.objects.create(
                        devolucion=devolucion,
                        producto=det.producto,
                        cantidad=det.cantidad,
                        motivo_detalle="Reingreso automático por NC"
                    )
                    # 2b) Movimiento de inventario de Entrada
                    if det is not None and det.producto.almacenes.exists():
                        almacen = det.producto.almacenes.first() or Almacen.objects.first()
                        MovimientoInventario.objects.create(
                            producto=det.producto,
                            almacen=almacen,
                            tipo='Entrada',
                            cantidad=det.cantidad,
                            referencia=f"Reingreso NC {factura.numero_control}"
                        )
                    print("DEVOLUCION DESDE VIEW AJUSTE")
                        
                    # 2c) Ajuste de stock atómico
                    Producto.objects.filter(pk=det.producto.pk).update(
                        stock=F('stock') + det.cantidad
                    )
                # 3) Generar la Nota de Crédito
                NotaCredito.objects.create(
                    devolucion=devolucion,
                    monto=factura.total_pagar,
                    estado="Pendiente"
                )
            # 2) Si es Nota de Débito ➞ salida extra de stock
            elif tipo_dte_obj.codigo == COD_NOTA_DEBITO:
                # (opcional) si quieres guardar un modelo NotaDebito, créalo aquí
                for det in factura.detalles.all():
                    if det is not None and det.producto.almacenes.exists():
                        MovimientoInventario.objects.create(
                            producto=det.producto,
                            almacen=det.producto.almacenes.first() or Almacen.objects.first(),
                            tipo='Salida',
                            cantidad=det.cantidad,
                            referencia=f"Salida ND {factura.numero_control}"
                        )
                        # ajustar stock sin bajar de cero
                        Producto.objects.filter(pk=det.producto.pk).update(
                            stock=Greatest(F('stock') - det.cantidad, Value(0))
                        )

            # Guardar el JSON en la carpeta "FE/json_facturas"
            json_path = os.path.join(RUTA_JSON_FACTURA.url, f"{factura.numero_control}.json")
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(factura_json, f, indent=4, ensure_ascii=False)

                return JsonResponse({
                    "mensaje": "Factura generada correctamente",
                    "factura_id": factura.id,
                    "numero_control": factura.numero_control,
                    "redirect": reverse('detalle_factura', args=[factura.id])
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error al generar la factura: {e}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#########################################################################################################
# EVENTOS DE CONTINGENCIA DE DTE
#########################################################################################################

#LISTADO DE EVENTOS dte_contingencia_list
def contingencia_list(request):
    try:
        request.session['intentos_reintento'] = 0  # Establecemos el contador a 0 al inicio
        #Verificar si existen eventos activos con fecha fuera de plazo y desactivarlos
        finalizar_contigencia_view(request)
        
        #Fecha y hora actual
        fecha_actual = obtener_fecha_actual()
        fecha_limite = (fecha_actual - timezone.timedelta(hours=72))#72 horas

        # Obtener listado de la base
        try:
            queryset = EventoContingencia.objects.prefetch_related('lotes_contingencia__factura').distinct().all().order_by('id')
        except Exception as e:
            return render(request, 'dte_contingencia.html', {"Error en la busqueda de contingencias": str(e)})

        # Aplicar filtros según los parámetros GET
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
            queryset = queryset.filter(lotes_contingencia__factura__tipo_dte__id=tipo_dte_id)
        
        # Configurar la paginación: 20 registros por página
        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        dtelist = paginator.get_page(page_number)
            
        tipos_dte = Tipo_dte.objects.filter(codigo__in=DTE_APLICA_CONTINGENCIA)
        
        # Crear una lista para almacenar los eventos con lotes y facturas agrupadas
        eventos_con_lotes = []
        
        for evento in dtelist:
            # Obtener todas las facturas relacionadas con los lotes del evento
            facturas = []
            for lote in evento.lotes_contingencia.all():
                facturas.append(lote.factura)
                
                #Verificar cada lote asociado al evento si ya pasaron 72 horas desde el otorgamiento del sello para el evento entonces inactivar lotes
                if evento.sello_recepcion is not None and evento.recibido_mh and evento.fecha_sello_recibido is not None:
                    fecha_sello_recibido =  evento.fecha_sello_recibido
                    if fecha_sello_recibido <= fecha_limite:
                        lote_obj = LoteContingencia.objects.filter(factura__id=lote.factura.id).first()
                        if lote_obj and lote_obj.finalizado == False:
                            lote_obj.finalizado = True
                            lote_obj.fecha_modificacion = fecha_actual.date()
                            lote_obj.hora_modificacion = fecha_actual.time()
                            lote_obj.save()
            # Dividir las facturas en grupos de 100
            facturas_en_grupos = []
            #facturas_en_grupos = [facturas[i:i + 2] for i in range(0, len(facturas), 2)]
            for i in range(0, len(facturas), 100):
                grupo_facturas = facturas[i:i + 100]
                mostrar_checkbox_lote = any(
                    f.recibido_mh == False and f.sello_recepcion and evento.sello_recibido is None for f in grupo_facturas
                )
                facturas_en_grupos.append({
                    'facturas': grupo_facturas,
                    'mostrar_checkbox_lote': mostrar_checkbox_lote
                })

            # Contar cuántos grupos de lotes existen (lotes por evento)
            total_lotes_evento = len(facturas_en_grupos)

            # Agregar el evento con lotes y facturas agrupadas
            eventos_con_lotes.append({
                'evento': evento,
                'facturas_en_grupos': facturas_en_grupos,
                'total_lotes_evento': total_lotes_evento,
                'mostrar_checkbox': any(  # Para checkbox del evento
                    f.recibido_mh == False and f.sello_recepcion is None for f in facturas
                )
            })
        
        return render(request, 'documentos/dte_contingencia_list.html', {
            'dtelist': dtelist,
            'tipos_dte': tipos_dte,
            'eventos_con_lotes': eventos_con_lotes
        })
    except Exception as e:
        return render(request, 'dte_contingencia.html', {"error": str(e)})

# ENVIA LA CONTINGENCIA 1 A 1
@csrf_exempt
def contingencia_dte_unificado_view(request):
    try:
        contingencia_id = request.GET.get("contingencia_id")
        
        print("[uno a uno]Inicio enviar contingencia view")
        
        # ---------------------------------
        # Paso 2: Obtener el json generado de contingencia
        # ---------------------------------
        try:
            response_evento_contingencia = contingencia_dte_view(request, contingencia_id)
            print("Response evento contingencia: ", response_evento_contingencia)
            if response_evento_contingencia and response_evento_contingencia.status_code != 302:
                return JsonResponse(response_evento_contingencia.data) 
            print("Status contingencia dte view: ", response_evento_contingencia)
        except Exception as e:
            print(f"Error al generar evento de contingencia: {str(e)}")
        
        # ---------------------------------
        # Paso 3: Llamar a la función firma del evento de contingencia
        # ---------------------------------
        try:
            response_firma = firmar_contingencia_view(request, contingencia_id)
            print("Response firma contingencia: ", response_firma)
            if response_firma and response_firma.status_code != 302 and response_firma.status_code !=200:
                return response_firma
            else:
                print("La respuesta de firma es None")
                ValueError("La respuesta de firma es None")
        except Exception as e:
            print(f"Error al firmar contingencia: {str(e)}")
        
        # ---------------------------------
        # Paso 4: Llamar a la función que envía el evento de contigencia firmado a Hacienda
        # ---------------------------------
        print("Enviar contingencia view")
        try:
            response_envio = enviar_contingencia_hacienda_view(request, contingencia_id)#PENDIENTE ACTUALIZAR
            print("response text envio contingencia: ", response_envio)
            print(f"Contenido de la respuesta de envio: {response_envio.content}")
        except Exception as e:
            print(f"Error al enviar contingencia a Hacienda: {str(e)}")

        
        # ---------------------------------
        # Consultar el estado final y preparar el mensaje de respuesta
        # ---------------------------------
        try:
            evento = EventoContingencia.objects.filter(id=contingencia_id).first()
            if evento:
                if evento.recibido_mh:
                    mensaje = "Contingencia enviada con éxito"
                else:
                    mensaje = "No se pudo enviar la contingencia"
            else:
                mensaje = "No se encontró el evento de contingencia"
        except Exception as e:
            print(f"Error al verificar el estado del evento: {str(e)}")
            mensaje = "Error al consultar el evento de contingencia"

        # Intentamos cargar el detalle (si es un JSON válido)
        try:
            if response_envio.status_code == 200:
                try:
                    detalle = json.loads(response_envio.content)
                except Exception as e:
                    # Si no se puede cargar como JSON, mostramos el error
                    print(f"Error al convertir la respuesta a JSON: {e}")
                    detalle = response_envio.content.decode()  # Decodificamos como texto si no es JSON
            else:
                # Si el código de estado no es 200, mostramos el código y el contenido
                print(f"Error en la respuesta de envío: {response_envio.status_code}")
                detalle = f"Error al enviar la contingencia, código de estado: {response_envio.status_code}"
        except Exception as e:
            detalle = f"Error procesando respuesta de envío: {str(e)}"

        # Verificamos el contenido de 'detalle' antes de retornar
        print(f"mensaje: {mensaje}, detalle: {detalle}")
        
        return JsonResponse({
            "mensaje": mensaje,
            "detalle": detalle
        })
    
    except Exception as e:
        print(f"Error general en el proceso unificado: {e}")
        return JsonResponse({"error": str(e)}, status=400)

# ENVIA TODAS LAS CONTINGENCIAS SELECCIONADAS EN LA TABLA
@csrf_exempt
def contingencias_dte_view(request):
    print("Enviar contingencias")
    if request.method == "POST":
        try:
            # Se espera recibir una lista de IDs en el parámetro 'contingencia_ids'
            contingencia_ids = request.POST.getlist('contingencia_ids')
            motivos_contingencia = request.GET.get("motivo_contingencia", None)
            codigos_motivo = request.GET.get("codigo_motivo", None)
            motivo = None
            
            results = []
            for contingencia_id in contingencia_ids:
                print("Enviar contingencia idd: ", contingencia_id)
                
                # ---------------------------------
                # Paso 1: Actualizar tipo contingencia si el codigo es 5
                # ---------------------------------
                # if codigo_motivo and codigo_motivo == COD_TIPO_CONTINGENCIA:
                #     try:
                #         motivo = TipoContingencia.objects.filter(codigo=codigo_motivo).first()
                #         if motivo:
                #             motivo.motivo_contingencia = motivo_contingencia
                #             motivo.save()
                #     except Exception as e:
                #         print(f"Error al actualizar motivo de contingencia: {str(e)}")
                #         return JsonResponse({"error": "Error al actualizar motivo de contingencia"}, status=400)
                
                # ---------------------------------
                # Paso 2: Obtener el json generado de contingencia
                # ---------------------------------
                try:
                    # Llamar a la función de generacion del evento en contingencia
                    response_evento_contingencia = contingencia_dte_view(request, contingencia_id)
                    if response_evento_contingencia and response_evento_contingencia.status_code != 302:
                        results.append({
                            "contingencia_id": contingencia_id,
                            "mensaje": "Error en contingencia",
                            "detalle": response_evento_contingencia.content.decode()
                        })
                        continue
                except Exception as e:
                    print(f"Error al generar evento de contingencia: {str(e)}")

                # ---------------------------------
                # Paso 3: Llamar a la función firma del evento de contingencia
                # ---------------------------------
                try:
                    response_firma = firmar_contingencia_view(request, contingencia_id)
                    print("Firma generada: ", response_firma)
                    if response_firma and (response_firma.status_code != 302 and response_firma.status_code !=200):
                        results.append({
                            "contingencia_id": contingencia_id,
                            "mensaje": "Error en firma",
                            "detalle": response_firma.content.decode()
                        })
                        continue
                except Exception as e:
                    print(f"Error al firmar contingencia: {str(e)}")

                # ---------------------------------
                # Paso 4: Llamar a la función que envía el evento de contigencia firmado a Hacienda
                # ---------------------------------
                print("Enviar contingencias a MH")
                try:
                    response_envio = enviar_contingencia_hacienda_view(request, contingencia_id)
                except Exception as e:
                    print(f"Error al enviar contingencia a Hacienda: {str(e)}")
                # ---------------------------------
                # Consultar el estado final y preparar el mensaje de respuesta
                # ---------------------------------
                try:
                    evento = EventoContingencia.objects.filter(id=contingencia_id).first()
                    if evento:
                        if evento.recibido_mh:
                            mensaje = "Contingencia enviada con éxito"
                        else:
                            mensaje = "No se pudo enviar la contingencia"
                    else:
                        mensaje = "No se encontró el evento de contingencia"
                except Exception as e:
                    print(f"Error al verificar el estado del evento: {str(e)}")
                    mensaje = "Error al consultar el evento de contingencia"

                # Intentamos cargar el detalle (si es un JSON válido)
                try:
                    if response_envio.status_code == 200:
                        try:
                            detalle = json.loads(response_envio.content)
                        except Exception as e:
                            # Si no se puede cargar como JSON, mostramos el error
                            print(f"Error al convertir la respuesta a JSON: {e}")
                            detalle = response_envio.content.decode()  # Decodificamos como texto si no es JSON
                        results.append({
                            "contingencia_id": contingencia_id,
                            "mensaje": mensaje,
                            "detalle": detalle
                        })
                    else:
                        # Si el código de estado no es 200, mostramos el código y el contenido
                        print(f"Error en la respuesta de envío: {response_envio.status_code}")
                        detalle = f"Error al enviar la contingencia, código de estado: {response_envio.status_code}"
                except Exception as e:
                    detalle = f"Error procesando respuesta de envío: {str(e)}"
                    results.append({
                            "contingencia_id": contingencia_id,
                            "mensaje": "Error inesperado",
                            "detalle": str(e)
                        })
                    return JsonResponse({"results": results})
                
            return JsonResponse({"results": results})
        except Exception as e:
            print(f"Error general en el proceso unificado: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

# GENERA EL EVENTO DE CONTINGENCIA
@csrf_exempt
def contingencia_dte_view(request, contingencia_id):
    print("Generar vista contingencia: id: ", contingencia_id)

    try:
        # Generar json, firmar, enviar a MH
        print("Emisor: ", emisor_fe)
        try:
            evento_contingencia = EventoContingencia.objects.get(id=contingencia_id)  # Buscar DTE a invalidar
            print("Evento contingencia dte view: ", evento_contingencia)
        except EventoContingencia.DoesNotExist:
            print("No se encontró el evento de contingencia")
            return JsonResponse({
                "error": "Evento no encontrado",
                "detalle": "No existe un evento con ese ID"
            }, status=status.HTTP_404_NOT_FOUND)

        if evento_contingencia is not None:
            detalles_dte = []
            facturas = []
            
            try:
                for lote in evento_contingencia.lotes_contingencia.all():
                    facturas.append(lote.factura)
            except Exception as e:
                print(f"Error al obtener facturas de los lotes: {e}")
                return JsonResponse({"error": "No se pudieron obtener las facturas"}, status=400)
            
            #if facturas and facturas.count()>0:
            if not facturas:
                print("El evento de contingencia no contiene lotes asignados")
                return JsonResponse({
                    "error": "El evento no contiene lotes asignados",
                    "detalle": "Debe haber al menos una factura asociada"
                }, status=status.HTTP_204_NO_CONTENT)
            
            for idx, fe in enumerate(facturas, start=1):
                detalles_dte.append({
                    "noItem": idx,
                    "tipoDoc": str(fe.tipo_dte.codigo),
                    "codigoGeneracion": str(fe.codigo_generacion).upper()
                })
            
            #Generar json contingencia
            print("Generar json contingencia: ", evento_contingencia)
            try:
                #Obtener fecha actual y aplicar formato YYYY-MM-DD
                fecha_actual = obtener_fecha_actual()
                fecha_transmision = fecha_actual.strftime('%Y-%m-%d')
                
                json_identificacion = {
                    "version": int(VERSION_EVENTO_CONTINGENCIA.valor),
                    "ambiente": str(AMBIENTE.codigo),
                    "codigoGeneracion": str(evento_contingencia.codigo_generacion).upper(),
                    "fTransmision": str(fecha_transmision),
                    "hTransmision": str(datetime.now().strftime('%H:%M:%S'))
                }
                
                json_emisor = {
                    "nit": str(emisor_fe.nit),
                    "nombre": str(emisor_fe.nombre_razon_social),
                    "nombreResponsable": str(emisor_fe.representante.nombre) if emisor_fe.representante else str(emisor_fe.nombre_razon_social),
                    "tipoDocResponsable": str(emisor_fe.representante.tipo_documento.codigo) if emisor_fe.representante else str(emisor_fe.tipo_documento.codigo),
                    "numeroDocResponsable": str(emisor_fe.representante.numero_documento) if emisor_fe.representante else str(emisor_fe.nit),
                    "tipoEstablecimiento": str(emisor_fe.tipoestablecimiento.codigo) if emisor_fe.tipoestablecimiento else "",
                    "codEstableMH": str(emisor_fe.codigo_establecimiento),
                    "codPuntoVenta": str(emisor_fe.codigo_punto_venta), #"0001",
                    "telefono": str(emisor_fe.telefono),
                    "correo": str(emisor_fe.email)
                }
                
                json_motivo = {
                    "fInicio": str(evento_contingencia.fecha_transmision), #date.today().strftime('%H:%M:%S'),
                    "fFin":  str(evento_contingencia.f_fin), #date.today().strftime('%H:%M:%S'),
                    "hInicio": str(evento_contingencia.hora_transmision.strftime('%H:%M:%S')), #La estructura de la hora de entrada en contingencia será definida por la Administración Tributaria
                    "hFin": str(evento_contingencia.h_fin.strftime('%H:%M:%S')), #La estructura de la hora de salida en contingencia será definida por la Administración Tributaria
                    "tipoContingencia": int(evento_contingencia.tipo_contingencia.codigo), #CAT-005 Tipo de Contingencia 
                }
                
                #Especifiar motivo de contingencia
                if evento_contingencia.tipo_contingencia and evento_contingencia.tipo_contingencia.codigo == COD_TIPO_CONTINGENCIA:
                    json_motivo["motivoContingencia"] = evento_contingencia.tipo_contingencia.motivo_contingencia #Explicar motivo contingencia
                else:
                    json_motivo["motivoContingencia"] = None
                
                json_completo = {
                    "identificacion": json_identificacion,
                    "emisor": json_emisor,
                    "detalleDTE": detalles_dte,
                    "motivo": json_motivo
                }
                
                evento_contingencia.json_original = json_completo
                evento_contingencia.fecha_modificacion = fecha_actual.date()
                evento_contingencia.hora_modificacion = fecha_actual.time()
                evento_contingencia.save()
                print("FIN view contingencia")
                return redirect(reverse('listar_contingencias'))
            except Exception as e:
                print(f"Error: al generar el JSON del evento de contingencia: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error general en el evento de contingencia: {e}")
        return JsonResponse({"error": str(e)}, status=400)

# FIRMAR EL JSON CONTINGENCIA
@csrf_exempt
def firmar_contingencia_view(request, contingencia_id):
    CERT_PATH        = get_config("certificado", campo="url_endpoint")
    """
    Firma contingencia y, si ya está firmada, la envía a Hacienda.
    """
    print("Contingencia | Inicio firma DTE: ", contingencia_id)  
    
    global emisor_fe
        
    contingencia = True
    intento = 1
    intentos_max = 3 #Intentos para envio del dte a MH
    tipo_contingencia_obj = None
    mensaje = None
    error_envio = None
    response = None
    response_data = {}
    fecha_actual = obtener_fecha_actual()
    
    #Buscar contingencia a firmar
    try:
        evento_contingencia = EventoContingencia.objects.get(id=contingencia_id)
        print("contingencia encontrada: ", evento_contingencia)
    except EventoContingencia.DoesNotExist:
        return JsonResponse({"error": "Evento de contingencia no encontrado"}, status=404)
    
    while intento <= intentos_max:
        token_data = Token_data.objects.filter(activado=True).first()
        if not token_data:
            return JsonResponse({"error": "No hay token activo registrado en la base de datos."}, status=401)

        if not os.path.exists(CERT_PATH):
            return JsonResponse({"error": "No se encontró el certificado en la ruta especificada."}, status=400)
        
        # Verificar y formatear el JSON original de la contingencia
        try:
            if isinstance(evento_contingencia.json_original, dict):
                dte_json_str = json.dumps(evento_contingencia.json_original, separators=(',', ':'))
            else:
                json_obj = json.loads(evento_contingencia.json_original)
                dte_json_str = json.dumps(json_obj, separators=(',', ':'))
        except Exception as e:
            return JsonResponse({
                "error": "El JSON original de contingencia no es válido",
                "detalle": str(e)
            }, status=400)
            
        # Antes de la llamada al firmador, se parsea una sola vez a objeto:
        if isinstance(evento_contingencia.json_original, dict):
            dte_json_obj = evento_contingencia.json_original
        else:
            dte_json_obj = json.loads(evento_contingencia.json_original)
            
        # Construir el payload con los parámetros requeridos
        payload = {
            "nit": str(emisor_fe.nit),   # Nit del contribuyente
            "activo": True,            # Indicador activo
            "passwordPri": str(emisor_fe.clave_privada), #"3nCr!pT@d0Pr1v@d@",   # Contraseña de la llave privada
            "dteJson": dte_json_obj   # JSON del DTE como cadena
        }

        headers = {"Content-Type": CONTENT_TYPE.valor}

        try:
            response = requests.post(FIRMADOR_URL.url_endpoint, json=payload, headers=headers)
            
            # Capturamos la respuesta completa
            if response:
                try:
                    response_data = response.json()
                except Exception as e:
                    # En caso de error al parsear el JSON, se guarda el texto crudo
                    response_data = {"error": "No se pudo parsear JSON", "detalle": response.text}
                    print("Error al decodificar JSON en envío:", e)
                
                # Guardar toda la respuesta en la factura para depuración (incluso si hubo error)
                # Verificar si la firma fue exitosa
                if response.status_code == 200 and response_data.get("status") == "OK":
                    evento_contingencia.json_firmado = response_data
                    evento_contingencia.firmado = True
                    evento_contingencia.save()
                    print("Guardar cambios contingencia firma: ", response_data.get("status"))
                    return JsonResponse({
                        "mensaje": "Firma de contingencia exitosa.",
                        "detalle": response_data
                }, status=response.status_code)
                else:
                    print("Firma | Ocurrio un error al firmar la factura")
                    if response.status_code in [500, 502, 503, 504, 408]: #503, 504
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                    elif response.status_code in [408, 499]: #500, 503
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                    elif response.status_code in [503, 504]: #503, 504
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                    else:#Otro- 400, 500, 502
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                        mensaje = f"Error en el envío de la factura: {response.status_code}"
                        print("Error: ", mensaje)
                    # Esperar antes de siguiente intento
                    error_envio = f"Error al firmar la factura: {response.status_code}"
                    print("Error en el intento de firma:", intento)
                    intento += 1
                    time.sleep(1) 
                    contingencia = True
        except requests.exceptions.RequestException as e:
            error_envio = "Error de conexión con el firmador"
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
            time.sleep(1) 
            intento += 1
            print("Error: ", error_envio)
            #return JsonResponse({"error": "Error de conexión con el firmador", "detalle": str(e)}, status=500)
        except requests.exceptions.ConnectionError:
            #Error de red del emisor
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_envio = f"Error de conexion: {response.status_code}"
            print("Error: ", error_envio)
        except requests.exceptions.Timeout:
            #Error del emisor
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_envio = f"Se agoto el tiempo de espera: {response.status_code}"
            print("Error: ", error_envio)
        except Exception as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
            error_envio = str(e)
            print(f"Ocurrió un error inesperado: {error_envio}")
            intento += 1
            time.sleep(1) 
    # Solo crear contingencia si al menos uno de los flujos falló
    if contingencia:
        evento_contingencia.fecha_modificacion = fecha_actual.date()
        evento_contingencia.hora_modificacion = fecha_actual.time()
        evento_contingencia.save()
        # (Opcional) Guardar el JSON firmado en un archivo
        try:
            if response and response.status_code == 200 and response_data.get("status") == "OK":
                json_signed_path = f"{FACTURAS_FIRMADAS_URL.url}{evento_contingencia.codigo_generacion}.json"
                os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
                with open(json_signed_path, "w", encoding="utf-8") as json_file:
                    json.dump(response_data, json_file, indent=4, ensure_ascii=False)
            else:
                # Se devuelve el error completo recibido
                return JsonResponse({"error": "Error al firmar la contingencia", "detalle": response_data}, status=400)
        except Exception as e:
            print("Error al guardar archivo firmado:", e)
    print("-Fin firma contingencia DTE - id contingencia ", contingencia_id)

csrf_exempt
def enviar_contingencia_hacienda_view(request, contingencia_id):
    print("-Inicio enviar contingencia a MH: ", contingencia_id)

    contingencia = True
    intento = 1
    intentos_max = 3  # Intentos para envio del DTE a MH
    tipo_contingencia_obj = None
    mensaje = None
    # Banderas para verificar si ya se creo una contingencia
    contingencia_creada = False
    error_autenticacion = None
    error_envio = None
    
    fecha_actual = obtener_fecha_actual()
    
    evento_contingencia = EventoContingencia.objects.get(id=contingencia_id)

    # Paso 1: Autenticación contra el servicio de Hacienda
    global emisor_fe
    nit_empresa = str(emisor_fe.nit)  # "06142811001040"
    pwd = str(emisor_fe.clave_publica)  # "Q#3P9l5&@aF!gT2sA"
    auth_url = URL_AUTH.url_endpoint
    auth_headers = {
        "Content-Type": HEADERS.url_endpoint,
        "User-Agent": HEADERS.valor
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}
    auth_response = None
    response_data = None

    print("Inicio response autenticacion")
    while intento <= intentos_max:
        print(f"Intento {intento} de {intentos_max}")
        try:
            # --- Autenticación
            auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

            if auth_response.status_code == 200:
                auth_response_data = auth_response.json()
                estado_response = auth_response_data.get("estado", None)

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
                contingencia = False  # No es necesario continuar en contingencia
                print("Autenticacion exitosa")
                break
            else:
                # --- Error de autenticación
                if auth_response.status_code in [500, 502, 503, 504, 408]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                elif auth_response.status_code in [408, 499]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                elif auth_response.status_code in [503, 504]:
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                else:
                    mensaje = f"Error en la autenticación: {auth_response.status_code}"
                    tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")

                # Intentar nuevamente
                error_autenticacion = f"Error en la autenticación: {auth_response.status_code}"
                print("Error autenticación: ", error_autenticacion)
                time.sleep(1) 
                intento += 1
                contingencia = True
        except requests.exceptions.RequestException as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
            print(f"Error de conexion con el servicio de autenticación: {e}")
            time.sleep(1) 
            intento += 1
            error_autenticacion = str(e)
        except requests.exceptions.ConnectionError:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_autenticacion = f"Error de conexion: {auth_response.status_code}"
            print("Error: ", error_autenticacion)
        except requests.exceptions.Timeout:
            #Error del emisor
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
            time.sleep(1) 
            intento += 1
            error_autenticacion = f"e agoto el tiempo de espera: {auth_response.status_code}"
            print("Error: ", error_autenticacion)
        except Exception as e:
            tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
            error_autenticacion = str(e)
            print(f"Ocurrió un error inesperado: {e}")
        print("Fin response autenticacion")
    # Si la autenticación falló después de los intentos, detener el flujo
    print("CONTINGENCIA: ", contingencia)

    #---Envio del dte
    if contingencia == False:
        intento = 1
        while intento <= intentos_max:
            print(f"Intento {intento} de {intentos_max}")
            try:
                # Paso 2: Enviar la factura firmada a Hacienda
                token_data_obj = Token_data.objects.filter(activado=True).first()
                if not token_data_obj or not token_data_obj.token:
                    return JsonResponse({"error": "No hay token activo para enviar la factura"}, status=401)

                codigo_generacion_str = str(evento_contingencia.codigo_generacion)
                # --- Validación y limpieza del documento firmado ---
                documento_str = evento_contingencia.json_firmado
                if not isinstance(documento_str, str):
                    documento_str = json.dumps(documento_str)

                # Eliminar posibles caracteres BOM y espacios innecesarios
                documento_str = documento_str.lstrip('\ufeff').strip()  # .upper()
                print("Json contingencia firmado: ", documento_str)

                try:
                    if isinstance(evento_contingencia.json_firmado, str):
                        firmado_data = json.loads(evento_contingencia.json_firmado)
                    else:
                        firmado_data = evento_contingencia.json_firmado
                except Exception as e:
                    return JsonResponse({
                        "error": "Error al parsear el documento firmado",
                        "detalle": str(e)
                    }, status=400)

                documento_token = firmado_data.get("body", "")
                if not documento_token:
                    return JsonResponse({
                        "error": "El documento firmado no contiene el token en 'body'"
                    }, status=400)

                documento_token = documento_token.strip()  # Limpiar espacios innecesarios

                envio_json = {
                    "nit": str(emisor_fe.nit),  # "06142811001040", 
                    "documento": str(documento_token)  # Enviamos solo el JWT firmado
                }

                envio_headers = {
                    "Authorization": str(f"Bearer {token_data_obj.token}"),
                    "User-Agent": USER_AGENT.valor,
                    "Content-Type": CONTENT_TYPE.valor#"Application/JSON"
                }

                envio_response = requests.post(
                    HACIENDA_CONTINGENCIA_URL.url_endpoint,
                    headers=envio_headers,
                    json=envio_json
                )
                print("Envio response text:", envio_response.text)
                sello_recibido = None

                try:
                    response_data = envio_response.json() if envio_response.text.strip() else {}
                    sello_recibido = response_data.get("selloRecibido", None)
                except ValueError as e:
                    response_data = {"raw": envio_response.text or "No content"}
                    print("Error al decodificar JSON en envío:", e)
                    
                #json_content = envio_response.content.decode('utf-8')
                #json_observaciones = json.loads(json_content)
                try:
                    json_observaciones = json.loads(envio_response.content)
                except Exception as e:
                    json_observaciones = envio_response.content.decode()
                    print("Error al decodificar JSON en observaciones:", e)

                if envio_response.status_code == 200 and sello_recibido is not None:
                    responseText = json.loads(envio_response.text)
                    print(f"Respuesta MH: {envio_response.status_code}, sello de recepcion: {responseText['selloRecibido']}")

                    evento_contingencia.sello_recepcion = response_data.get("selloRecibido", "")
                    evento_contingencia.recibido_mh = True
                    evento_contingencia.finalizado = True
                    # Guardar respuesta de MH en json_original
                    json_response_data = {
                        "jsonRespuestaMh": response_data
                    }
                    json_original = evento_contingencia.json_original

                    #Combinar jsons
                    json_nuevo = json_original | json_response_data
                    #Convertir diccionario en json
                    json_respuesta_mh = json.dumps(json_nuevo)
                    #Al convertir un diccionario en json se guarda como un string, por lo que se debe convertir a json (loads)
                    json_original_campo = json.loads(json_respuesta_mh)
                    evento_contingencia.json_original = json_original_campo
                    evento_contingencia.fecha_modificacion = fecha_actual.date()
                    evento_contingencia.hora_modificacion = fecha_actual.time()
                    evento_contingencia.fecha_sello_recibido = fecha_actual
                    evento_contingencia.save()
                    print("-Fin enviar contingencia a MH")
                    return JsonResponse({
                        "mensaje": "Contingencia enviada con éxito",
                        "respuesta": response_data
                    }, status=envio_response.status_code)
                else:
                    if auth_response.status_code in [500, 502, 503, 504, 408]: #503, 504
                        print("Error al conectarse al servidor: ", auth_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                    elif auth_response.status_code in [408, 499]: #500, 503
                        print("Error al conectarse al servidor: ", auth_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="2")
                    elif auth_response.status_code in [503, 504]: #503, 504
                        print("Error al conectarse al servidor: ", auth_response.status_code)
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="4")
                    else:#Otro- 400, 500, 502
                        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                        mensaje = f"Error en el envío de la factura: {envio_response.status_code}"
                        print("Error en el envio de la factura: # intento de envio: ", intento)
                        
                    # Esperar antes de siguiente intento
                    error_envio = f"Error en el envío de la factura: {envio_response.status_code}"
                    time.sleep(1) 
                    intento += 1
                    contingencia = True
                    return JsonResponse({
                        "mensaje": error_envio,
                        "estado": response_data.get("estado", ""),
                        "respuesta": response_data.get("descripcionMsg", "")
                    }, status=envio_response.status_code)

            except requests.exceptions.RequestException as e:
                error_envio = str(e)
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="1")
                time.sleep(1) 
                intento += 1
                print("Error: ", error_envio)
            except requests.exceptions.ConnectionError:
                #Error de red del emisor
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
                time.sleep(1) 
                intento += 1
                error_envio = f"Error de conexion: {envio_response.status_code}"
                print("Error: ", error_envio)
            except requests.exceptions.Timeout:
                #Error del emisor
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="3")
                time.sleep(1) 
                intento += 1
                error_envio = f"Se agoto el tiempo de espera: {envio_response.status_code}"
                print("Error: ", error_envio)
            except Exception as e:
                tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
                error_envio = str(e)
                print(f"Ocurrió un error inesperado al enviar la contingencia: {e}")
                error_envio = str(e)
                intento += 1
                time.sleep(1) 
    else:
        evento_contingencia.fecha_modificacion = fecha_actual.date()
        evento_contingencia.hora_modificacion = fecha_actual.time()
        evento_contingencia.save()

    return JsonResponse({
        "error": "Excedido el máximo número de intentos",
        "detalle": f"Error de conexión o autenticación: {error_autenticacion or error_envio}"
    })

#########################################################################################################
# ENVIO DE LOTES EN CONTINGENCIA
#########################################################################################################
@csrf_exempt
def lote_contingencia_dte_view(request, factura_id, tipo_contiengencia_obj):
    print("Crear lote de los dte generados en contingencia: ", factura_id)
    lote_contingencia = None
    crear_evento = False
    max_items = 5000
    try:
        #Paso 1: Buscar factura guardada en contingencia
        documento_contingencia = FacturaElectronica.objects.filter(id=factura_id).order_by('id').first()
        print("Dte contingencia: ", documento_contingencia)
        
        if documento_contingencia is None:
            return JsonResponse({
                "mensaje": f"Factura con ID {factura_id} no encontrada.",
                "detalle": "No se encontro el documento electronico"
            }, status=404)
        #Buscar si existe un dte en contigencia
        lote_existe = LoteContingencia.objects.filter(factura_id=documento_contingencia.id)
        print("Lote ya existe: ", lote_existe)
        
        if not lote_existe and documento_contingencia.contingencia == True:
            try:
                #Paso 2: Verificar si existe un evento de contingencia activo, sino existe crear el evento, si la cantidad de facturas agregadas al evento supera los 5000 crear un nuevo evento
                evento_contingencia = EventoContingencia.objects.annotate(num_lotes_evento=Count('lotes_contingencia')).filter(finalizado=False, recibido_mh=False, num_lotes_evento__lt=max_items).first()
                if evento_contingencia:
                    crear_evento = False
                elif evento_contingencia is None or not evento_contingencia:
                    crear_evento = True
                
                if crear_evento:
                    print("Crear contingencia")
                    codigo_generacion_contingencia = str(uuid.uuid4()).upper()
                    evento_contingencia = EventoContingencia.objects.create(
                        codigo_generacion = codigo_generacion_contingencia,
                        tipo_contingencia = tipo_contiengencia_obj
                    )
                    
                #Crear lotes
                if evento_contingencia:
                    try:
                        print("Creacion de lotes")
                        lote_contingencia = LoteContingencia.objects.create(
                            factura = documento_contingencia, 
                            evento = evento_contingencia
                        )
                        mensaje = f"Lote creado correctamente: {lote_contingencia.id}"
                        
                        return lote_contingencia
                    except Exception as e:
                        print(f"Error al crear el lote: {e}")
                        mensaje = f"Hubo un fallo al crear el lote: {str(e)}"
                else:
                    mensaje = "Hubo un fallo en el evento de contingencia"
                    
            except Exception as e:
                # En caso de que no se encuentre el evento que buscamos
                print("No se encontró un evento con las condiciones especificadas. ", e)
            return JsonResponse({
                #"factura_id": factura_id,
                #"mensaje": mensaje,
                "lote": lote_contingencia
            })
        else:
            mensaje = "El documento electrónico no está disponible"
        
        return JsonResponse({
            "mensaje": mensaje
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "mensaje": "Error en la creación de lotes",
            "detalle": str(e)
        }, status=404)
    finally:
        print("Proceso de creacion de lote de contingencia finalizado")

@csrf_exempt
def envio_dte_unificado_view(request):
    try:
        request.session['intentos_reintento'] = 0 
        factura_id = request.GET.get("factura_id")
        print("[uno a uno]Inicio enviar lote view: ", factura_id)
        # Establecer la zona horaria de El Salvador
        timezone_actual = pytz.timezone('America/El_Salvador')

        # Obtener la fecha y hora actual UTC y convertirla a la zona horaria de El Salvador
        datetime_utc = datetime.now(pytz.utc)
        fecha_actual = datetime_utc.astimezone(timezone_actual)
        
        response_envio = None
        
        try:
            results = []
            # ---------------------------------
            # Paso 1: Llamar a la función firma
            # ---------------------------------
            response_firma = firmar_factura_view(request, factura_id, interno=True)
            if not isinstance(response_firma, HttpResponse):
                print("response firma: ", response_firma)
                return JsonResponse({"error": "Respuesta inesperada de firma"}, status=500)
            if response_firma and response_firma.status_code and response_firma.status_code != 302 and response_firma.status_code != 200:
                return response_firma
        except Exception as e:
            print(f"Error al firmar factura: {str(e)}")
            
        # ---------------------------------
        # Paso 2: Llamar a la función que envía el dte firmado a Hacienda
        # ---------------------------------
        print(f"Enviar lote a MH: request: {request}, factura id: {factura_id}")
        
        try:
            response_envio = enviar_factura_hacienda_view(request, factura_id, uso_interno=True)
        except Exception as e:
            print("Error al llamar envío a Hacienda:", e)
            return JsonResponse({"error": f"Fallo al enviar a Hacienda: {e}"}, status=500)

        if not isinstance(response_envio, HttpResponse):
            return JsonResponse({"error": "Respuesta inesperada de envío"}, status=500)
        if response_envio.status_code != 200:
            return response_envio
        # ---------------------------------
        # Consultar el estado final y preparar el mensaje de respuesta
        # ---------------------------------
        try:
            factura = FacturaElectronica.objects.filter(id=factura_id).first()
            print("Factura procesada: ", factura)
            if factura:
                if factura.sello_recepcion is not None:
                    #Si la factura fue recibida y obtuvo sello de recepcion entonces finalizar el lote
                    lote = LoteContingencia.objects.filter(factura__id=factura_id).first()
                    print("Lote-Factura: ", lote.factura.numero_control)
                    if lote:
                        lote.finalizado=True
                        lote.recibido_mh = True
                        lote.fecha_modificacion = fecha_actual.date()
                        lote.hora_modificacion = fecha_actual.time()
                        lote.save()
                    mensaje = "Factura recibida con éxito"
                else:
                    mensaje = "No se pudo enviar la factura"
            else:
                mensaje = "No se encontró el documento elerectronico"
        except Exception as e:
            print(f"Error al verificar el estado del evento: {str(e)}")
            mensaje = "Error al consultar el evento de contingencia"

        try:
            if response_envio and response_envio.status_code and response_envio.status_code == 200:
                try:
                    detalle = json.loads(response_envio.content)
                except Exception as e:
                    # Si no se puede cargar como JSON, mostramos el error
                    print(f"Error al convertir la respuesta a JSON: {e}")
                    detalle = response_envio.content.decode()  # Decodificamos como texto si no es JSON
            else:
                # Si el código de estado no es 200, mostramos el código y el contenido
                print(f"Error en la respuesta de envío: {response_envio.status_code}")
                detalle = f"Error al enviar la factura, código de estado: {response_envio.status_code}"
        except Exception as e:
            detalle = f"Error procesando respuesta de envío: {str(e)}"
        print(f"mensaje: {mensaje}, detalle: {detalle}")
        results.append({
            "factura_id": factura_id,
            "mensaje": mensaje,
            "detalle": detalle
        })
        return JsonResponse({
            "mensaje": mensaje,
            "detalle": detalle
        })
    except Exception as e:
        results.append({
            "factura_id": factura_id,
            "mensaje": "Error inesperado",
            "detalle": str(e)
        })
        print({"error": str(e)}, status=400)
    return JsonResponse({"results": results})
        
@csrf_exempt
def lotes_dte_view(request):
    if request.method == "POST":
        try:
            request.session['intentos_reintento'] = 0 
            # Se espera recibir una lista de IDs en el parámetro 'factura_ids'
            factura_ids = request.POST.getlist('factura_ids')
            print("Lote de contingencias: ", factura_ids)
            results = []
            #facturas_firmadas_ids = []
            
            detalle_firma = None
            
            for factura_id in factura_ids:
                print("Enviar contingencia idd: ", factura_id)
                try:
                    # Llamar a la función de firma
                    response_firma = firmar_factura_view(request, factura_id, interno=True)
                    if response_firma and response_firma.status_code != 302 and response_firma.status_code != 200:
                        try:
                            detalle_error = response_firma.content.decode()
                        except Exception:
                            detalle_error = str(response_firma.content)
                        results.append({
                            "factura_id": factura_id,
                            "mensaje": "Error en firma",
                            "detalle": detalle_error
                        })
                        continue
                    print("decodificar respuesta firma: ", response_firma.content)
                    
                    #Asignar todos los ids de facturas firmadas
                    #facturas_firmadas_ids.append(factura_id)

                    # Llamar a la función de envío
                    response_envio = enviar_lotes_hacienda_view(request, factura_id)
                    print("Lote enviado a MH")
                    # Consultar el estado final del evento de contingencia
                    factura_electronica = FacturaElectronica.objects.get(id=factura_id)
                    
                    if factura_electronica:
                        if factura_electronica.recibido_mh:
                            mensaje = "Dte enviado con éxito"
                        else:
                            mensaje = "No se pudo enviar el dte"
                    else:
                        mensaje = "No se encontró el dte"

                    try:
                        detalle_firma = json.loads(response_firma.content)
                    except Exception:
                        detalle_firma = response_firma.content.decode()
                    
                    try:
                        detalle = json.loads(response_envio.content)
                    except Exception:
                        detalle = response_envio.content.decode()
                    
                    results.append({
                        "factura_id": factura_id,
                        "mensaje": mensaje,
                        "detalle_firma: ": detalle_firma,
                        "detalle": detalle
                    })
                    
                except Exception as e:
                    print("Ocurrio un error al firmar documentos: ", str(e))
                    results.append({
                        "factura_id": factura_id,
                        "mensaje": "Error inesperado",
                        "detalle_firma: ": detalle_firma,
                        "detalle": str(e)
                    })
                    return JsonResponse({"results": results})
                    
            #Enviar lotes firmados, en la recepcion de lotes se envia una lista de Documentos Tributarios Electrónicos Firmados los cuales seran procesados
            # for factura_id in facturas_firmadas_ids:
            #     try:
            #         # Llamar a la función de envío
            #         response_envio = enviar_lotes_hacienda_view(request, factura_id)
            #         print("Lote enviado a MH")
                    
            #         try:
            #             # Consultar el estado final del evento de contingencia
            #             factura_electronica = FacturaElectronica.objects.get(id=factura_id)
            #             if factura_electronica:
            #                 if factura_electronica.recibido_mh:
            #                     mensaje = "Dte enviado con éxito"
            #                 else:
            #                     mensaje = "No se pudo enviar el dte"
            #             else:
            #                 mensaje = "No se encontró el dte"
            #         except FacturaElectronica.DoesNotExist:
            #             mensaje = "No se encontró el DTE"

            #         try:
            #             detalle = json.loads(response_envio.content)
            #         except Exception:
            #             detalle = response_envio.content.decode()
                    
            #         results.append({
            #             "factura_id": factura_id,
            #             "mensaje": mensaje,
            #             "detalle": detalle
            #         })
            #     except Exception as e:
            #         print("Error al enviar lote a MH:", str(e))
            #         results.append({
            #             "factura_id": factura_id,
            #             "mensaje": "Error inesperado",
            #             "detalle": str(e)
            #         })
                    
            return JsonResponse({"results": results})
        except Exception as e:
            print(f"Error general en el proceso unificado: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
@csrf_exempt
@require_POST
def enviar_lotes_hacienda_view(request, factura_id):
    print("Inicio enviar factura a MH lote")
    
    contingencia = True
    intento = 1
    intentos_max = 3 #Intentos para envio del dte a MH
    tipo_contingencia_obj = None
    
    fecha_actual = obtener_fecha_actual()
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    # Paso 1: Autenticación contra el servicio de Hacienda
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    emisor = factura.dteemisor or _get_emisor_for_user(request.user, estricto=False)
    if not emisor:
        return JsonResponse({"error": "No se encontró emisor para firmar este DTE."}, status=400)
    nit_empresa = str(emisor.nit) 
    pwd = str(emisor.clave_publica) 
    auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
    auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MiAplicacionDjango/1.0"
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}
    auth_response = None
    response_data = None
    envio_response = None
    try:
        auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

        if auth_response.status_code == 200:
            auth_response_data = auth_response.json()
            token_body = auth_response_data.get("body", {})
            token = token_body.get("token")
            token_type = token_body.get("tokenType", "Bearer")
            roles = token_body.get("roles", [])

            # Si el token viene con el prefijo "Bearer " se remueve
            if token and token.startswith("Bearer "):
                token = token[len("Bearer "):]

            # Actualizamos o creamos el objeto de token
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
        else:
            return JsonResponse({
                "error": "Error en la autenticación",
                "detalle": auth_response_data.get("message", "Error no especificado")
            }, status=auth_response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Error de conexión con el servicio de autenticación",
            "detalle": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Paso 2: Enviar la factura firmada a Hacienda
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    
    token_data_obj = Token_data.objects.filter(activado=True).first()
    if not token_data_obj or not token_data_obj.token:
        return JsonResponse({"error": "No hay token activo para enviar la factura"}, status=status.HTTP_401_UNAUTHORIZED)
    
    codigo_generacion_str = str(factura.codigo_generacion)
    
    # Validación y limpieza del documento firmado
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
        return JsonResponse({
            "error": "Error al parsear el documento firmado",
            "detalle": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    documento_token = firmado_data.get("body", "")
    if not documento_token:
        return JsonResponse({
            "error": "El documento firmado no contiene el token en 'body'"
        }, status=status.HTTP_400_BAD_REQUEST)

    documento_token = documento_token.strip()  # Limpiar espacios innecesarios

    envio_json = {
        "ambiente": "01",  # "00" para Pruebas; "01" para Producción
        "idEnvio": factura.id,
        "version": int(factura.json_original["identificacion"]["version"]),
        "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
        "documento": documento_token,  # Enviamos solo el JWT firmado
        "codigoGeneracion": codigo_generacion_str,
        #Campos para envio de recepcionLote
        #"nitEmisor": str(emisor_fe.nit),
        #"documentos": documento_token # Enviamos solo el JWT firmado
    }

    envio_headers = {
        "Authorization": f"Bearer {token_data_obj.token}",
        "User-Agent": "DjangoApp",
        "Content-Type": "application/json"
    }

    try:
        #URL para el envio de lotes "https://api.dtes.mh.gob.sv/fesv/recepcionlote/",
        #Error: {"error":"Error al enviar la factura","status":400,"detalle":{"timestamp":"2025-04-24T19:08:13.918-0600","status":400,"error":"Bad Request","path":"/fesv/recepcionlote/"}}
        envio_response = requests.post(
            "https://api.dtes.mh.gob.sv/fesv/recepciondte",
            json=envio_json,
            headers=envio_headers
        )
        
        sello_recibido = None

        try:
            response_data = envio_response.json() if envio_response.text.strip() else {}
            sello_recibido = response_data.get("selloRecibido", None)
        except ValueError as e:
            response_data = {"raw": envio_response.text or "No content"}

        if envio_response.status_code == 200 and sello_recibido is not None:
            # Actualizar campos de la factura según la respuesta
            factura.sello_recepcion = response_data.get("selloRecibido", "")
            factura.recibido_mh = True
            # Combinar la respuesta de Hacienda con el JSON original para guardar trazabilidad
            json_response_data = {"jsonRespuestaMh": response_data}
            json_original = factura.json_original
            
            json_nuevo = json_original | json_response_data
            factura.json_original = json.loads(json.dumps(json_nuevo))
            factura.estado = True
            factura.fecha_modificacion = fecha_actual.date()
            factura.hora_modificacion = fecha_actual.time()
            
            #Crear HTML
            html_content = render_to_string('documentos/factura_consumidor/template_factura.html', {"factura": factura}, request=request)
            
            #Guardar archivo pdf
            # Definir ruta de PDF
            pdf_signed_path = os.path.join(RUTA_COMPROBANTES_PDF.url, factura.tipo_dte.codigo, 'pdf', f"{str(factura.codigo_generacion).upper()}.pdf")
            
            print("guardar pdf: ", pdf_signed_path)
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(pdf_signed_path), exist_ok=True)
            
            # Crear y guardar el PDF
            try:
                with open(pdf_signed_path, "wb") as pdf_file:
                    pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)
                    
                if pisa_status.err:
                    print(f"Error al crear el PDF en {pdf_signed_path}")
                else:
                    print(f"PDF guardado exitosamente en {pdf_signed_path}")
            except Exception as e:
                    print(f"Error guardando el PDF: {e}")
            #Enviar correo
            if factura:
                try:
                    enviar_correo_individual_view(request, factura.id, pdf_signed_path, None)
                    factura.envio_correo = True
                except Exception as e:
                        print(f"Error enviando el correo: {e}")
            
            factura.save()
            return JsonResponse({
                "mensaje": "Factura enviada con éxito",
                "respuesta": response_data
            }, status=status.HTTP_200_OK)
        else:
            factura.estado = False
            factura.fecha_modificacion = fecha_actual.date()
            factura.hora_modificacion = fecha_actual.time()
            factura.save()
            return JsonResponse({
                "error": "Error al enviar la factura",
                "status": envio_response.status_code,
                "detalle": response_data
            }, status=envio_response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Error de conexión con Hacienda",
            "detalle": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Finalizacion de eventos en contingencia(hacerlo automatico)
@csrf_exempt
def finalizar_contigencia_view(request):
    print("Finzalizar contingencias activas")

    results = []
    contingencias = []

    try:
        contingencias_activas = []

        #Verificar si existen eventos en contingencia activos de las ultimas 24 horas
        fecha_actual = obtener_fecha_actual()
        fecha_limite = (fecha_actual - timezone.timedelta(hours=24))
        
        # Contingencias activas sin rechazo
        try:
            zona_horaria = pytz.timezone('America/El_Salvador')
            #Agregar al listado las contingencias activas que no fueron enviadas a mh
            eventos = EventoContingencia.objects.filter(rechazado=False, finalizado=False)
            if eventos:
                for evento in eventos:
                    try:
                        fecha_hora_unificada = zona_horaria.localize(datetime.combine(evento.fecha_transmision, evento.hora_transmision))
                        if fecha_hora_unificada <= fecha_limite:
                            contingencias_activas.append(evento)
                    except Exception as e:
                        print(f"Error procesando evento activo: {str(e)}")
        except Exception as e:
            return JsonResponse({"error": f"Error al consultar eventos activos: {str(e)}"})

        # Contingencias rechazadas por MH
        #Agregar al listado las contingencias activas que fueron rechazadas por mh
        try:
            eventos_rechazados_mh = EventoContingencia.objects.filter(rechazado=True, finalizado=False)
            if eventos_rechazados_mh:
                for evento in eventos_rechazados_mh:
                    try:
                        fecha_hora_unificada = zona_horaria.localize(datetime.combine(evento.fecha_modificacion, evento.hora_modificacion))
                        if fecha_hora_unificada <= fecha_limite:
                            contingencias_activas.append(evento)
                    except Exception as e:
                        print(f"Error procesando evento rechazado: {str(e)}")
        except Exception as e:
            return JsonResponse({"error": f"Error al consultar eventos rechazados: {str(e)}"})
        if contingencias_activas:
            for contingencia_activa in contingencias_activas:
                try:
                    if contingencia_activa.finalizado == False:
                        contingencia_activa.finalizado=True
                        contingencia_activa.f_fin = fecha_actual.date()
                        contingencia_activa.h_fin = fecha_actual.time()
                        
                        contingencia_activa.fecha_modificacion = fecha_actual.date()
                        contingencia_activa.hora_modificacion = fecha_actual.time()
                        contingencia_activa.save()
                        contingencias.append(contingencia_activa.codigo_generacion)
                except Exception as e:
                    print(f"Error actualizando contingencia: {str(e)}")
                    
                mensaje = "Contingencias modificadas"
        else:
            mensaje = "Contingencias no encontradas"
        # Finalizar con el retorno de la respuesta
        results.append({
            "contingencia": contingencias,
            "mensaje": mensaje
        })
        return JsonResponse({"results": results})
        
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado al actualizar contingencia: {str(e)}"})

def obtener_fecha_actual():
    try:
        zona_horaria = pytz.timezone('America/El_Salvador')
        fecha_actual = datetime.now(zona_horaria)
        return fecha_actual
    except Exception as e:
        print(f"Error al obtener fecha actual: {str(e)}")
        return None

#Eliminar despues de realizar pruebas
@csrf_exempt
def procesar_respuesta_view(request):
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        factura_id = request.POST.get('factura_id')

        if respuesta == 'si':
            # Procesar acción afirmativa
            print("Usuario aceptó")
        else:
            print("Usuario canceló")

        return redirect('detalle_factura', factura_id=factura_id)
    return HttpResponse("Método no permitido", status=405)

def motivo_contingencia_view(request):
    try:
        factura_id = request.GET.get("factura_id")
        motivo = request.GET.get("motivo")

        print(f"Asignar motivo: factura id: {factura_id}, motivo: {motivo}")

        evento = EventoContingencia.objects.filter(lotes_contingencia__factura=factura_id).first()

        if not evento:
            return JsonResponse({"error": "No se encontró un evento asociado a esta factura."}, status=404)

        fecha_actual = obtener_fecha_actual()

        if not evento.motivo_contingencia:
            evento.motivo_contingencia = motivo
        tipo_contingencia_obj = TipoContingencia.objects.get(codigo="5")
        evento.tipo_contingencia = tipo_contingencia_obj
        evento.fecha_modificacion = fecha_actual.date()
        evento.hora_modificacion = fecha_actual.time()
        evento.save()
        print("Evento modificado: ", evento)
        
        #Actualizar json factura
        try:
            factura = FacturaElectronica.objects.filter(id=factura_id).first()
            print("Factura a modificar: ", factura, factura.json_original["identificacion"])
            if evento and evento.tipo_contingencia and evento.tipo_contingencia.codigo == COD_TIPO_CONTINGENCIA:
                factura.json_original["identificacion"]["tipoContingencia"] = int(evento.tipo_contingencia.codigo)
                factura.json_original["identificacion"]["motivoContin"] = str(evento.motivo_contingencia)
            else:
                factura.json_original["identificacion"]["tipoContingencia"] = None
                factura.json_original["identificacion"]["motivoContin"] = None
            print("Campo a modificado motivo: ", factura.json_original["identificacion"])
            factura.save()
        except Exception as e:
            mensaje = f"Hubo un fallo al crear el lote: {str(e)}"
            print(mensaje)
        
        return redirect (reverse('detalle_factura', args=[factura_id]))
    
    except Exception as e:
        print("Error inesperado: ", e)
        return JsonResponse({"error": f"Hubo un error inesperado: {str(e)}"}, status=500)

#########################################################################################################
# ENVIO DE CORREOS
#########################################################################################################
import glob
#Envio de correos dte

#BC:Guardar archivos pdf y json que posteriormente seran enviados en el correo
#Crear carpeta para almacenar los archivos pdf ubicacion: FE/dtes/tipo_dte/pdf
#La carpeta para almacenar los archivos json ya existe ubicacion: FE/json_facturas

from django.utils.text import slugify
from AUTENTICACION.email_utils import get_smtp_connection_for
import tempfile  # <-- necesario para el PDF temporal
from django.apps import apps as django_apps  # <-- para resolver la ruta de la app

# Helpers PDF
def _fe_app_path():
    """
    Devuelve la ruta absoluta del paquete de la app FE en disco.
    Soporta label 'FE' o 'fe'.
    """
    try:
        return django_apps.get_app_config('FE').path
    except LookupError:
        return django_apps.get_app_config('fe').path  # fallback usual


def _ensure_json_factura(fe_obj, target_path):
    """
    Asegura que exista el JSON de la factura en target_path.
    Si no existe, lo crea desde factura.json_original.
    """
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if not os.path.exists(target_path):
        data = fe_obj.json_original or {}
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return target_path


def _render_pdf_from_template(request, template_name, context):
    """
    Genera un PDF (bytes) desde un template HTML.
    Intenta con WeasyPrint; si falla, usa xhtml2pdf.
    """
    html_string = render_to_string(template_name, context, request=request)
    base_url = request.build_absolute_uri('/')

    # Plan A: WeasyPrint
    try:
        from weasyprint import HTML
        return HTML(string=html_string, base_url=base_url).write_pdf()
    except Exception as e_weasy:
        # Plan B: xhtml2pdf
        try:
            from xhtml2pdf import pisa
            from io import BytesIO
            out = BytesIO()
            status = pisa.CreatePDF(src=html_string, dest=out, encoding='utf-8')
            if status.err:
                raise Exception("xhtml2pdf no pudo generar el PDF")
            return out.getvalue()
        except Exception as e_pisa:
            raise Exception(f"No se pudo generar PDF (WeasyPrint/xhtml2pdf): {e_weasy} / {e_pisa}")

@csrf_exempt
def enviar_correo_individual_view(request, factura_id, archivo_pdf=None, archivo_json=None):
    """
    Envía correo con PDF generado al vuelo y JSON desde FE/json_factura.
    """
    fe = get_object_or_404(FacturaElectronica, id=factura_id)
    receptor = Receptor_fe.objects.filter(id=fe.dtereceptor_id).first()
    emisor = Emisor_fe.objects.filter(id=fe.dteemisor_id).first()

    if not receptor:
        messages.error(request, "No se encontró el receptor.")
        return redirect('detalle_factura', factura_id=factura_id)

    # 1) JSON: FE/json_factura/<numero_control>.json
    try:
        if not archivo_json:
            base_json = os.path.join(_fe_app_path(), "json_factura")
            archivo_json = os.path.join(base_json, f"{fe.numero_control}.json")
        _ensure_json_factura(fe, archivo_json)
    except Exception as e:
        messages.warning(request, f"No se pudo preparar el JSON: {e}")
        archivo_json = None

    # 2) PDF: generar en tiempo real con el template
    #    FE/templates/documentos/factura_consumidor/template_factura.html
    pdf_temp_path = None
    try:
        if not archivo_pdf or not os.path.exists(archivo_pdf):
            ctx = {
                "factura": fe,
                "emisor": emisor,
                "receptor": receptor,
                "detalles": fe.detalles.all().select_related("producto", "unidad_medida"),
                # Agrega aquí más llaves si tu template las necesita:
                "total_pagar": fe.total_pagar,
                "total_iva": fe.total_iva,
                "total_gravadas": getattr(fe, "total_gravadas", 0),
            }
            pdf_bytes = _render_pdf_from_template(
                request,
                "documentos/factura_consumidor/template_factura.html",
                ctx
            )
            # escribir a un tmp para adjuntar
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(pdf_bytes)
            tmp.flush()
            tmp.close()
            pdf_temp_path = tmp.name
            archivo_pdf = pdf_temp_path
    except Exception as e:
        messages.warning(request, f"No se pudo generar el PDF: {e}")
        archivo_pdf = None

    # 3) SMTP desde BD (scope 'fe')
    conn, from_email = get_smtp_connection_for('fe')
    if not from_email:
        messages.error(request, "No hay remitente configurado para correo FE.")
        # limpiar tmp si lo creamos
        if pdf_temp_path and os.path.exists(pdf_temp_path):
            os.unlink(pdf_temp_path)
        return redirect('detalle_factura', factura_id=factura_id)

    correo_destino = receptor.correo or getattr(settings, 'DEFAULT_DTE_FALLBACK_EMAIL', None) or getattr(emisor, 'email', None)
    if not correo_destino:
        messages.error(request, "El receptor no tiene correo y no hay correo de respaldo configurado.")
        if pdf_temp_path and os.path.exists(pdf_temp_path):
            os.unlink(pdf_temp_path)
        return redirect('detalle_factura', factura_id=factura_id)

    estado = "Procesado" if (fe.recibido_mh and fe.sello_recepcion) else ("Contingencia" if fe.contingencia else "Pendiente")
    consultar_url = getattr(CONSULTAR_DTE, 'url_endpoint', '')

    html = f"""
    <p>Estimado/a {receptor.nombre or 'Cliente'},</p>
    <p>Le enviamos su documento electrónico:</p>
    <ul>
        <li><strong>Tipo:</strong> {fe.tipo_dte.descripcion}</li>
        <li><strong>Código de generación:</strong> {str(fe.codigo_generacion).upper()}</li>
        <li><strong>Fecha de emisión:</strong> {fe.fecha_emision:%Y-%m-%d}</li>
        <li><strong>Hora de emisión:</strong> {fe.hora_emision:%H:%M:%S}</li>
        <li><strong>Estado:</strong> {estado}</li>
    </ul>
    <p>Adjuntamos el PDF y el JSON.</p>
    {f'<p>Consultar DTE: {consultar_url}</p>' if consultar_url else ''}
    <br>
    <p>Atentamente,<br>{getattr(emisor, 'nombre_razon_social', 'Emisor')}<br>{getattr(emisor, 'email', from_email)}</p>
    """

    subject = f"Documento Electrónico {fe.tipo_dte.descripcion}"
    email = EmailMessage(
        subject=subject,
        body=html,
        from_email=from_email,
        to=[correo_destino],
        connection=conn,
    )
    email.content_subtype = "html"

    # Adjuntos
    if archivo_pdf and os.path.exists(archivo_pdf):
        with open(archivo_pdf, 'rb') as f:
            email.attach(f"DTE_{slugify(receptor.nombre or 'cliente')}.pdf", f.read(), 'application/pdf')
    else:
        messages.warning(request, "No se adjuntó el PDF porque no se pudo generar o encontrar.")

    if archivo_json and os.path.exists(archivo_json):
        with open(archivo_json, 'rb') as f:
            email.attach(f"DTE_{slugify(fe.numero_control)}.json", f.read(), 'application/json')
    else:
        messages.warning(request, "No se adjuntó el JSON porque no se encontró/creó.")

    try:
        email.send(fail_silently=False)
        fe.envio_correo = True
        fe.save(update_fields=['envio_correo'])
        messages.success(request, f"Correo enviado a {correo_destino}.")
    except Exception as e:
        fe.envio_correo = False
        fe.save(update_fields=['envio_correo'])
        messages.error(request, f"Error al enviar correo: {e}")

    # limpiar tmp
    if pdf_temp_path and os.path.exists(pdf_temp_path):
        os.unlink(pdf_temp_path)

    return redirect('detalle_factura', factura_id=factura_id)

####################################################################################################
# VISTAS DE CONFIGURACION DE EMPRESA
####################################################################################################

@login_required
@transaction.atomic
def configurar_empresa_view(request):

    """
    Una sola pantalla para crear/editar:
      - Emisor_fe (único registro 'mi empresa')
      - representanteEmisor vinculado (FK en Emisor_fe)
    """
    # 1) Cargar el emisor ligado al usuario (si existe)
    emisor = _get_emisor_for_user(request.user, estricto=False)
    rep_inst = getattr(emisor, "representante", None) if emisor else None

    rep_instance = emisor.representante if emisor and emisor.representante_id else None

    if request.method == "POST":
        emisor_form = EmisorForm(request.POST, request.FILES, instance=emisor)
        rep_form = RepresentanteEmisorForm(request.POST, instance=rep_instance)

        if emisor_form.is_valid() and rep_form.is_valid():
            # Guardar representante primero
            representante = rep_form.save()

            # Guardar emisor y enlazar representante
            emisor_obj = emisor_form.save(commit=False)
            emisor_obj.representante = representante
            emisor_obj.save()
            emisor_form.save_m2m()  # actividades_economicas

            messages.success(request, "Configuración de la empresa guardada correctamente.")
            return redirect(reverse("configurar_empresa"))
        else:
            messages.error(request, "Por favor, revise los campos marcados.")
    else:
        emisor_form = EmisorForm(instance=emisor)
        rep_form = RepresentanteEmisorForm(instance=rep_instance)

    context = {
        "emisor_form": emisor_form,
        "rep_form": rep_form,
        "tiene_emisor": bool(emisor),
        "emisor": emisor,
    }
    return render(request, "configurar_empresa.html", context)
