import openpyxl
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import AuthResponseSerializer
from .models import Token_data
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from openpyxl import Workbook

#importaciones para actividad economica
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#IMPORTACIONES DE DTE
from datetime import timedelta
import os
import json
import re
import time
import uuid
import requests
import unicodedata

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import ROUND_HALF_UP, ConversionSyntax, Decimal
from intracoe import settings
from .models import Ambiente, CondicionOperacion, DetalleFactura, FacturaElectronica, Modelofacturacion, NumeroControl, Emisor_fe, ActividadEconomica,  Receptor_fe, Tipo_dte, TipoMoneda, TipoUnidadMedida, TiposDocIDReceptor, Municipio, EventoInvalidacion, TipoInvalidacion, TiposEstablecimientos, Descuento, FormasPago, Plazo
from INVENTARIO.models import Producto, TipoItem, Tributo
from .models import Token_data
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
from .forms import ExcelUploadForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

from django.core import serializers
from django.urls import reverse
from django.views.decorators.http import require_POST
from datetime import datetime
from dateutil.relativedelta import relativedelta

FIRMADOR_URL = "http://192.168.2.25:8113/firmardocumento/"
DJANGO_SERVER_URL = "http://127.0.0.1:8000"

SCHEMA_PATH_fe_fc_v1 = "FE/json_schemas/fe-fc-v1.json"

CERT_PATH = "FE/cert/06142811001040.crt"  # Ruta al certificado

# URLS de Hacienda (Pruebas y Producción)
HACIENDA_URL_TEST = "https://apitest.dtes.mh.gob.sv/fesv/recepciondte"
HACIENDA_URL_PROD = "https://api.dtes.mh.gob.sv/fesv/recepciondte"

#BC 04/03/2025: Constantes
COD_CONSUMIDOR_FINAL = "01"
COD_CREDITO_FISCAL = "03"
VERSION_EVENTO_INVALIDACION = 2
AMBIENTE = Ambiente.objects.get(codigo="01")
#AMBIENTE = "01"
COD_FACTURA_EXPORTACION = "11"
COD_TIPO_INVALIDACION_RESCINDIR = 2
COD_NOTA_CREDITO = "05"
COD_COMPROBANTE_LIQUIDACION = "08"
EMI_SOLICITA_INVALIDAR_DTE = "emisor"
REC_SOLICITA_INVALIDAR_DTE = "receptor"
COD_TIPO_ITEM_OTROS = "4"
COD_TRIBUTOS_SECCION_2 = "2"
COD_DOCUMENTO_RELACIONADO_NO_SELEC = "S"
ID_CONDICION_OPERACION = 2

formas_pago = [] #Asignar formas de pago

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

########################################################################################################

#VISTAS PARA EL EMISOR O EMPRESA
from .models import Emisor_fe
from .forms import EmisorForm

class EmisorListView(ListView):
    model = Emisor_fe
    template_name = 'emisor/list.html'
    context_object_name = 'emisores'
    paginate_by = 10

class EmisorDetailView(DetailView):
    model = Emisor_fe
    template_name = 'emisor/detail.html'

class EmisorCreateView(CreateView):
    model = Emisor_fe
    form_class = EmisorForm  # Usamos nuestro formulario personalizado
    template_name = 'emisor/create.html'
    success_url = reverse_lazy('emisor_list')

class EmisorUpdateView(UpdateView):
    model = Emisor_fe
    template_name = 'emisor/update.html'
    fields = ['nit', 'nombre_razon_social', 'direccion_comercial', 'telefono', 'email', 'actividades_economicas', 'codigo_establecimiento', 'nombre_comercial']
    success_url = reverse_lazy('emisor_list')

class EmisorDeleteView(DeleteView):
    model = Emisor_fe
    template_name = 'emisor/delete.html'
    context_object_name = 'emisor'
    success_url = reverse_lazy('emisor_list')

########################################################################################################

# Cargar el esquema JSON de la factura electrónica
schema_path = "FE/json_schemas/fe-fc-v1.json"
with open(schema_path, "r", encoding="utf-8") as schema_file:
    factura_schema = json.load(schema_file)

# Extraer los campos obligatorios del esquema JSON
required_fields = factura_schema.get("required", [])
properties = factura_schema.get("properties", {})

# Obtener etiquetas y tipos de datos
form_fields = []
for field in required_fields:
    field_type = properties.get(field, {}).get("type", "text")
    form_fields.append({"name": field, "type": field_type})

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

######################################################################################################################

#########################################################################################################
# GENERACION DE DOCUMENTOS ELECTRONICOS
#########################################################################################################

# Función auxiliar para convertir números a letras (stub, cámbiala según tus necesidades)
from num2words import num2words

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

def obtener_numero_control_ajax(request):
    tipo_dte = request.GET.get('tipo_dte', '01')  # Valor por defecto '03' si no se envía ninguno
    #iniciar_dte = request.GET.get('iniciar_dte', False)
    print(f"Inicializando DTE Vista: {tipo_dte}")
    nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
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

