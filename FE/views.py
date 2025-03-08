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
from decimal import ROUND_HALF_UP, Decimal
from intracoe import settings
from .models import Ambiente, CondicionOperacion, DetalleFactura, FacturaElectronica, Modelofacturacion, NumeroControl, Emisor_fe, ActividadEconomica,  Receptor_fe, Tipo_dte, TipoMoneda, TipoUnidadMedida, TiposDocIDReceptor, Municipio, EventoInvalidacion, TipoInvalidacion, TiposEstablecimientos
from INVENTARIO.models import Producto
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
COD_FACTURA_EXPORTACION = "11"
COD_TIPO_INVALIDACION_RESCINDIR = 2
COD_NOTA_CREDITO = "05"
COD_COMPROBANTE_LIQUIDACION = "08"
EMI_SOLICITA_INVALIDAR_DTE = "emisor"
REC_SOLICITA_INVALIDAR_DTE = "receptor"

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

# Función auxiliar para convertir números a letras (stub, cámbiala según tus necesidades)
from num2words import num2words

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
    #print(f"Inicializando DTE Vista: {iniciar_dte}")
    nuevo_numero = NumeroControl.preview_numero_control(tipo_dte)
    return JsonResponse({'numero_control': nuevo_numero})

from decimal import Decimal, ROUND_HALF_UP
@csrf_exempt
@transaction.atomic
def generar_factura_view(request):
    print("Inicio generar dte")
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
        

        context = {
            "numero_control": nuevo_numero,
            "codigo_generacion": codigo_generacion,
            "fecha_generacion": fecha_generacion,
            "hora_generacion": hora_generacion,
            "emisor": emisor_data,
            "receptores": receptores,
            "productos": productos,
            "tipooperaciones": tipooperaciones,
            "tipoDocumentos": tipoDocumentos
        }
        return render(request, "generar_dte.html", context)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
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
            print(f"DTE seleccionado desde el form: {tipo_dte}")

            # Configuración adicional
            tipooperacion_id = data.get("condicion_operacion", None)
            porcentaje_retencion_iva = Decimal(data.get("porcentaje_retencion_iva", "0"))
            retencion_iva = data.get("retencion_iva", False)
            productos_retencion_iva = data.get("productos_retencion_iva", [])
            porcentaje_retencion_renta = Decimal(data.get("porcentaje_retencion_renta", "0"))
            retencion_renta = data.get("retencion_renta", False)
            productos_retencion_renta = data.get("productos_retencion_renta", [])

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
            #tipo_dte_obj = Tipo_dte.objects.get("tipo_documento")
            tipo_dte_obj = Tipo_dte.objects.get(codigo=tipo_dte)
            print(f"Tipo de documento a generar = {tipo_dte_obj}")

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
            )

            # Inicializar acumuladores globales
            total_gravada = Decimal("0.00")  # Suma de totales netos
            total_iva = Decimal("0.00")       # Suma de totales IVA
            total_pagar = Decimal("0.00")     # Suma de totales con IVA
            DecimalRetIva = Decimal("0.00")
            DecimalRetRenta = Decimal("0.00")
            DecimalIvaPerci = Decimal("0.00")
            total_operaciones = Decimal("0.00")

            # Obtener unidad de medida
            unidad_medida_obj = TipoUnidadMedida.objects.get(codigo="59")

            # Recorrer productos para crear detalles (realizando el desglose)
            for index, prod_id in enumerate(productos_ids):
                try:
                    producto = Producto.objects.get(id=prod_id)
                except Producto.DoesNotExist:
                    continue

                cantidad = int(cantidades[index]) if index < len(cantidades) else 1
                # El precio del producto ya incluye IVA (por ejemplo, 8.50)
                precio_incl = producto.preunitario

                # Calcular precio neto y IVA unitario
                #precio_neto = (precio_incl / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                precio_neto = (precio_incl ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL :
                    total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                else:  #Cuando no es FE quitarle iva al precio
                    #precio_neto = (precio_incl / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    #BC: verificar si el precio del prod para ccf ya viene con iva
                    total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print(f"Precio Incl = {precio_incl}, Precio neto = {precio_neto}, tipo dte:  {tipo_dte}")
                
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                # Totales por ítem
                total_neto = (precio_neto * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #total_iva_item = (iva_unitario * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #funcional total_iva_item = ( ( precio_incl * cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                print(f"IVA Item = {total_iva_item}, iva unitario = {iva_unitario}, cantidad = {cantidad} ")
                
                total_con_iva = (precio_incl * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                descuento_monto = Decimal("0.00")  # Se asume 0 descuento por ítem

                detalle = DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    unidad_medida=unidad_medida_obj,
                    precio_unitario=precio_incl,  # Se almacena el precio bruto (con IVA)
                    descuento=descuento_monto,
                    ventas_no_sujetas=Decimal("0.00"),
                    ventas_exentas=Decimal("0.00"),
                    ventas_gravadas=total_neto,  # Total neto
                    pre_sug_venta=precio_incl,
                    no_gravado=Decimal("0.00"),
                )
                # Actualizamos manualmente los campos calculados
                detalle.total_sin_descuento = total_neto
                detalle.iva = total_iva_item
                detalle.total_con_iva = total_con_iva
                detalle.iva_item = total_iva_item  # Guardamos el total IVA para este detalle
                detalle.save()

                total_gravada += total_neto
                total_iva += total_iva_item
                total_pagar += total_con_iva
                total_operaciones = total_gravada

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

            # Actualizar totales en la factura
            factura.total_no_sujetas = Decimal("0.00")
            factura.total_exentas = Decimal("0.00")
            factura.total_gravadas = total_gravada
            factura.sub_total_ventas = total_gravada
            factura.descuen_no_sujeto = Decimal("0.00")
            factura.descuento_exento = Decimal("0.00")
            factura.descuento_gravado = Decimal("0.00")
            factura.por_descuento = Decimal("0.00")
            factura.total_descuento = Decimal("0.00")
            factura.sub_total = total_gravada
            factura.iva_retenido = DecimalRetIva
            factura.retencion_renta = DecimalRetRenta
            factura.total_operaciones = total_gravada
            factura.total_no_gravado = Decimal("0.00")
            factura.total_pagar = total_pagar
            factura.total_letras = num_to_letras(total_pagar)
            factura.total_iva = total_iva
            factura.condicion_operacion = tipooperacion_obj
            factura.iva_percibido = DecimalIvaPerci
            factura.save()

            # Construir el cuerpoDocumento para el JSON con desglose
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                # Recalcular (para el JSON) usando los valores ya calculados:
                #precio_neto = (Decimal(det.precio_unitario) / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE DEBE INCLUIRSE EL IVA EN EL PRECIO
                precio_neto = (Decimal(det.precio_unitario) ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #iva_unitario = (Decimal(det.precio_unitario) - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE DEBE INCLUIRSE EL IVA EN EL PRECIO
                iva_unitario = (Decimal(det.precio_unitario)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_neto = (precio_neto * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                #total_iva_item = (iva_unitario * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #BC: TEMPORALMENTE COMETAREADO YA QUE PARA FE EL CALCULO ES DIFERENTE
                total_iva_item = ( ( iva_unitario * det.cantidad) / Decimal("1.13") * Decimal("0.13") ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print(f"-Total IVA = {total_iva_item}")
                
                total_con_iva = (Decimal(det.precio_unitario) * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                print(f"Item {idx}: IVA unitario = {iva_unitario}, Total IVA = {total_iva_item}, IVA almacenado = {det.iva_item}")
                
                #BC 03/03/25:para el caso de FE el campo tributos enviarlo null
                tipo_dte_item = str(det.factura.tipo_dte.codigo)
                if tipo_dte_item == COD_CONSUMIDOR_FINAL:
                    tributos = None  
                else :
                    tributos = ["20"]
                    #tributos = "20"
                    
                cuerpo_documento.append({
                    "numItem": idx,
                    "tipoItem": 1,
                    "numeroDocumento": None,
                    "codigo": str(det.producto.codigo),
                    "codTributo": None,
                    "descripcion": str(det.producto.descripcion),
                    "cantidad": float(det.cantidad),
                    "uniMedida": int(det.unidad_medida.codigo) if det.unidad_medida.codigo.isdigit() else 59,
                    "precioUni": float(precio_neto),      # Precio unitario neto
                    #"ivaUnitario": float(iva_unitario),     # IVA unitario
                    #"totalNeto": float(total_neto),         # Total neto por ítem
                    #"totalIva": float(total_iva_item),       # Total IVA por ítem
                    #"totalConIva": float(total_con_iva),     # Total con IVA por ítem
                    "montoDescu": float(det.descuento),
                    "ventaNoSuj": float(det.ventas_no_sujetas),
                    "ventaExenta": float(det.ventas_exentas),
                    "ventaGravada": float(det.ventas_gravadas),
                    "tributos": tributos, #iva para todos los items 
                    "psv": 0.0,
                    "noGravado": float(det.no_gravado),
                    #"ivaItem": float(total_iva_item)        # IVA total por línea
                })
                
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
            
            factura_json = generar_json(ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento, observaciones, Decimal(str(total_iva_item)))
            print(f"JSON:  = {factura_json} ")
            
            factura.json_original = factura_json
            factura.save()

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
def generar_json(ambiente_obj, tipo_dte_obj, factura, emisor, receptor, cuerpo_documento, observaciones, iva_item_total):
    print("-Inicio llenar json")

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
        #"montoTotalOperacion": float(factura.total_operaciones),
        "totalNoGravado": float(factura.total_no_gravado),
        #"totalPagar": float(factura.total_pagar),
        "totalLetras": factura.total_letras,
        #"totalIva": float(factura.total_iva),
        "saldoFavor": 0.0,
        "condicionOperacion": int(factura.condicion_operacion.codigo) if factura.condicion_operacion and factura.condicion_operacion.codigo.isdigit() else 1,
        "pagos": None,
        #"tributos": None,
        "numPagoElectronico": None
    }
    
    json_extension = {
        "nombEntrega": None,
        "docuEntrega": None,
        "nombRecibe": None,
        "docuRecibe": None,
        "observaciones": observaciones,
        "placaVehiculo": None
    }
    
    json_apendice = None
    
    print("-Inicio modificacion de json")
    #Modificacion de json en base al tipo dte a generar
    if receptor is not None:
        nrc_receptor = None
        print("-Nrc: ", receptor.nrc)
        if receptor.nrc is not None and receptor.nrc !="None":
            nrc_receptor = str(receptor.nrc)
        json_receptor["nrc"] = nrc_receptor
        
    json_resumen["tributos"] = [
            {
               "codigo": "20",
               "descripcion": "Impuesto al valor agregado 13%",
               "valor": float(factura.total_iva)
            }
        ]
        
    if tipo_dte_obj.codigo == COD_CONSUMIDOR_FINAL:
        json_receptor["tipoDocumento"] = str(receptor.tipo_documento.codigo) if receptor.tipo_documento else ""
        json_receptor["numDocumento"] = str(receptor.num_documento) 
        
        #iva_item_total obtener solo el monto
        valor_iva_item = iva_item_total
        
        #Recorrer items y modificar campo ivaItem cuando son FE
        for i, cuerpo in enumerate(cuerpo_documento):
            #Remover el item
            cuerpo_documento.pop(i)
            #Modificar campo
            cuerpo["ivaItem"] = float(valor_iva_item)
            #Agregar nuevamente el item
            cuerpo_documento.insert(i, cuerpo)
                   
        json_resumen["totalIva"] = float(factura.total_iva)
        json_resumen["montoTotalOperacion"] = float(factura.total_operaciones)
        json_resumen["totalPagar"] = float(factura.total_pagar)
        json_resumen["tributos"] = None
    elif tipo_dte_obj.codigo == COD_CREDITO_FISCAL:
        json_receptor["nit"] = str(receptor.num_documento)
        json_receptor["nombreComercial"] = str(receptor.nombreComercial)
        json_resumen["ivaPerci1"] = float(factura.iva_percibido)
        
        print("-Asignar tributos")
        #Asignar tributos
        tributo = json_resumen["tributos"]
        tributo_valor = tributo[0]
        subtotal = float(factura.sub_total)
        valor_tributos = float(tributo_valor["valor"])
        total_operaciones = subtotal + valor_tributos
        json_resumen["montoTotalOperacion"] = float(total_operaciones)
        total_pagar = json_resumen["montoTotalOperacion"] - json_resumen["ivaPerci1"] - json_resumen["ivaRete1"] - json_resumen["reteRenta"] - json_resumen["totalNoGravado"]
        json_resumen["totalPagar"] = total_pagar
            
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

@csrf_exempt    
def invalidacion_dte_view(request, factura_id):
    print("-Inicio invalidar dte- request ", request)
    print("-factura id ", factura_id)
    
    codigo_generacion_invalidacion = str(uuid.uuid4()).upper()
    
    #Buscar dte a invalidar
    invalidar_codigo_generacion = "39f71e48-c22b-4833-89e1-8256e16d9401"
    
    factura_invalidar = FacturaElectronica.objects.get(codigo_generacion=invalidar_codigo_generacion)
    
    #Tipo Invalidacion
    tipo_invalidacion = TipoInvalidacion.objects.get(codigo="1") #Campo dinamico
    
    #Quien solicita invalidar el dte, el emisor o receptor
    solicitud = "receptor" #Campo dinamico

    #Llenar registro en tabla
    invalidacion = EventoInvalidacion.objects.create(
        codigo_generacion = codigo_generacion_invalidacion,
        factura = factura_invalidar,
        codigo_generacion_r = invalidar_codigo_generacion,
        tipo_anulacion = tipo_invalidacion,
        motivo_anulacion = tipo_invalidacion.descripcion, #Campo dinamico
        nombre_solicita = factura_invalidar.dteemisor.nombre_razon_social,
        tipo_documento_solicita = int(factura_invalidar.dteemisor.tipo_documento.codigo),
        numero_documento_solicita = factura_invalidar.dteemisor.nit,
        solicita_invalidacion = solicitud
    )
    
    if factura_invalidar is not None:
        
        json_identificacion_inv = {
            "version": int(VERSION_EVENTO_INVALIDACION), #Version vigente 2
            "ambiente": str(Ambiente.codigo),
            "codigoGeneracion": str(invalidacion.codigo_generacion),
            "FecAnual": str(invalidacion.fecha_anulacion),
            "horAnula": str(invalidacion.hora_anulacion.strftime('%H:%M:%S'))
            
        }
        
        tipo_establecimiento = TiposEstablecimientos.objects.get(codigo=invalidacion.factura.dteemisor.tipoestablecimiento.codigo)
        json_emisor_inv = {
            "nit": str(invalidacion.factura.dteemisor.nit),
            "nombre": str(invalidacion.factura.dteemisor.nombre_razon_social),
            "tipoEstablecimiento": str(tipo_establecimiento.codigo),
            "nomEstablecimiento": str(tipo_establecimiento.descripcion),
            "codEstableMH": str(invalidacion.factura.dteemisor.codigo_establecimiento or "M001"),
            "codEstable": "0001",
            "codPuntoVentaMH": str(invalidacion.factura.dteemisor.codigo_punto_venta or "P001"),
            "codPuntoVenta": "0001",
            "telefono": str(invalidacion.factura.dteemisor.telefono),
            "correo": str(invalidacion.factura.dteemisor.email)
        }
        
        #seccion documento
        json_documento_inv = {
            "tipoDte" : str(invalidacion.factura.tipo_dte.codigo),
            "codigoGeneracion" : str(factura_invalidar.codigo_generacion),
            "selloRecibido" : str(factura_invalidar.sello_recepcion),
            "numeroControl" : str(factura_invalidar.numero_control),
            "fechaEmi" : str(factura_invalidar.fecha_emision),
            "tipoDocumento" : int(invalidacion.factura.dtereceptor.tipo_documento.codigo),
            "numDocumento" : str(invalidacion.factura.dtereceptor.num_documento),
            "nombre" : str(invalidacion.factura.dtereceptor.nombre),
            "telefono" : str(invalidacion.factura.dtereceptor.telefono),
            "correo" : str(invalidacion.factura.dtereceptor.correo) 
        }
        
        json_motivo_inv = {
            "tipoAnulacion" : int(invalidacion.tipo_anulacion.codigo),
            "motivoAnulacion" : str(invalidacion.motivo_anulacion),
            "nombreResponsable" : str(invalidacion.factura.dteemisor.nombre_razon_social),
            "tipoDocResponsable" : int(invalidacion.factura.dteemisor.tipo_documento.codigo),
            "numDocResponsable" : str(invalidacion.factura.dteemisor.nit),
        }
        
        #Modificaciones en json segun el dte a invalidar
        
        #Si el DTE a invalidar es F, CCF o FEX agregar campo "montoIva"
        tipo_dte_invalidar = invalidacion.factura.tipo_dte.codigo
        if tipo_dte_invalidar == COD_CONSUMIDOR_FINAL or tipo_dte_invalidar == COD_CREDITO_FISCAL or tipo_dte_invalidar == COD_FACTURA_EXPORTACION:
            json_documento_inv["montoIva"] = float(factura_invalidar.total_operaciones)
        else:
             json_documento_inv["montoIva"] = None
        
        #Si el tipo de invalidacion es codigo 1 o 3 llenar este campo con el codGeneracion del documento que reemplazara el dte a invalidar, no aplica para NC y Comp Liquidacion
        if tipo_dte_invalidar != COD_NOTA_CREDITO and tipo_dte_invalidar != COD_COMPROBANTE_LIQUIDACION:
            if int(invalidacion.tipo_anulacion.codigo) == COD_TIPO_INVALIDACION_RESCINDIR:
                json_documento_inv["codigoGeneracionR"] = None
            else:
                json_documento_inv["codigoGeneracionR"] = str(invalidacion.codigo_generacion_r),
            
        if solicitud == EMI_SOLICITA_INVALIDAR_DTE:
            json_motivo_inv["nombreSolicita"] = str(invalidacion.factura.dteemisor.nombre_razon_social),
            json_motivo_inv["tipDocSolicita"] = int(invalidacion.factura.dteemisor.tipo_documento.codigo),
            json_motivo_inv["numDocSolicita"] = str(invalidacion.factura.dteemisor.nit)
        elif solicitud == REC_SOLICITA_INVALIDAR_DTE:
            json_motivo_inv["nombreSolicita"] = str(invalidacion.factura.dtereceptor.nombre),
            json_motivo_inv["tipDocSolicita"] = int(invalidacion.factura.dtereceptor.tipo_documento.codigo),
            json_motivo_inv["numDocSolicita"] = str(invalidacion.factura.dtereceptor.num_documento)
            
        json_completo = {
            "identificacion": json_identificacion_inv,
            "emisor": json_emisor_inv,
            "documento": json_documento_inv,
            "motivo": json_motivo_inv
        }
        
        json_invalidacion = json.dumps(json_completo)
        json_original = json.loads(json_invalidacion)
        invalidacion.json_invalidacion = json_original
        invalidacion.save()
    #firmar 
    print("-Url firma ", request)
    firmar_factura_anulacion_view(request, factura_id)
    
@csrf_exempt
def firmar_factura_anulacion_view(request, factura_id): #id=160 cod_generacion=39f71e48-c22b-4833-89e1-8256e16d9401
    """
    Firma la factura y, si ya está firmada, la envía a Hacienda.
    """
    print("-Inicio firma invalidacion DTE - id factura ", factura_id)
    evento_invalidacion = EventoInvalidacion.objects.filter(factura__id=factura_id).first()
    invalidacion = evento_invalidacion#get_object_or_404(EventoInvalidacion, factura__id = factura_id)

    token_data = Token_data.objects.filter(activado=True).first()
    if not token_data:
        return JsonResponse({"error": "No hay token activo registrado en la base de datos."}, status=401)

    if not os.path.exists(CERT_PATH):
        return JsonResponse({"error": "No se encontró el certificado en la ruta especificada."}, status=400)
    
    # Verificar y formatear el JSON original de la factura
    print("-inicio verificacion formato json invalidacion")
    try:
        print("-if inicio verificacion formato json ", invalidacion.json_invalidacion)
        if isinstance(invalidacion.json_invalidacion, dict):
            dte_json_str = json.dumps(invalidacion.json_invalidacion, separators=(',', ':'))
        else:
            json_obj = json.loads(invalidacion.json_invalidacion)
            dte_json_str = json.dumps(json_obj, separators=(',', ':'))
    except Exception as e:
        return JsonResponse({
            "error": "El JSON original de la factura no es válido",
            "detalle": str(e)
        }, status=400)
    print("-fin verificacion formato json INVALIDACION ")
    # Construir el payload con los parámetros requeridos
    payload = {
        "nit": "06142811001040",   # Nit del contribuyente
        "activo": True,            # Indicador activo
        "passwordPri": "3nCr!pT@d0Pr1v@d@",   # Contraseña de la llave privada
        "dteJson": invalidacion.json_invalidacion    # JSON del DTE como cadena
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(FIRMADOR_URL, json=payload, headers=headers)
        
        # Capturamos la respuesta completa
        try:
            response_data = response.json()
            print("-Capturar respuesta MH", response_data)
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
            json_signed_path = f"FE/json_facturas_firmadas/{invalidacion.codigo_generacion}.json"
            os.makedirs(os.path.dirname(json_signed_path), exist_ok=True)
            with open(json_signed_path, "w", encoding="utf-8") as json_file:
                json.dump(response_data, json_file, indent=4, ensure_ascii=False)
                print("-Respuesta 200 - cod generacion", invalidacion.codigo_generacion)
            print("-Fin firma invalidacion DTE")
            return redirect(reverse('detalle_factura', args=[factura_id]))
        else:
            # Se devuelve el error completo recibido
            print("-Fin firma invalidacion DTE")
            return JsonResponse({"error": "Error al firmar la factura", "detalle": response_data}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Error de conexión con el firmador", "detalle": str(e)}, status=500)


#############################################################################################################

def detalle_factura(request, factura_id):
    factura = get_object_or_404(FacturaElectronica, id=factura_id)
    return render(request, "documentos/factura_consumidor/template_factura.html", {"factura": factura})

######################################################################################

#VISTAS PARA FIRMAR Y GENERAR EL SELLO DE RECEPCION CON HACIENDA
# Asegúrate de que esta vista no tenga otros decoradores (por ejemplo, login_required)
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
            factura.save()
            return JsonResponse({
                "mensaje": "Factura enviada con éxito",
                "respuesta": response_data
            })
        else:
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


