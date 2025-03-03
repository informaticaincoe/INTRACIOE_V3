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
#from weasyprint import CSS, HTML
from decimal import ROUND_HALF_UP, Decimal
from intracoe import settings
from .models import Ambiente, CondicionOperacion, DetalleFactura, FacturaElectronica, Modelofacturacion, NumeroControl, Emisor_fe, ActividadEconomica, Producto, Receptor_fe, Tipo_dte, TipoMoneda, TipoUnidadMedida, TiposDocIDReceptor, Municipio
from FE.models import Token_data
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

#importaciones para actividad economica
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

FIRMADOR_URL = "http://192.168.2.25:8113/firmardocumento/"
DJANGO_SERVER_URL = "http://127.0.0.1:8000"

SCHEMA_PATH_fe_fc_v1 = "FE/json_schemas/fe-fc-v1.json"

CERT_PATH = "FE/cert/06142811001040.crt"  # Ruta al certificado

# URLS de Hacienda (Pruebas y Producción)
HACIENDA_URL_TEST = "https://apitest.dtes.mh.gob.sv/fesv/recepciondte"
HACIENDA_URL_PROD = "https://api.dtes.mh.gob.sv/fesv/recepciondte"

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

#VISTA PARA NUMERO DE CONTROL
def incrementar_numero_control():
    # Obtiene el último número de control usado y añade uno
    ultimo_numero = (
        FacturaElectronica.objects.latest('id').numero_control
        if FacturaElectronica.objects.exists()
        else "DTE-01-M001P001-000000000000000"
    )
    match = re.search(r"(\d+)$", ultimo_numero)
    if match:
        numero_actual = int(match.group(1))
        nuevo_numero = numero_actual + 1
        return f"DTE-01-M001P001-{nuevo_numero:015d}"
    return None

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
    

from decimal import Decimal, ROUND_HALF_UP
@csrf_exempt
@transaction.atomic
def generar_factura_view(request):
    if request.method == 'GET':
        # ... (la parte GET permanece igual)
        emisor_obj = Emisor_fe.objects.first()
        if emisor_obj:
            nuevo_numero = NumeroControl.obtener_numero_control()
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

        context = {
            "numero_control": nuevo_numero,
            "codigo_generacion": codigo_generacion,
            "fecha_generacion": fecha_generacion,
            "hora_generacion": hora_generacion,
            "emisor": emisor_data,
            "receptores": receptores,
            "productos": productos,
            "tipooperaciones": tipooperaciones
        }
        return render(request, "generar_dte.html", context)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
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
            
            if not numero_control:
                numero_control = NumeroControl.obtener_numero_control()
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
            tipo_dte_obj = Tipo_dte.objects.get(codigo="01")
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
                precio_neto = (precio_incl / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                iva_unitario = (precio_incl - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                # Totales por ítem
                total_neto = (precio_neto * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_iva_item = (iva_unitario * cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
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
            factura.save()

            # Construir el cuerpoDocumento para el JSON con desglose
            cuerpo_documento = []
            for idx, det in enumerate(factura.detalles.all(), start=1):
                # Recalcular (para el JSON) usando los valores ya calculados:
                precio_neto = (Decimal(det.precio_unitario) / Decimal("1.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                iva_unitario = (Decimal(det.precio_unitario) - precio_neto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_neto = (precio_neto * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_iva_item = (iva_unitario * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                total_con_iva = (Decimal(det.precio_unitario) * det.cantidad).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                print(f"Item {idx}: IVA unitario = {iva_unitario}, Total IVA = {total_iva_item}, IVA almacenado = {det.iva_item}")

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
                    "tributos":["20"], #iva para todos los items
                    "psv": 0.0,
                    "noGravado": float(det.no_gravado),
                    "ivaItem": float(total_iva_item)        # IVA total por línea
                })

            factura_json = {
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
                    "tipoDocumento": str(receptor.tipo_documento.codigo) if receptor.tipo_documento else "",
                    "numDocumento": str(receptor.num_documento),
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
                    "correo": receptor.correo or ""
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
            }

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