from decimal import Decimal, ROUND_HALF_UP
@csrf_exempt
@transaction.atomic
def generar_factura_view(request):
    print("Inicio generar dte")
    #global formas_pago = [] #Asignar formas de pago
    if request.method == 'GET':
        tipo_dte = request.GET.get('tipo_dte', '01')
        emisor_obj = Emisor_fe.objects.first()
        
        if emisor_obj:
            nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)#dte selc. por defecto FE
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
        productos = Producto.objects.all()
        tipooperaciones = CondicionOperacion.objects.all()
        tipoDocumentos = Tipo_dte.objects.all()
        tipoItems = TipoItem.objects.all()
        descuentos = Descuento.objects.all()
        formasPago = FormasPago.objects.all()

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
            "formasPago": formasPago
        }
        return render(request, "generar_dte.html", context)

    elif request.method == 'POST':
        try:
            items_permitidos = 2000
            data = json.loads(request.body)
            docsRelacionados = []#Acumular los documentos relacionados
            # Datos básicos
            numero_control = data.get('numero_control', '')
            print(f"Numero de control: {numero_control}")
            codigo_generacion = data.get('codigo_generacion', '')
            receptor_id = data.get('receptor_id', None)
            
            nit_receptor = data.get('nit_receptor', '')
            nombre_receptor = data.get('nombre_receptor', '')
            direccion_receptor = data.get('direccion_receptor', '')
            telefono_receptor = data.get('telefono_receptor', '')
            correo_receptor = data.get('correo_receptor', '')
            observaciones = data.get('observaciones', '')
            tipo_dte = data.get("tipo_documento_seleccionado", None) #BC: obtiene la seleccion del tipo de documento desde la pantalla del sistema
            tipo_item = data.get("tipo_item_select", None)
            print("Tipo de item seleccionado: ", tipo_item)
            tipo_doc_relacionar = data.get("documento_seleccionado", None)
            documento_relacionado = data.get("documento_relacionado", None)
            porcentaje_descuento = data.get("descuento_select", "0")
            porcentaje_descuento_item = Decimal(porcentaje_descuento.replace(",", "."))
            

            # Configuración adicional
            tipooperacion_id = data.get("condicion_operacion", None)
            porcentaje_retencion_iva = Decimal(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = data.get("retencion_iva", False)
            productos_retencion_iva = data.get("productos_retencion_iva", [])
            porcentaje_retencion_renta = Decimal(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = data.get("retencion_renta", False)
            productos_retencion_renta = data.get("productos_retencion_renta", [])
            formaPago = data.get("forma_pago_seleccionada", None)
            
            descuento_global = data.get("descuento_global_input", "0")
            saldo_favor = data.get("saldo_favor_input", "0")
            base_imponible_checkbox = data.get("no_gravado", False)
            
            if saldo_favor is not None and saldo_favor !="":
                saldo_f = Decimal(saldo_favor)
                if saldo_f > Decimal("0.00"):
                    saldo_favor = saldo_f * Decimal("-1")
                else:
                    saldo_favor = Decimal("0.00")
            else:
                saldo_favor = Decimal("0.00")
            print("-Saldo a Favor: ", saldo_favor)

            # Datos de productos
            productos_ids = data.get('productos_ids', [])
            cantidades = data.get('cantidades', [])
            # En este caso, se asume que el descuento por producto es 0 (se aplica globalmente)
            
            if numero_control:
                numero_control = NumeroControl.obtener_numero_control(tipo_dte)
                print(numero_control)
            if not codigo_generacion:
                codigo_generacion = str(uuid.uuid4()).upper()

            # Obtener emisor
            emisor_obj = Emisor_fe.objects.first()
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
            ambiente_obj = Ambiente.objects.get(codigo="01")
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            tipo_item_obj = TipoItem.objects.get(codigo=tipo_item)

            tipomodelo_obj = Modelofacturacion.objects.get(codigo="1")
            tipooperacion_obj = CondicionOperacion.objects.get(id=tipooperacion_id) if tipooperacion_id else None
            tipo_moneda_obj = TipoMoneda.objects.get(codigo="USD")

            print("-Base imponible: ", base_imponible_checkbox)
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
            
            #Campos DTE
            tributo_valor = None

            # Recorrer productos para crear detalles (realizando el desglose)
            for index, prod_id in enumerate(productos_ids):
                try:
                    producto = Producto.objects.get(id=prod_id)
                except Producto.DoesNotExist:
                    continue
                
                # Obtener unidad de medida
                #Unidad de medida = 99 cuando el contribuyente preste un servicio
                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo="99")
                else:
                    unidad_medida_obj = TipoUnidadMedida.objects.get(codigo=producto.unidad_medida.codigo)
                print("-Unidad de medida: ", unidad_medida_obj)

                #Cantidad = 1, Si se utiliza el campo base imponible, si el tipo de item es 4, ...
                if base_imponible_checkbox is True or tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    cantidad = 1
                else:
                    cantidad = int(cantidades[index]) if index < len(cantidades) else 1
                    print("-Cantidad modificada", cantidad)
                
                # El precio del producto ya incluye IVA (por ejemplo, 8.50)
                precio_incl = producto.preunitario

                # Calcular precio neto y IVA unitario
                #precio_neto = (precio_incl / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                #precio_neto = (precio_incl ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                #Campo tributos
                if (base_imponible_checkbox is False and tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS) or tipo_dte_obj.codigo == COD_CREDITO_FISCAL: #factura.tipo_dte.codigo != COD_CONSUMIDOR_FINAL and
                    # Codigo del tributo (tributos.codigo)
                    tributoIva = Tributo.objects.get(codigo="20")#IVA este codigo solo aplica a ventas gravadas(ya que estan sujetas a iva)
                    tributo_valor = Tributo.objects.get(codigo="20").valor_tributo
                    tributos = [str(tributoIva.codigo)]
                else:
                    tributos = None
                print("-Tributos: ", tributos)
                
                print("-tributo_valor: ", tributo_valor)
                if tributo_valor is None:
                    tributo_valor = Decimal("0.00")
                
                #Campo precioUni
                if base_imponible_checkbox is True:
                    precio_neto = float(0.00)
                elif base_imponible_checkbox is False and tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL : #si es FE agregarle iva al prod
                    precio_neto = (precio_incl * Decimal("1.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:  #Cuando no es FE quitarle iva al precio si se aplico desde el producto
                    precio_neto = (precio_incl / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #BC: verificar si el precio del prod para ccf ya viene con iva
                    #total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print(f"Precio Incl = {precio_incl}, Precio neto = {precio_neto}, tipo dte:  {tipo_dte}")
                
                
                if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                    print("-Precio neto: ", precio_neto)
                    precio_neto = precio_neto * Decimal(tributo_valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    print("-Precio neto con valor trib: ", precio_neto)
                
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #Campo descuento por bonificaciones(montoDescu)
                #descuento_monto = descuento_monto # Se asume 0 descuento por ítem
                
                porcentaje_descuento_item = Descuento.objects.get(id=porcentaje_descuento)
                print("-Descuento a aplicar: ", porcentaje_descuento)
                if porcentaje_descuento_item.porcentaje > Decimal("0.00"):
                    descuento_aplicado=True
                else:
                    descuento_aplicado = False
                print("-Descuento por item", porcentaje_descuento_item.porcentaje)

                #descuento_monto = Decimal("0.00")  # Se asume 0 descuento por ítem
                
                # Totales por ítem
                #Campo Ventas gravadas
                total_neto = ((precio_neto * cantidad) - (porcentaje_descuento_item.porcentaje / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                #total_iva_item = (iva_unitario * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #funcional total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                print(f"IVA Item = {total_iva_item}, iva unitario = {iva_unitario}, cantidad = {cantidad}, total neto = {total_neto} ")
                
                #total_con_iva = (precio_incl * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                
                #Campo codTributo
                cuerpo_documento_tributos = []
                tributo = None
                if producto.tributo is None:
                    seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                    return JsonResponse({"error": "Seleccionar tributo para el producto" })
                
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
                    precio_unitario=precio_incl,  # Se almacena el precio bruto (con IVA)
                    descuento = porcentaje_descuento_item,
                    tiene_descuento = descuento_aplicado,
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=total_neto,  # Total neto
                    pre_sug_venta=precio_incl,
                    no_gravado=Decimal("0.00"),
                    saldo_favor=saldo_favor
                )

                total_gravada += total_neto
                
                #Calcular el valor del tributo
                if tipo_dte_obj.codigo == COD_CREDITO_FISCAL:
                    valorTributo = ( Decimal(total_gravada) * Decimal(tributo_valor) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_operaciones = total_gravada + valorTributo
                else:
                    total_operaciones = total_gravada
                print("-Calcular el total de operaciones: ", total_operaciones)
                
                if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
                    total_con_iva = (precio_neto * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:
                    #total_con_iva = (precio_neto * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    total_con_iva = total_operaciones - DecimalIvaPerci - DecimalRetIva - DecimalRetRenta - total_no_gravado
                    print("-Total pagar: ", total_con_iva)
                
                total_iva += total_iva_item
                total_pagar += total_con_iva
                
                # Actualizamos manualmente los campos calculados
                detalle.total_sin_descuento = total_neto
                detalle.iva = total_iva_item
                detalle.total_con_iva = total_con_iva
                detalle.iva_item = total_iva_item  # Guardamos el total IVA para este detalle
                detalle.save()
                
                #saldo.compare(Decimal("0.00")) > 0:
                
                print("-Aplicar tributo sujeto iva")
                valor_porcentaje = Decimal(porcentaje_descuento_item.porcentaje)
                
                print("-Validar porcentaje")
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

            # Actualizar totales en la factura
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = total_gravada
            factura.sub_total_ventas = total_gravada
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = total_descuento_gravado
            factura.por_descuento = descuento_global #Decimal("0.00")
            factura.total_descuento = total_descuento_gravado
            factura.sub_total = total_gravada
            factura.iva_retenido = DecimalRetIva
            factura.retencion_renta = DecimalRetRenta
            factura.total_operaciones = total_operaciones #total_gravada
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = total_pagar
            factura.total_letras = num_to_letras(total_pagar)
            factura.total_iva = total_iva
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = DecimalIvaPerci
            factura.tipo_documento_relacionar = tipo_doc_relacionar
            factura.documento_relacionado = documento_relacionado
            factura.save()

            # Construir el cuerpoDocumento para el JSON con desglose
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                        
                print("-N° items: ", idx)
                #baseImponible = det.base_imponible
                print("-Base imponible: ", base_imponible_checkbox)
                #Items permitidos 2000
                if idx > items_permitidos:
                    return JsonResponse({"error": "Cantidad máxima de ítems permitidos " }, {items_permitidos})
                else:
                    codTributo = None 
                    tributo_valor = None
                    #Verificar los documentos relacionados (maximo deben ser 50)
                    if tipo_doc_relacionar is not None and tipo_doc_relacionar != COD_DOCUMENTO_RELACIONADO_NO_SELEC:
                        #Agregar todos los documentos relacionados a la lista
                        if docsRelacionados is not None:
                            for docRelacionado in docsRelacionados:
                                if docRelacionado != documento_relacionado:
                                    docsRelacionados.append(documento_relacionado)
                        else:
                            docsRelacionados.append(documento_relacionado)
                        print(f"-Lista de documentos relacionados: {docsRelacionados} ")
                        #Si la lista ya supera 50 docs relacionados detener el proceso de agregado de items
                        if len(docsRelacionados) > 50:
                            documentosRelacionadosMensaje = "Cantidad maxima permitida de documentos relacionados: 50"
                            return JsonResponse({"error": "Cantidad maxima permitida de documentos relacionados: 50" })
                    
                    #Campo codTributo
                    cuerpo_documento_tributos = []
                    if det.producto.tributo is None:
                        seleccionarTributoMensaje = "Seleccionar tributo para el producto"
                        return JsonResponse({"error": "Seleccionar tributo para el producto" })
                    else:
                        if tipo_item_obj.codigo == COD_TIPO_ITEM_OTROS:
                            #codTributo = None 
                            codTributo = tributo.codigo
                            #if tipo_dte_obj.codigo == COD_CREDITO_FISCAL:
                                #codTributo = tributo.codigo #MH: Cuando se haga uso de este campo se permitira adicionar unicamente el codigo 20-IVA 
                                #print("-Tributo asociado al prod: ", tributo)
                               # print("-Cod tributo: ", codTributo)
                            #else:
                                #codTributo = None
                            
                            #Si el tributo asociado el prod pertenece a la seccion 2 de la tabla agregar un segundo item
                            if tributo.tipo_tributo.codigo == COD_TRIBUTOS_SECCION_2:
                                print("-Crear nuevo item")
                                #Nuevo item (requerido cuando el tributo es de la seccion 2)
                                cuerpo_documento_tributos.append({
                                    "numItem": idx+1,
                                    "tipoItem": int(tipo_item_obj.codigo),
                                    "numeroDocumento": None,
                                    "codigo": str(det.producto.codigo),
                                    "codTributo": codTributo,
                                    "descripcion": str(tributo.descripcion),
                                    "cantidad": float(cantidad), #float(det.cantidad),
                                    "uniMedida": int(unidad_medida_obj.codigo), #int(det.unidad_medida.codigo) if det.unidad_medida.codigo.isdigit() else 59,
                                    "precioUni": float(precio_neto),      # Precio unitario neto
                                    #"ivaUnitario": float(iva_unitario),     # IVA unitario
                                    #"totalNeto": float(total_neto),         # Total neto por ítem
                                    #"totalIva": float(total_iva_item),       # Total IVA por ítem
                                    #"totalConIva": float(total_con_iva),     # Total con IVA por ítem
                                    "montoDescu": float(porcentaje_descuento_item.porcentaje),
                                    "ventaNoSuj": float(0.0),
                                    "ventaExenta": float(0.0),
                                    "ventaGravada": float(det.ventas_gravadas),#BC: Revisar
                                    "tributos": tributos, #iva para todos los items 
                                    "psv": 0.0,
                                    "noGravado": float(0.0),
                                    #"ivaItem": float(total_iva_item)        # IVA total por línea
                                })
                        
                    # Recalcular (para el JSON) usando los valores ya calculados:
                    #precio_neto = (Decimal(det.precio_unitario) / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE DEBE INCLUIRSE EL IVA EN EL PRECIO
                    #precio_neto = (Decimal(det.precio_unitario) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #iva_unitario = (Decimal(det.precio_unitario) - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE DEBE INCLUIRSE EL IVA EN EL PRECIO
                    #iva_unitario = (Decimal(det.precio_unitario)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #total_neto = (precio_neto * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #total_iva_item = (iva_unitario * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE EL CALCULO ES DIFERENTE
                    #total_iva_item = ( ( iva_unitario * det.cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    print(f"-Total IVA = {total_iva_item}")
                    
                    #total_con_iva = (Decimal(det.precio_unitario) * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                    print(f"Item {idx}: IVA unitario = {iva_unitario}, Total IVA = {total_iva_item}, IVA almacenado = {det.iva_item}")
                    
                    print("-Cod tributo: ", codTributo)
                    cuerpo_documento.append({
                        "numItem": idx,
                        "tipoItem": int(tipo_item_obj.codigo),
                        "numeroDocumento": None,#str(documento_relacionado) if str(documento_relacionado) else None,
                        "codigo": str(det.producto.codigo),
                        "codTributo": codTributo,
                        "descripcion": str(det.producto.descripcion),
                        "cantidad": float(cantidad), #float(det.cantidad),
                        "uniMedida": int(unidad_medida_obj.codigo), #int(det.unidad_medida.codigo) if det.unidad_medida.codigo.isdigit() else 59,
                        "precioUni": float(precio_neto),      # Precio unitario neto
                        #"ivaUnitario": float(iva_unitario),     # IVA unitario
                        #"totalNeto": float(total_neto),         # Total neto por ítem
                        #"totalIva": float(total_iva_item),       # Total IVA por ítem
                        #"totalConIva": float(total_con_iva),     # Total con IVA por ítem
                        "montoDescu": float(porcentaje_descuento_item.porcentaje),#float(det.descuento),
                        "ventaNoSuj": float(det.ventas_no_sujetas),
                        "ventaExenta": float(det.ventas_exentas),
                        "ventaGravada": float(det.ventas_gravadas),
                        "tributos": tributos, #iva para todos los items 
                        "psv": 0.0,
                        "noGravado": float(det.no_gravado),
                        #"ivaItem": float(total_iva_item)        # IVA total por línea
                    })
                                        
                    #cuerpo_documento_tributos[0] = idx + 1
                    if cuerpo_documento_tributos is None:
                        cuerpo_documento.append(cuerpo_documento_tributos)
                  
                print(f"Item {idx}: IVA unitario = {iva_unitario}, Total IVA = {total_iva_item}, IVA almacenado = {det.iva_item}")

            """factura_json = {
                "identificacion": {
                    "version": 1,
                    "ambiente": ambiente_obj.codigo,
                    "tipoDte": str(tipo_dte_obj.codigo),
                    "numeroControl": str(factura.numero_control),
                    "codigoGeneracion": str(factura.codigo_generacion),
                    "tipoModelo": 1,
                    "tipoOperacion": 1,
                    "tipoContingencia": None,
                    "motivoContin": None,
                    "fecEmi": str(factura.fecha_emision),
                    "horEmi": factura.hora_emision.strftime('%H:%M:%S'),
                    "tipoMoneda": str(factura.tipomoneda.codigo) if factura.tipomoneda else "USD"
                },
                "documentoRelacionado": None,
                "emisor": {
                    "nit": str(emisor.nit),
                    "nrc": str(emisor.nrc),
                    "nombre": str(emisor.nombre_razon_social),
                    "codActividad": str(emisor.actividades_economicas.first().codigo) if emisor.actividades_economicas.exists() else "",
                    "descActividad": str(emisor.actividades_economicas.first().descripcion) if emisor.actividades_economicas.exists() else "",
                    "nombreComercial": str(emisor.nombre_comercial),
                    "tipoEstablecimiento": str(emisor.tipoestablecimiento.codigo) if emisor.tipoestablecimiento else "",
                    "direccion": {
                        "departamento": "05",
                        "municipio": "19",
                        "complemento": emisor.direccion_comercial
                    },
                    "telefono": str(emisor.telefono),
                    "correo": str(emisor.email),
                    "codEstableMH": str(emisor.codigo_establecimiento or "M001"),
                    "codEstable": "0001",
                    "codPuntoVentaMH": str(emisor.codigo_punto_venta or "P001"),
                    "codPuntoVenta": "0001",
                },
                "receptor": {
                    "tipoDocumento": tipo_documento_receptor,#str(receptor.tipo_documento.codigo) if receptor.tipo_documento else "",
                    "numDocumento": num_documento_receptor,
                    "nit": str(receptor.num_documento),
                    "nrc": receptor.nrc,
                    "nombre": str(receptor.nombre),
                    "codActividad": "24310",
                    "descActividad": "undición de hierro y acero",
                    "direccion": {
                        "departamento": "05",
                        "municipio": "19",
                        "complemento": receptor.direccion or ""
                    },
                    "telefono": receptor.telefono or "",
                    "correo": receptor.correo or "",
                    #BC 04/03/2025
                    "nombreComercial": str(receptor.nombreComercial)
                },
                "otrosDocumentos": None,
                "ventaTercero": None,
                "cuerpoDocumento": cuerpo_documento,
                "resumen": {
                    "totalNoSuj": float(factura.total_no_sujetas),
                    "totalExenta": float(factura.total_exentas),
                    "totalGravada": float(factura.total_gravadas),
                    "subTotalVentas": float(factura.sub_total_ventas),
                    "descuNoSuj": float(factura.descuen_no_sujeto),
                    "descuExenta": float(factura.descuento_exento),
                    "descuGravada": float(factura.descuento_gravado),
                    "porcentajeDescuento": float(factura.por_descuento),
                    "totalDescu": float(factura.total_descuento),
                    "subTotal": float(factura.sub_total),
                    "ivaRete1": float(factura.iva_retenido),
                    "reteRenta": float(factura.retencion_renta),
                    "montoTotalOperacion": float(factura.total_operaciones),
                    "totalNoGravado": float(factura.total_no_gravado),
                    "totalPagar": float(factura.total_pagar),
                    "totalLetras": factura.total_letras,
                    "totalIva": float(factura.total_iva),
                    "saldoFavor": 0.0,
                    "condicionOperacion": int(factura.condicion_operacion.codigo) if factura.condicion_operacion and factura.condicion_operacion.codigo.isdigit() else 1,
                    "pagos": None,
                    "tributos": None,
                    "numPagoElectronico": None
                },
                "extension": {
                    "nombEntrega": None,
                    "docuEntrega": None,
                    "nombRecibe": None,
                    "docuRecibe": None,
                    "observaciones": observaciones,
                    "placaVehiculo": None
                },
                "apendice": None,
            }"""
            print("-Saldo a favor: ", saldo_favor)
            factura_json = generar_json(ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento, observaciones, Decimal(str(total_iva_item)), base_imponible_checkbox, saldo_favor)
            
            factura.json_original = factura_json
            if formas_pago is not None and formas_pago !=[]:
                factura.formas_Pago = formas_pago
            factura.save()
            print("-Cambios asignados en factura")

            # Guardar el JSON en la carpeta "FE/json_facturas"
            json_path = os.path.join("FE/json_facturas", f"{factura.numero_control}.json")
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(factura_json, f, indent=4, ensure_ascii=False)

                return JsonResponse({
                    "mensaje": "Factura generada correctamente",
                    "factura_id": factura.id,
                    "numero_control": factura.numero_control,
                    "redirect": reverse('detalle_factura', args=[factura.id])
                })
        except Exception as e:
            print(f"Error al generar la factura: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

#BC 05/03/2025:
def generar_json(ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento, observaciones, iva_item_total, base_imponible_checkbox, saldo_favor):
    print("-Inicio llenar json")
    print("-Saldo a favor: ", saldo_favor)
    try:
        if saldo_favor is None or saldo_favor == "":
            saldo_favor = Decimal("0.00")
        
        #Resumen tributos
        tributo = Tributo.objects.get(codigo="20")
        
        #Llenar json
        json_identificacion = {
            "version": tipo_dte_obj.version,
            "ambiente":  ambiente_obj.codigo,
            "tipoDte": str(tipo_dte_obj.codigo),
            "numeroControl": str(factura.numero_control),
            "codigoGeneracion": str(factura.codigo_generacion),
            "tipoModelo": 1,
            "tipoOperacion": 1,
            "tipoContingencia": None,
            "motivoContin": None,
            "fecEmi": str(factura.fecha_emision),
            "horEmi": factura.hora_emision.strftime('%H:%M:%S'),
            "tipoMoneda": str(factura.tipomoneda.codigo) if factura.tipomoneda else "USD"
        }
        
        json_documento_relacionado = None
        
        json_emisor = {
            "nit": str(emisor.nit),
            "nrc": str(emisor.nrc),
            "nombre": str(emisor.nombre_razon_social),
            "codActividad": str(emisor.actividades_economicas.first().codigo) if emisor.actividades_economicas.exists() else "",
            "descActividad": str(emisor.actividades_economicas.first().descripcion) if emisor.actividades_economicas.exists() else "",
            "nombreComercial": str(emisor.nombre_comercial),
            "tipoEstablecimiento": str(emisor.tipoestablecimiento.codigo) if emisor.tipoestablecimiento else "",
            "direccion": {
                "departamento": "05",
                "municipio": "19",
                "complemento": emisor.direccion_comercial
            },
            "telefono": str(emisor.telefono),
            "correo": str(emisor.email),
            "codEstableMH": str(emisor.codigo_establecimiento or "M001"),
            "codEstable": "0001",
            "codPuntoVentaMH": str(emisor.codigo_punto_venta or "P001"),
            "codPuntoVenta": "0001",
        }
                
        json_receptor = {
            #"nit": str(receptor.num_documento),
            #"nrc": str(receptor.nrc) if str(receptor.nrc) else None,
            "nombre": str(receptor.nombre),
            "codActividad": "24310",
            "descActividad": "undición de hierro y acero",
            "direccion": {
                "departamento": "05",
                "municipio": "19",
                "complemento": receptor.direccion or ""
            },
            "telefono": receptor.telefono or "",
            "correo": receptor.correo or "",
            #BC 04/03/2025
            #"nombreComercial": str(receptor.nombre)
        }
        
        json_otros_documentos = None
        
        total_operaciones = Decimal("0.00")
        
        pagos = formas_pago
        print("Pagos: ", pagos)
        
        json_resumen = {
            "totalNoSuj": float(factura.total_no_sujetas),
            "totalExenta": float(factura.total_exentas),
            "totalGravada": float(factura.total_gravadas),
            "subTotalVentas": float(factura.sub_total_ventas),
            "descuNoSuj": float(factura.descuen_no_sujeto),
            "descuExenta": float(factura.descuento_exento),
            "descuGravada": float(factura.descuento_gravado),
            "porcentajeDescuento": float(factura.por_descuento),
            "totalDescu": float(factura.total_descuento),
            "subTotal": float(factura.sub_total),
            "ivaRete1": float(factura.iva_retenido),
            "reteRenta": float(factura.retencion_renta),
            "montoTotalOperacion": float(factura.total_operaciones),
            "totalNoGravado": float(factura.total_no_gravado),
            "totalPagar": float(factura.total_pagar),
            "totalLetras": factura.total_letras,
            #"totalIva": float(factura.total_iva),
            "saldoFavor": float(saldo_favor),#0.0,
            "condicionOperacion": int(factura.condicion_operacion.codigo) if factura.condicion_operacion and factura.condicion_operacion.codigo.isdigit() else 1,
            "pagos": pagos,
            #"tributos": None,
            "numPagoElectronico": None
        }
        
        print("-Subtoltalventas: ", json_resumen["subTotalVentas"])
        
        json_extension = {
            "nombEntrega": None,
            "docuEntrega": None,
            "nombRecibe": None,
            "docuRecibe": None,
            "observaciones": observaciones,
            "placaVehiculo": None
        }
        
        json_apendice = None
        
        #Modificacion de json en base al tipo dte a generar
        if receptor is not None:
            nrc_receptor = None
            if receptor.nrc is not None and receptor.nrc !="None":
                nrc_receptor = str(receptor.nrc)
            json_receptor["nrc"] = nrc_receptor
        
        #Calcular el valor total del tributo
        subTotalVentas = json_resumen["subTotalVentas"]
        valorTributo = ( Decimal(subTotalVentas) * Decimal(tributo.valor_tributo) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        json_resumen["tributos"] = [
                {
                "codigo": str(tributo.codigo),
                "descripcion": str(tributo.descripcion),
                "valor": float(valorTributo)
                }
            ]
        print("-Valor tributos: ", json_resumen["tributos"])
        
        if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
            json_receptor["tipoDocumento"] = str(receptor.tipo_documento.codigo) if receptor.tipo_documento else ""
            json_receptor["numDocumento"] = str(receptor.num_documento) 
            
            #iva_item_total obtener solo el monto
            valor_iva_item = iva_item_total
            
            #Recorrer items y modificar campo ivaItem cuando son FE
            for i, cuerpo in enumerate(cuerpo_documento):
                print("-Cod tributo del cuerpo doc: ", cuerpo["codTributo"])
                #Remover el item
                cuerpo_documento.pop(i)
                #Modificar campo
                cuerpo["ivaItem"] = float(valor_iva_item)
                #Agregar nuevamente el item
                cuerpo_documento.insert(i, cuerpo)
                if cuerpo["tipoItem"] != COD_TIPO_ITEM_OTROS:
                    #cuerpo["codTributo"] = None
                    if base_imponible_checkbox == True:
                        cuerpo["tributos"] = None
            print("-Cod tributo del cuerpo doc: ", cuerpo["codTributo"])
            json_resumen["totalIva"] = float(factura.total_iva)
            #json_resumen["montoTotalOperacion"] = float(factura.total_operaciones)
            json_resumen["totalPagar"] = float(factura.total_pagar)
            json_resumen["tributos"] = None
        elif tipo_dte_obj.codigo == COD_CREDITO_FISCAL:
            json_receptor["nit"] = str(receptor.num_documento)
            json_receptor["nombreComercial"] = str(receptor.nombreComercial)
            json_resumen["ivaPerci1"] = float(factura.iva_percibido)
            
            if base_imponible_checkbox == True:
                json_resumen["tributos"] = None
            
            print("-Asignar tributos")
            #Asignar tributos
            if json_resumen["tributos"] is not None and json_resumen["tributos"] !="":
                tributo = json_resumen["tributos"]
                tributo_valor = tributo[0]
                subtotal = float(factura.sub_total)
                valor_tributos = float(tributo_valor["valor"])
                #suma_operaciones = subtotal + valor_tributos
                #total_operaciones = Decimal(str(suma_operaciones)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                #json_resumen["montoTotalOperacion"] = float(total_operaciones)
                #total_pagar = json_resumen["montoTotalOperacion"] - json_resumen["ivaPerci1"] - json_resumen["ivaRete1"] - json_resumen["reteRenta"] - json_resumen["totalNoGravado"]
                #json_resumen["totalPagar"] = total_pagar
                
        if json_resumen["saldoFavor"] is not None and json_resumen["saldoFavor"] !="" and Decimal(json_resumen["saldoFavor"]).compare(Decimal("0.00")) > 0:
            print("-Asignar condicion operacion 1")
            json_resumen["condicionOperacion"] = int(CondicionOperacion.objects.get(codigo="1").codigo) #Al contado
            
        json_completo = {
            "identificacion": json_identificacion,
            "documentoRelacionado": json_documento_relacionado,
            "emisor": json_emisor,
            "receptor": json_receptor,
            "otrosDocumentos": json_otros_documentos,
            "ventaTercero": None,
            "cuerpoDocumento": cuerpo_documento,
            "resumen": json_resumen,
            "extension": json_extension,
            "apendice": json_apendice
        }
        
        return json_completo
    except Exception as e:
            print(f"Error al generar el json de la factura: {e}")
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt    
def invalidacion_dte_view(request, factura_id):
    
    #Generar json, firmar, enviar a mh
    
    codigo_generacion_invalidacion = str(uuid.uuid4()).upper()
    print("-Codigo generacion evento invalidacion ", codigo_generacion_invalidacion)
    factura_invalidar = FacturaElectronica.objects.get(id=factura_id)#Buscar dte a invalidar
    """#Validar plazos de invalidacion
    tipo_dte = str(factura_invalidar.tipo_dte.codigo)
    if tipo_dte == COD_CONSUMIDOR_FINAL or tipo_dte == COD_FACTURA_EXPORTACION:
        #3 meses permitidos par FE y FEX
        fecha_actual = datetime.now()
        fecha_limite_inv = fecha_actual - relativedelta(months=3)
        #24 horas para el resto de DTEs
        fecha_hora_emision = factura_invalidar.fecha_emision + " " + factura_invalidar.hora_emision
        diferencia = fecha_actual - fecha_hora_emision
                
        print("-Fecha limite ", fecha_limite_inv)
        print("-Fecha de emision", factura_invalidar.fecha_emision)
        
        if factura_invalidar.fecha_emision > fecha_limite_inv:
            return JsonResponse({
                "mensaje": "No permitido, plazo para invalidar documento 3 meses"
            })
        else:
            if diferencia >= timedelta(days=1):
                return JsonResponse({
                    "mensaje": "No permitido, plazo para invalidar documento 24 horas"
                })
    """
    
    #Tipo Invalidacion
    tipo_invalidacion = TipoInvalidacion.objects.get(codigo="2") #Campo dinamico
    print("-Tipo anulacion: ", tipo_invalidacion)
    #Quien solicita invalidar el dte, el emisor o receptor
    solicitud = "receptor" #Campo dinamico
    
    try: 
        if factura_invalidar is not None:
            print("-Factura a invalidar encontrada", factura_invalidar)
            #Buscar si la factura ya tiene un evento de invalidacion
            evento_invalidacion = EventoInvalidacion.objects.filter(factura__codigo_generacion=factura_invalidar.codigo_generacion).first()
            
            if evento_invalidacion is None:
                #Llenar registro en tabla
                evento_invalidacion = EventoInvalidacion.objects.create(
                    codigo_generacion = codigo_generacion_invalidacion,
                    factura = factura_invalidar,
                    tipo_invalidacion = tipo_invalidacion,
                    motivo_anulacion = tipo_invalidacion.descripcion, #Campo dinamico
                    codigo_generacion_r = factura_invalidar.codigo_generacion,
                    solicita_invalidacion = solicitud
                )
            else:
                evento_invalidacion.tipo_invalidacion = tipo_invalidacion
                evento_invalidacion.motivo_anulacion = tipo_invalidacion.descripcion #Campo dinamico
                evento_invalidacion.codigo_generacion_r = factura_invalidar.codigo_generacion
                evento_invalidacion.solicita_invalidacion = solicitud
                evento_invalidacion.save()
            
            json_identificacion_inv = {
                "version": int(VERSION_EVENTO_INVALIDACION), #Version vigente 2
                "ambiente": "01", #str(Ambiente.codigo),
                "codigoGeneracion": str(evento_invalidacion.codigo_generacion).upper(),
                "fecAnula": str(evento_invalidacion.fecha_anulacion),
                "horAnula": str(evento_invalidacion.hora_anulacion.strftime('%H:%M:%S'))
            }
            
            tipo_establecimiento = TiposEstablecimientos.objects.get(codigo=evento_invalidacion.factura.dteemisor.tipoestablecimiento.codigo)
            
            json_emisor_inv = {
                "nit": str(evento_invalidacion.factura.dteemisor.nit),
                "nombre": str(evento_invalidacion.factura.dteemisor.nombre_razon_social),
                "tipoEstablecimiento": str(tipo_establecimiento.codigo),
                "nomEstablecimiento": str(tipo_establecimiento.descripcion),
                "codEstableMH": str(evento_invalidacion.factura.dteemisor.codigo_establecimiento or "M001"),
                "codEstable": "0001",
                "codPuntoVentaMH": str(evento_invalidacion.factura.dteemisor.codigo_punto_venta or "P001"),
                "codPuntoVenta": "0001",
                "telefono": str(evento_invalidacion.factura.dteemisor.telefono),
                "correo": str(evento_invalidacion.factura.dteemisor.email)
            }
            
            json_documento_inv = {
                "tipoDte" : str(evento_invalidacion.factura.tipo_dte.codigo),
                "codigoGeneracion" : str(factura_invalidar.codigo_generacion).upper(),
                "selloRecibido" : str(factura_invalidar.sello_recepcion),
                "numeroControl" : str(factura_invalidar.numero_control),
                "fecEmi" : str(factura_invalidar.fecha_emision),
                "tipoDocumento" : str(evento_invalidacion.factura.dtereceptor.tipo_documento.codigo),
                "numDocumento" : str(evento_invalidacion.factura.dtereceptor.num_documento),
                "nombre" : str(evento_invalidacion.factura.dtereceptor.nombre),
                "telefono" : str(evento_invalidacion.factura.dtereceptor.telefono),
                "correo" : str(evento_invalidacion.factura.dtereceptor.correo) 
            }
            print("-Json motivo-tipo anulacion", evento_invalidacion.tipo_invalidacion)
            json_motivo_inv = {
                "tipoAnulacion" : int(evento_invalidacion.tipo_invalidacion.codigo),
                "motivoAnulacion" : str(evento_invalidacion.motivo_anulacion),
                "nombreResponsable" : str(evento_invalidacion.factura.dteemisor.nombre_razon_social),
                "tipDocResponsable" : str(evento_invalidacion.factura.dteemisor.tipo_documento.codigo),
                "numDocResponsable" : str(evento_invalidacion.factura.dteemisor.nit),
            }
            
            #----------Modificaciones en json segun el dte a invalidar
            
            #Si el DTE a invalidar es F, CCF o FEX agregar campo "montoIva"
            tipo_dte_invalidar = evento_invalidacion.factura.tipo_dte.codigo
            if tipo_dte_invalidar == COD_CONSUMIDOR_FINAL or tipo_dte_invalidar == COD_CREDITO_FISCAL or tipo_dte_invalidar == COD_FACTURA_EXPORTACION:
                json_documento_inv["montoIva"] = float(factura_invalidar.total_operaciones)
            else:
                json_documento_inv["montoIva"] = None
            
            #Si el tipo de invalidacion es codigo 1 o 3 llenar este campo con el codGeneracion del documento que reemplazara el dte a invalidar, no aplica para NC y Comp Liquidacion
            if int(evento_invalidacion.tipo_invalidacion.codigo) == COD_TIPO_INVALIDACION_RESCINDIR and tipo_dte_invalidar != COD_NOTA_CREDITO and tipo_dte_invalidar != COD_COMPROBANTE_LIQUIDACION:
                json_documento_inv["codigoGeneracionR"] = None
            else:
                json_documento_inv["codigoGeneracionR"] = None#.upper() #str(evento_invalidacion.codigo_generacion_r).upper() #campo en la vista
                print("codGeneracionR",json_documento_inv["codigoGeneracionR"])       
            #Asignar informacion de quien solicita la invalidacion, segun seleccion(receptor o emisor)
            if solicitud == EMI_SOLICITA_INVALIDAR_DTE:
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.factura.dteemisor.nombre_razon_social)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.factura.dteemisor.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.factura.dteemisor.nit)
            elif solicitud == REC_SOLICITA_INVALIDAR_DTE:
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.factura.dtereceptor.nombre)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.factura.dtereceptor.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.factura.dtereceptor.num_documento)
            
            json_completo = {
                "identificacion": json_identificacion_inv,
                "emisor": json_emisor_inv,
                "documento": json_documento_inv,
                "motivo": json_motivo_inv
            }
            
            json_invalidacion = json.dumps(json_completo)
            json_invalidacion_completo = json.loads(json_invalidacion)
            evento_invalidacion.json_invalidacion = json_invalidacion_completo
            evento_invalidacion.nombre_solicita = json_motivo_inv["nombreSolicita"]
            evento_invalidacion.tipo_documento_solicita = json_motivo_inv["tipDocSolicita"]
            evento_invalidacion.numero_documento_solicita = json_motivo_inv["numDocSolicita"]
            evento_invalidacion.save()
        else:
            return JsonResponse({
            "error": "Error DTE a invalidar no encontrado",
            "detalle": str(e)
        }) 
        return redirect (reverse('detalle_factura', args=[factura_id]))
    except Exception as e:
        codigo_generacion_invalidacion = str(uuid.uuid4()).upper()
        print(f"Error al generar el evento de invalidación: {e}")
        return JsonResponse({"error": str(e)}, status=400)
    
#VISTAS PARA FIRMAR Y GENERAR EL SELLO DE RECEPCION CON HACIENDA

@csrf_exempt
def firmar_factura_view(request, factura_id):
    """
    Firma la factura y, si ya está firmada, la envía a Hacienda.
    """
    print("-Inicio firma DTE")
    factura = get_object_or_404(FacturaElectronica, id=factura_id)

    token_data = Token_data.objects.filter(activado=True).first()
    if not token_data:
        return JsonResponse({"error": "No hay token activo registrado en la base de datos."}, status=401)

    if not os.path.exists(CERT_PATH):
        return JsonResponse({"error": "No se encontró el certificado en la ruta especificada."}, status=400)
    
    # Verificar y formatear el JSON original de la factura
    try:
        if isinstance(factura.json_original, dict):
            dte_json_str = json.dumps(factura.json_original, separators=(',', ':'))
        else:
            json_obj = json.loads(factura.json_original)
            dte_json_str = json.dumps(json_obj, separators=(',', ':'))
    except Exception as e:
        return JsonResponse({
            "error": "El JSON original de la factura no es válido",
            "detalle": str(e)
        }, status=400)

    # Construir el payload con los parámetros requeridos
    payload = {
        "nit": "06142811001040",   # Nit del contribuyente
        "activo": True,            # Indicador activo
        "passwordPri": "3nCr!pT@d0Pr1v@d@",   # Contraseña de la llave privada
        "dteJson": factura.json_original    # JSON del DTE como cadena
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(FIRMADOR_URL, json=payload, headers=headers)
        
        # Capturamos la respuesta completa
        try:
            response_data = response.json()
        except Exception as e:
            # En caso de error al parsear el JSON, se guarda el texto crudo
            response_data = {"error": "No se pudo parsear JSON", "detalle": response.text}
        
        # Guardar toda la respuesta en la factura para depuración (incluso si hubo error)
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

            return redirect(reverse('detalle_factura', args=[factura_id]))
        else:
            # Se devuelve el error completo recibido
            return JsonResponse({"error": "Error al firmar la factura", "detalle": response_data}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Error de conexión con el firmador", "detalle": str(e)}, status=500)

from django.views.decorators.http import require_POST
@csrf_exempt
@require_POST
def enviar_factura_hacienda_view(request, factura_id):
    # Paso 1: Autenticación contra el servicio de Hacienda
    nit_empresa = "06142811001040"
    pwd = "Q#3P9l5&@aF!gT2sA"
    auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
    auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MiAplicacionDjango/1.0"
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}

    try:
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
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Error de conexión con el servicio de autenticación",
            "detalle": str(e)
        }, status=500)

    # Paso 2: Enviar la factura firmada a Hacienda
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    # if not factura.firmado:
    #     return JsonResponse({"error": "La factura no está firmada"}, status=400)

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
        "ambiente": "01",  # "00" para Pruebas; "01" para Producción
        "idEnvio": factura.id,
        "version": int(factura.json_original["identificacion"]["version"]),
        "tipoDte": str(factura.json_original["identificacion"]["tipoDte"]),
        "documento": documento_token,  # Enviamos solo el JWT firmado
        "codigoGeneracion": codigo_generacion_str
    }

    envio_headers = {
        "Authorization": f"Bearer {token_data_obj.token}",
        "User-Agent": "DjangoApp",
        "Content-Type": "application/json"
    }

    try:
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
            factura.save()
            return JsonResponse({
                "mensaje": "Factura enviada con éxito",
                "respuesta": response_data
            })
        else:
            factura.estado=False
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
        }, status=500)


    if request.method != 'POST':
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
        return JsonResponse({"error": str(e)}, status=400)

#########################################################################################################
# EVENTO DE INVALIDACION DE DTE
#########################################################################################################

@csrf_exempt    
def invalidacion_dte_view(request, factura_id):
    # Generar json, firmar, enviar a MH
    codigo_generacion_invalidacion = str(uuid.uuid4()).upper()
    print("-Codigo generacion evento invalidacion ", codigo_generacion_invalidacion)
    factura_invalidar = FacturaElectronica.objects.get(id=factura_id)  # Buscar DTE a invalidar

    # Tipo Invalidacion (se asume código "2" como ejemplo)
    tipo_invalidacion = TipoInvalidacion.objects.get(codigo="2")
    # Quién solicita invalidar el DTE: emisor o receptor (este valor es dinámico)
    solicitud = "receptor"
    
    try: 
        if factura_invalidar is not None:
            print("-Factura a invalidar encontrada", factura_invalidar)
            # Buscar si la factura ya tiene un evento de invalidación
            evento_invalidacion = EventoInvalidacion.objects.filter(
                factura__codigo_generacion=factura_invalidar.codigo_generacion
            ).first()
            
            # Si no existe, se crea el registro; de lo contrario, se actualiza
            if evento_invalidacion is None:
                evento_invalidacion = EventoInvalidacion.objects.create(
                    codigo_generacion=codigo_generacion_invalidacion,
                    factura=factura_invalidar,
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
            
            # Armar el JSON de identificación
            json_identificacion_inv = {
                "version": int(VERSION_EVENTO_INVALIDACION),  # Version vigente, por ejemplo 2
                "ambiente": "01",  # O el valor que corresponda
                "codigoGeneracion": str(evento_invalidacion.codigo_generacion).upper(),
                "fecAnula": str(evento_invalidacion.fecha_anulacion),
                "horAnula": str(evento_invalidacion.hora_anulacion.strftime('%H:%M:%S'))
            }
            
            # Armar JSON para "emisor"
            tipo_establecimiento = TiposEstablecimientos.objects.get(
                codigo=evento_invalidacion.factura.dteemisor.tipoestablecimiento.codigo
            )
            json_emisor_inv = {
                "nit": str(evento_invalidacion.factura.dteemisor.nit),
                "nombre": str(evento_invalidacion.factura.dteemisor.nombre_razon_social),
                "tipoEstablecimiento": str(tipo_establecimiento.codigo),
                "nomEstablecimiento": str(tipo_establecimiento.descripcion),
                "codEstableMH": str(evento_invalidacion.factura.dteemisor.codigo_establecimiento or "M001"),
                "codEstable": "0001",
                "codPuntoVentaMH": str(evento_invalidacion.factura.dteemisor.codigo_punto_venta or "P001"),
                "codPuntoVenta": "0001",
                "telefono": str(evento_invalidacion.factura.dteemisor.telefono),
                "correo": str(evento_invalidacion.factura.dteemisor.email)
            }
            
            # Armar JSON para "documento"
            json_documento_inv = {
                "tipoDte": str(evento_invalidacion.factura.tipo_dte.codigo),
                "codigoGeneracion": str(factura_invalidar.codigo_generacion).upper(),
                "selloRecibido": str(factura_invalidar.sello_recepcion),
                "numeroControl": str(factura_invalidar.numero_control),
                "fecEmi": str(factura_invalidar.fecha_emision),
                "tipoDocumento": str(evento_invalidacion.factura.dtereceptor.tipo_documento.codigo),
                "numDocumento": str(evento_invalidacion.factura.dtereceptor.num_documento),
                "nombre": str(evento_invalidacion.factura.dtereceptor.nombre),
                "telefono": str(evento_invalidacion.factura.dtereceptor.telefono),
                "correo": str(evento_invalidacion.factura.dtereceptor.correo) 
            }
            
            # Armar JSON para "motivo"
            json_motivo_inv = {
                "tipoAnulacion": int(evento_invalidacion.tipo_invalidacion.codigo),
                "motivoAnulacion": str(evento_invalidacion.motivo_anulacion),
                "nombreResponsable": str(evento_invalidacion.factura.dteemisor.nombre_razon_social),
                "tipDocResponsable": str(evento_invalidacion.factura.dteemisor.tipo_documento.codigo),
                "numDocResponsable": str(evento_invalidacion.factura.dteemisor.nit),
            }
            
            # Ajustes según el DTE a invalidar
            tipo_dte_invalidar = evento_invalidacion.factura.tipo_dte.codigo
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
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.factura.dteemisor.nombre_razon_social)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.factura.dteemisor.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.factura.dteemisor.nit)
            elif solicitud == REC_SOLICITA_INVALIDAR_DTE:
                json_motivo_inv["nombreSolicita"] = str(evento_invalidacion.factura.dtereceptor.nombre)
                json_motivo_inv["tipDocSolicita"] = str(evento_invalidacion.factura.dtereceptor.tipo_documento.codigo)
                json_motivo_inv["numDocSolicita"] = str(evento_invalidacion.factura.dtereceptor.num_documento)
            
            # Armado del JSON completo
            json_completo = {
                "identificacion": json_identificacion_inv,
                "emisor": json_emisor_inv,
                "documento": json_documento_inv,
                "motivo": json_motivo_inv
            }
            
            # Se convierte a JSON (opcional) y se almacena en el campo correspondiente
            evento_invalidacion.json_invalidacion = json_completo
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
def firmar_factura_anulacion_view(request, factura_id): 
    """
    Firma la factura y, si ya está firmada, la envía a Hacienda.
    """
    print("-Inicio firma invalidacion DTE - id factura ", factura_id)
    #Buscar factura a firmar
    evento_invalidacion = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
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
    # Construir el payload con los parámetros requeridos
    payload = {
        "nit": "06142811001040",   # Nit del contribuyente
        "activo": True,            # Indicador activo
        "passwordPri": "3nCr!pT@d0Pr1v@d@",   # Contraseña de la llave privada
        "dteJson": evento_invalidacion.json_invalidacion    # JSON del DTE como cadena
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(FIRMADOR_URL, json=payload, headers=headers)
        
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
            json_signed_path = f"FE/json_facturas_firmadas/{evento_invalidacion.codigo_generacion}.json"
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
#@require_POST
def enviar_factura_invalidacion_hacienda_view(request, factura_id):
    print("-Inicio enviar invalidacion a MH")
    # Paso 1: Autenticación contra el servicio de Hacienda
    nit_empresa = "06142811001040"
    pwd = "Q#3P9l5&@aF!gT2sA"
    auth_url = "https://api.dtes.mh.gob.sv/seguridad/auth"
    auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MiAplicacionDjango/1.0"
    }
    auth_data = {"user": nit_empresa, "pwd": pwd}

    try:
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
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Error de conexión con el servicio de autenticación",
            "detalle": str(e)
        }, status=500)

    # Paso 2: Enviar la factura firmada a Hacienda
    #factura = get_object_or_404(FacturaElectronica, id=factura_id)
    evento_invalidacion = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
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
        "User-Agent": "DjangoApp",
        "Content-Type": "application/json"
    }
        
    try:
        envio_response = requests.post(
            "https://api.dtes.mh.gob.sv/fesv/anulardte",
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

def detalle_factura(request, factura_id):
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    return render(request, "documentos/factura_consumidor/template_factura.html", {"factura": factura})

######################################################################################

def seleccion_descuento_ajax(request):
    descuento_porcentaje = request.GET.get("descuento_id")
    print("-Descuento url: ", descuento_porcentaje)
    return JsonResponse({'descuento': descuento_porcentaje})

def agregar_formas_pago_ajax(request):
    print("-Formas de pago url: ", request)
    global formas_pago
    
    formas_pago = []
    try:
        forma_pago_id = request.GET.get("fp_id")
        num_referencia = request.GET.get("num_ref", None)
        if num_referencia == "":
            num_referencia = None
        monto_fp = request.GET.get("monto_fp")
        periodo_plazo = request.GET.get("periodo", None)
        condicion_operacion = request.GET.get("condicion_op", None)

        saldo_favor = request.GET.get("saldo_favor_r", None)
        print("-Convertir saldo a favor a decimal", saldo_favor)
        tiene_saldoF = False
        
        monto = Decimal("0.00")
        try:
            if saldo_favor is not None and saldo_favor !="":
                print("Convertir saldo a favor: ", saldo_favor)
                saldo = Decimal(saldo_favor)
                if  saldo.compare(Decimal("0.00")) > 0:
                    tiene_saldoF = True
                    codFormaPago = FormasPago.objects.get(codigo="99")
            else:
                saldo_favor = Decimal("0.00")
            print("-Saldo a favor formas de pago: ", saldo_favor)
        except ConversionSyntax:
            print(f"Error: '{saldo}' no es un valor decimal válido.")
        
        if forma_pago_id:
            formaPago = FormasPago.objects.get(id=forma_pago_id)
            if formaPago is not None:
                formas_pago_json  = {
                    "codigo": str(formaPago.codigo),
                    "montoPago": float(monto_fp),
                    "referencia": str(num_referencia),
                    "plazo": None
                }
        
        if tiene_saldoF:
            formas_pago_json["codigo"] = str(codFormaPago.codigo)
        if int(condicion_operacion) > 0 and int(condicion_operacion) == int(ID_CONDICION_OPERACION):
            print("-Condicion operacion 2")
            formas_pago_json["codigo"] = None
            formas_pago_json["montoPago"] = float(monto)
            formas_pago_json["plazo"] = str(Plazo.objects.get(id=1).codigo) #Plazo por días
            formas_pago_json["periodo"] = int(periodo_plazo)
        else:
            print("-Condicion operacion !=2")
            formas_pago_json["periodo"] = None
            
        if formas_pago_json["codigo"] == "01": #Forma d pago billetes y monedas
            formas_pago_json["referencia"] = None
        
        formas_pago.append(formas_pago_json)
        print("-Formas de pago seleccionadas: ", formas_pago)
        
        return JsonResponse({'formasPago': formas_pago})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    