# views.py
from io import BytesIO
import io
import os
import logging
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db import connections
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
#from weasyprint import HTML, CSS
from xhtml2pdf import pisa
from decimal import Decimal
import tempfile
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime
from django.template.loader import get_template

import csv
from django.views import View
from FE.models import FacturaElectronica
from INVENTARIO.models import Compra
from .models import (
    CuentaContable, AsientoContable, LineaAsiento,
    CuentaPorCobrar, PagoCobro,
    CuentaPorPagar, PagoPagar,
)
from FE.models import Receptor_fe
from INVENTARIO.models import Proveedor

logger = logging.getLogger(__name__)

###################################################################################################################

@login_required
def listar_quedans(request):
    proveedor_nombre = request.GET.get('proveedor_nombre', '').strip()  # Nombre del proveedor (opcional)
    fecha_quedan = request.GET.get('fecha_quedan', '').strip()  # Fecha de quedan en formato 'YYYY-MM-DD' (opcional)

    with connections['brilo_sqlserver'].cursor() as cursor:
        # Construir la consulta base con alias
        query = """
            SELECT q.mqdnId, q.mqdnNumero, q.prvId, q.mqdnFecha, q.mqdnFechaPago, q.mqdnComentarios, p.prvNombre
            FROM olCompras.dbo.maeQuedans AS q
            INNER JOIN olComun.dbo.Proveedores AS p ON q.prvId = p.prvId
        """
        
        # Filtrar según los criterios de búsqueda
        where_clauses = []
        params = []
        
        # Agregar filtros a la consulta si se proporcionan parámetros de búsqueda
        if proveedor_nombre:
            where_clauses.append("p.prvNombre LIKE %s")
            params.append(f"%{proveedor_nombre}%")
        
        if fecha_quedan:
            where_clauses.append("q.mqdnFecha = %s")
            params.append(fecha_quedan)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Ordenar por fecha
        query += " ORDER BY q.mqdnFecha DESC"

        # Ejecutar la consulta con filtros
        cursor.execute(query, params)
        quedans = cursor.fetchall()

        # Paginación de resultados
        paginator = Paginator(quedans, 20)  # 20 elementos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Preparar contexto con los resultados y los criterios de búsqueda
        context = {
            'page_obj': page_obj,
            'proveedor_nombre': proveedor_nombre,
            'fecha_quedan': fecha_quedan,
        }

    return render(request, 'quedans/listar_quedans.html', context)

@login_required
def generar_pdf_quedan(request, mqdn_id):
    with connections['brilo_sqlserver'].cursor() as cursor:
        # Consultar datos del quedan
        cursor.execute("SELECT mqdnNumero, mqdnFecha, mqdnFechaPago, mqdnComentarios, prvId FROM olCompras.dbo.maeQuedans WHERE mqdnId = %s", [mqdn_id])
        quedan = cursor.fetchone()
        
        # Consultar proveedor
        cursor.execute("SELECT prvNombre FROM olComun.dbo.Proveedores WHERE prvId = %s", [quedan[4]])
        proveedor = cursor.fetchone()

        # Consultar detalles del quedan, ahora incluye mcoPorcentRetIVA
        cursor.execute("""
            SELECT mcoTipoDoc, mcoNumDoc, mcoFecha, mcoSumasAfecto, mcoPorcentRetIVA, mcoPorcentPercep, mcoTotalAPagarManual, mcoPorcentIVA 
            FROM olCompras.dbo.maeCompras 
            WHERE mqdnId = %s
        """, [mqdn_id])
        detalles = cursor.fetchall()

        # Inicializar variables de acumulación
        total_pago = Decimal(0)
        iva_total = Decimal(0)
        percep_total = Decimal(0)
        retencion_total = Decimal(0)  # Variable para la retención total

        # Lista para almacenar los detalles procesados
        detalles_procesados = []

        # Iterar sobre los detalles para acumular los valores
        for detalle in detalles:
            # Validar que el valor no sea None antes de convertirlo a Decimal
            suma_afecto = Decimal(detalle[3]) if detalle[3] is not None else Decimal(0.00)
            por_iva = Decimal(detalle[7]) if detalle[7] is not None else Decimal(0.13)  # Valor por defecto 0.13 si el IVA es None
            por_percep = Decimal(detalle[5]) if detalle[5] is not None else Decimal(0.00)
            por_retencion = Decimal(detalle[4]) if detalle[4] is not None else Decimal(0.00)  # Retención

            # Calcular IVA, Percepción y Retención
            iva = suma_afecto * por_iva
            percep = suma_afecto * por_percep
            retencion = suma_afecto * por_retencion  # Calcular la retención

            # Acumular el total de cada factura (ahora incluyendo la retención)
            if por_percep > 0:
                total_pago += suma_afecto + iva + percep - retencion  # Restar la retención
            else:
                total_pago += suma_afecto + iva - retencion  # Restar la retención

            # Acumular IVA, Percepción y Retención (para mostrar en el template si es necesario)
            iva_total += iva
            percep_total += percep
            retencion_total += retencion  # Acumular la retención

            # Guardar el detalle procesado en la lista
            detalles_procesados.append({
                'tipo_doc': detalle[0],
                'num_doc': detalle[1],
                'fecha': detalle[2],
                'suma_afecto': suma_afecto,
                'iva': iva,
                'percep': percep,
                'retencion': retencion,  # Agregar la retención
                'total': suma_afecto + iva + percep - retencion if por_percep > 0 else suma_afecto + iva - retencion,  # Incluir retención
            })

    # Renderizar el template HTML a string
    html_content = render_to_string('quedans/quedan_template.html', {
        'quedan': quedan,
        'proveedor': proveedor,
        'detalles': detalles_procesados,
        'total_pago': total_pago,
        'iva_total': iva_total,
        'percep_total': percep_total,
        'retencion_total': retencion_total,  # Pasar el total de retención al template
    })

    # Generar el PDF usando xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quedan_{quedan[1]}.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response, page_orientation='landscape')

    # Verificar errores en la generación del PDF
    if pisa_status.err:
        return HttpResponse(f"Error al generar el PDF: {pisa_status.err}")
    
    return response

@login_required
def enviar_quedan(request, mqdn_id):
    with connections['brilo_sqlserver'].cursor() as cursor:
        # Consultar datos del quedan
        cursor.execute("SELECT mqdnNumero, mqdnFecha, mqdnFechaPago, mqdnComentarios, prvId FROM olCompras.dbo.maeQuedans WHERE mqdnId = %s", [mqdn_id])
        quedan = cursor.fetchone()
        
        # Consultar proveedor
        cursor.execute("SELECT prvNombre, prvEmailRepLegal FROM olComun.dbo.Proveedores WHERE prvId = %s", [quedan[4]])
        proveedor = cursor.fetchone()

        # Consultar detalles del quedan
        cursor.execute("""
            SELECT mcoTipoDoc, mcoNumDoc, mcoFecha, mcoSumasAfecto, mcoPorcentRetIVA, mcoPorcentPercep, mcoTotalAPagarManual, mcoPorcentIVA 
            FROM olCompras.dbo.maeCompras 
            WHERE mqdnId = %s
        """, [mqdn_id])
        detalles = cursor.fetchall()

        # Variables para el cálculo de totales
        total_pago = Decimal(0)
        iva_total = Decimal(0)
        percep_total = Decimal(0)
        retencion_total = Decimal(0)

        detalles_procesados = []
        for detalle in detalles:
            suma_afecto = Decimal(detalle[3]) if detalle[3] is not None else Decimal(0.00)
            por_iva = Decimal(detalle[7]) if detalle[7] is not None else Decimal(0.13)
            por_percep = Decimal(detalle[5]) if detalle[5] is not None else Decimal(0.00)
            por_retencion = Decimal(detalle[4]) if detalle[4] is not None else Decimal(0.00)

            iva = suma_afecto * por_iva
            percep = suma_afecto * por_percep
            retencion = suma_afecto * por_retencion

            total_factura = suma_afecto + iva + percep - retencion if por_percep > 0 else suma_afecto + iva - retencion
            total_pago += total_factura

            iva_total += iva
            percep_total += percep
            retencion_total += retencion

            detalles_procesados.append({
                'tipo_doc': detalle[0],
                'num_doc': detalle[1],
                'fecha': detalle[2],
                'suma_afecto': suma_afecto,
                'iva': iva,
                'percep': percep,
                'retencion': retencion,
                'total': total_factura,
            })

    # Renderizar el template HTML
    template = get_template('quedans/quedan_template.html')
    context = {
        'quedan': quedan,
        'proveedor': proveedor,
        'detalles': detalles_procesados,
        'total_pago': total_pago,
        'iva_total': iva_total,
        'percep_total': percep_total,
        'retencion_total': retencion_total,
    }
    html_content = template.render(context)

    # Generar el PDF con xhtml2pdf
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode('utf-8')), dest=pdf_buffer, page_orientation='landscape')
    
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    pdf_buffer.seek(0)
    pdf_content = pdf_buffer.getvalue()

    # Guardar el PDF en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdf_file.write(pdf_content)
        pdf_file_path = pdf_file.name

    # Crear y enviar el correo
    subject = f'Quedan No. {quedan[0]} - {proveedor[0]}'
    message = (
        f'Estimado, adjunto encontrará el PDF con los detalles del quedan.\n\n'
        f'Quedan No.: {quedan[0]}\n'
        f'Cantidad de documentos: {len(detalles_procesados)}\n'
        f'Total a pagar: ${total_pago:.2f}\n\n'
        f'Saludos cordiales,\n'
        f'Departamento de Contabilidad'
    )
    file_name = f"QUEDAN NUM {quedan[0]} - {proveedor[0]}.pdf"
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER_QUEDAN,
        to=[proveedor[1]],
    )
    with open(pdf_file_path, 'rb') as pdf_attachment:
        email.attach(file_name, pdf_attachment.read(), 'application/pdf')
    email.send()

    # Eliminar el archivo temporal
    os.remove(pdf_file_path)

    # Responder con el PDF descargable
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quedan_{quedan[1]}.pdf"'
    return response

@login_required
def enviar_quedan_hoy(request):
    # Obtener la fecha actual
    today = datetime.today().date()

    with connections['brilo_sqlserver'].cursor() as cursor:
        # Consultar todos los quedan del día actual
        cursor.execute("""
            SELECT mqdnId, mqdnNumero, mqdnFecha, mqdnFechaPago, mqdnComentarios, prvId 
            FROM olCompras.dbo.maeQuedans 
            WHERE CAST(mqdnFecha AS DATE) = %s
        """, [today])
        quedans = cursor.fetchall()

        for quedan in quedans:
            # Consultar proveedor
            cursor.execute("SELECT prvNombre, prvEmailRepLegal FROM olComun.dbo.Proveedores WHERE prvId = %s", [quedan[5]])
            proveedor = cursor.fetchone()

            # Consultar detalles del quedan
            cursor.execute("""
                SELECT mcoTipoDoc, mcoNumDoc, mcoFecha, mcoSumasAfecto, mcoPorcentRetIVA, mcoPorcentPercep, 
                       mcoTotalAPagarManual, mcoPorcentIVA 
                FROM olCompras.dbo.maeCompras 
                WHERE mqdnId = %s
            """, [quedan[0]])
            detalles = cursor.fetchall()

            # Variables para el cálculo de totales
            total_pago = Decimal(0)
            iva_total = Decimal(0)
            percep_total = Decimal(0)
            retencion_total = Decimal(0)

            detalles_procesados = []
            for detalle in detalles:
                suma_afecto = Decimal(detalle[3]) if detalle[3] is not None else Decimal(0.00)
                por_iva = Decimal(detalle[7]) if detalle[7] is not None else Decimal(0.13)
                por_percep = Decimal(detalle[5]) if detalle[5] is not None else Decimal(0.00)
                por_retencion = Decimal(detalle[4]) if detalle[4] is not None else Decimal(0.00)

                iva = suma_afecto * por_iva
                percep = suma_afecto * por_percep
                retencion = suma_afecto * por_retencion

                total_factura = suma_afecto + iva + percep - retencion if por_percep > 0 else suma_afecto + iva - retencion
                total_pago += total_factura

                iva_total += iva
                percep_total += percep
                retencion_total += retencion

                detalles_procesados.append({
                    'tipo_doc': detalle[0],
                    'num_doc': detalle[1],
                    'fecha': detalle[2],
                    'suma_afecto': suma_afecto,
                    'iva': iva,
                    'percep': percep,
                    'retencion': retencion,
                    'total': total_factura,
                })

            # Renderizar el template HTML para el PDF
            html_content = render_to_string('quedans/quedan_template.html', {
                'quedan': quedan,
                'proveedor': proveedor,
                'detalles': detalles_procesados,
                'total_pago': total_pago,
                'iva_total': iva_total,
                'percep_total': percep_total,
                'retencion_total': retencion_total,
            })

            # Generar el PDF utilizando xhtml2pdf
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer, page_orientation='landscape')

            if pisa_status.err:
                return HttpResponse('Error al generar el PDF', status=500)

            pdf_buffer.seek(0)
            pdf_content = pdf_buffer.getvalue()

            # Guardar el PDF temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                pdf_file.write(pdf_content)
                pdf_file_path = pdf_file.name

            # Construir el asunto y el mensaje del correo
            subject = f'Quedan No. {quedan[1]} - {proveedor[0]}'
            message = (
                f'Estimado, adjunto encontrará el PDF con los detalles del quedan.\n\n'
                f'Quedan No.: {quedan[1]}\n'
                f'Cantidad de documentos: {len(detalles_procesados)}\n'
                f'Total a pagar: ${total_pago:.2f}\n\n'
                f'Saludos cordiales,\n'
                f'Departamento de Contabilidad'
            )

            # Crear el nombre del archivo con el formato solicitado
            file_name = f"QUEDAN NUM {quedan[1]} - {proveedor[0]}.pdf"

            # Crear el objeto EmailMessage
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER_QUEDAN,
                to=[proveedor[1]],  # Correo del proveedor
            )

            # Adjuntar el archivo PDF al correo
            with open(pdf_file_path, 'rb') as pdf_attachment:
                email.attach(file_name, pdf_attachment.read(), 'application/pdf')

            # Enviar el correo
            email.send()

            # Eliminar el archivo temporal después de enviarlo
            os.remove(pdf_file_path)

    # Responder con un mensaje de éxito
    return HttpResponse("Se enviaron todos los quedans generados el día de hoy.", content_type="text/plain")


# ---------------------------------
# ANEXOS DE HACIENDA
# ---------------------------------

# Helpers de formato
def padr(s: str, width: int, char: str = " ") -> str:
    return (s or "").ljust(width, char)[:width]

def padl(s: str, width: int, char: str = " ") -> str:
    return (s or "").rjust(width, char)[-width:]

def format_moneda(v) -> str:
    # dos decimales sin separador de miles
    return f"{v:,.2f}".replace(",", "") if v is not None else "0.00"

# Anexo de Ventas a Consumidor Final
class AnexoConsumidorFinalCSV(View):
    """
    CSV Anexo Consumidor Final para facturas de tipo_dte.codigo = '01'.
    Agrega BOM para que Excel lea correctamente los acentos.
    """

    def get(self, request, *args, **kwargs):
        # Solo facturas cuyo tipo_dte.codigo sea '01'
        qs = FacturaElectronica.objects.filter(
            tipo_dte__codigo='01'
        ).order_by('fecha_emision')

        logger.info(f"[Anexo CSV] facturas tipo_dte=01: {qs.count()}")

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = \
            'attachment; filename="anexo_consumidor_final.csv"'
        response.write('\ufeff')  # BOM para Excel

        writer = csv.writer(response, delimiter=';')

        # Cabecera
        writer.writerow([
            'FECHA DE EMISIÓN',
            'CLASE DE DOCUMENTO',
            'TIPO DE DOCUMENTO',
            'NÚMERO DE RESOLUCIÓN',
            'SERIE DEL DOCUMENTO',
            'NUMERO DE CONTROL INTERNO DEL',
            'NUMERO DE CONTROL INTERNO AL',
            'NÚMERO DE DOCUMENTO (DEL)',
            'NÚMERO DE DOCUMENTO (AL)',
            'NÚMERO DE MAQUINA REGISTRADORA',
            'VENTAS EXENTAS',
            'VENTAS INTERNAS EXENTAS NO SUJETAS A PROPORCIONALIDAD',
            'VENTAS NO SUJETAS',
            'VENTAS GRAVADAS LOCALES',
            'EXPORTACIONES DENTRO DEL ÁREA DE CENTROAMÉRICA',
            'EXPORTACIONES FUERA DEL ÁREA DE CENTROAMÉRICA',
            'EXPORTACIONES DE SERVICIO',
            'VENTAS A ZONAS FRANCAS Y DPA (TASA CERO)',
            'VENTAS A CUENTA DE TERCEROS NO DOMICILIADOS',
            'TOTAL DE VENTAS',
            'TIPO DE OPERACIÓN (RENTA)',
            'TIPO DE INGRESO (RENTA)',
            'NÚMERO DEL ANEXO',
        ])

        for f in qs:
            fecha = f.fecha_emision.strftime('%d/%m/%Y')
            clase = '4'
            # Usamos la descripción que viene de la BD para el tipo 01
            tipo = f"{f.tipo_dte.codigo}"
            num_resol = f.numero_control or ''
            serie = f.codigo_generacion.hex.upper() if f.codigo_generacion else ''

            # Campos internos y máquina vacíos (si no aplica)
            ctrl_del = ctrl_al = doc_del = doc_al = num_reg = ''

            # Montos (asegurar no nulos)
            v_exentas = f.total_exentas or 0
            v_no_sujetas = f.total_no_sujetas or 0
            v_gravadas = f.total_gravadas or 0
            total_ventas = f.total_pagar or 0

            # Operación / ingreso
            tipo_oper = (
                f"{f.condicion_operacion.codigo}"
                if f.condicion_operacion else ''
            )
            tipo_ing = ''  # ajustar si lo calculas distinto

            num_anexo = '2'

            writer.writerow([
                fecha,
                clase,
                tipo,
                num_resol,
                serie,
                ctrl_del,
                ctrl_al,
                doc_del,
                doc_al,
                num_reg,
                f"{v_exentas:.2f}",
                '',  # ventas internas exentas no sujetas
                f"{v_no_sujetas:.2f}",
                f"{v_gravadas:.2f}",
                '0.00', '0.00', '0.00', '0.00', '0.00',
                f"{total_ventas:.2f}",
                tipo_oper,
                tipo_ing,
                num_anexo,
            ])

        return response

# Anexo de Ventas a Contribuyentes
class AnexoContribuyentesCSV(View):
    """
    Genera el CSV ANEXO CONTRIBUYENTES para FacturaElectronica tipo '01'.
    """

    def get(self, request, *args, **kwargs):
        qs = FacturaElectronica.objects.filter(
            tipo_dte__codigo="01"
        ).order_by("fecha_emision")

        logger.info(f"[Anexo Contribuyentes] facturas tipo 01: {qs.count()}")

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = 'attachment; filename="anexo_contribuyentes.csv"'
        resp.write("\ufeff")  # BOM para Excel

        writer = csv.writer(resp, delimiter=";")

        # Cabecera
        writer.writerow([
            "FECHA DE EMISIÓN",
            "CLASE DE DOCUMENTO",
            "TIPO DE DOCUMENTO",
            "NÚMERO DE RESOLUCIÓN",
            "SERIE DEL DOCUMENTO",
            "NÚMERO DE DOCUMENTO",
            "NÚMERO DE CONTROL INTERNO",
            "NIT PROVEEDOR/CLIENTE",
            "NOMBRE RAZÓN SOCIAL",
            "VENTAS EXENTAS",
            "VENTAS NO SUJETAS",
            "VENTAS GRAVADAS LOCALES",
            "DÉBITO FISCAL",
            "VENTAS A TERCEROS NO DOMICILIADOS",
            "DÉBITO TERCEROS",
            "TOTAL DE VENTAS",
            "DUI",
            "TIPO DE OPERACIÓN",
            "TIPO DE INGRESO",
            "NÚMERO DEL ANEXO",
        ])

        for f in qs:
            sFECHADOC    = f.fecha_emision.strftime("%d/%m/%Y")
            sCLASEDOC    = padr("4", 1)   # fijo para DTE
            sTIPODOC     = padr(f.tipo_dte.codigo, 2)
            sNUMRESOL    = padl(f.numero_control, 100)
            sNUMSERIE    = padr(f.codigo_generacion.hex.upper(), 100)
            sNUMDOC      = padr(f.dtereceptor.num_documento or "", 100)
            sNUMINTERNO  = padr("", 100)   # no tiene interno
            sNITPROV     = padl(f.dtereceptor.num_documento or "", 14)
            sNOMBRE      = padr(f.dtereceptor.nombre, 100)

            sVEXENTAS      = padl(format_moneda(f.total_exentas or 0), 11)
            sVNOSUJETAS    = padl(format_moneda(f.total_no_sujetas or 0), 11)
            sVGRAVADAS     = padl(format_moneda(f.total_gravadas or 0), 11)
            sDEBITOFISCAL  = padl(format_moneda(f.iva_retenido or 0), 11)
            sVTERCEROS     = padl(format_moneda(0), 11)
            sDEBITOTERC    = padl(format_moneda(0), 11)
            sTOTALVENTAS   = padl(format_moneda(f.total_pagar or 0), 11)

            sDUI           = padl("", 9)
            sTIPOOPER      = padr(f.condicion_operacion.codigo if f.condicion_operacion else "", 2)
            sTIPOINGRESO   = padr("", 2)
            sNUMANEXO      = padr("1", 1)

            writer.writerow([
                sFECHADOC,
                sCLASEDOC,
                sTIPODOC,
                sNUMRESOL,
                sNUMSERIE,
                sNUMDOC,
                sNUMINTERNO,
                sNITPROV,
                sNOMBRE,
                sVEXENTAS,
                sVNOSUJETAS,
                sVGRAVADAS,
                sDEBITOFISCAL,
                sVTERCEROS,
                sDEBITOTERC,
                sTOTALVENTAS,
                sDUI,
                sTIPOOPER,
                sTIPOINGRESO,
                sNUMANEXO,
            ])

        return resp
    
# Anexo de Compras
class AnexoComprasCSV(View):
    """
    Genera el CSV ANEXO DE COMPRAS (anexo 3).
    """
    def get(self, request, *args, **kwargs):
        qs = Compra.objects.all().order_by('fecha')
        logger.info(f"[Anexo Compras] compras: {qs.count()}")

        resp = HttpResponse(content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = 'attachment; filename="anexo_compras.csv"'
        resp.write('\ufeff')  # BOM para Excel

        writer = csv.writer(resp, delimiter=';')

        # Cabecera:
        writer.writerow([
            'FECHA DE EMISIÓN',
            'CLASE DE DOCUMENTO',
            'TIPO DE DOCUMENTO',
            'NÚMERO DEL DOCUMENTO',
            'NIT PROVEEDOR',
            'NOMBRE PROVEEDOR',
            'COMPRAS INTERNAS EXENTAS',
            'INTERNACIONES EXENTAS Y/O NO SUJETAS',
            'IMPORTACIONES EXENTAS Y/O NO SUJETAS',
            'COMPRAS INTERNAS GRAVADAS',
            'INTERNACIONES GRAVADAS BIENES',
            'IMPORTACIONES GRAVADAS BIENES',
            'IMPORTACIONES GRAVADAS SERVICIOS',
            'CRÉDITO FISCAL',
            'TOTAL DE COMPRAS',
            'DUI',
            'TIPO DE OPERACIÓN',
            'CLASIFICACIÓN',
            'SECTOR',
            'TIPO GASTO/COSTO',
            'NÚMERO DEL ANEXO',
        ])

        for compra in qs:
            # 1) Fechas y documentos: (añade los campos a tu modelo si no existen)
            sFECHADOC    = compra.fecha.strftime('%d/%m/%Y')
            sCLASEDOC    = padr('4', 1)               # fijo DTE
            sTIPODOC     = padr(getattr(compra, 'tipo_documento', ''), 2)
            sNUMDOC      = padr(getattr(compra, 'numero_documento', ''), 100)

            # 2) Proveedor:
            sNITPROV     = padl(compra.proveedor.ruc_nit, 14)
            sNOMBRE      = padr(compra.proveedor.nombre, 100)

            # 3) Montos (aquí debes definir la lógica de cálculo según tus categorías):
            detalles = compra.detalles.all()
            # Ejemplo: todo como ‘gravado’ salvo producto.precio_iva==False
            exentas_int = sum(d.subtotal for d in detalles if not d.producto.precio_iva)
            gravadas_int= sum(d.subtotal for d in detalles if d.producto.precio_iva)
            # Para los demás campos (importaciones, internaciones, etc.) necesitas
            # un flag en DetalleCompra o Producto para diferenciarlos; por ahora cero:
            sCOMPRASEXENTAS     = padl(format_moneda(exentas_int), 11)
            sINTEREXENTAS       = padl('0.00', 11)
            sIMPOREXENTAS       = padl('0.00', 11)
            sCOMPRASGRAVADAS    = padl(format_moneda(gravadas_int), 11)
            sINTERGRAVBIENES    = padl('0.00', 11)
            sIMPORGRAVBIENES    = padl('0.00', 11)
            sIMPORGRAVSERV      = padl('0.00', 11)
            # Crédito fiscal = suma de IVA en detalles (si lo calculas)
            credito_fiscal      = sum(
                (d.subtotal * Decimal('0.13')).quantize(Decimal('0.01'))
                for d in detalles if d.producto.precio_iva
            )
            sCREDITOFISCAL      = padl(format_moneda(credito_fiscal), 11)
            sTOTALCOMPRAS       = padl(format_moneda(compra.total), 11)

            # 4) Otros campos que el macro usa: añade a tu modelo si no existen
            sDUI                = padl('', 9)
            sTIPOOPERACION      = padr(getattr(compra, 'tipo_operacion', ''), 1)
            sCLASIFICACION      = padr(getattr(compra, 'clasificacion', ''), 1)
            sSECTOR             = padr(getattr(compra, 'sector', ''), 1)
            sTIPOCOSTOGASTO     = padr(getattr(compra, 'tipo_costo_gasto', ''), 1)

            sNUMANEXO           = padr('3', 1)

            writer.writerow([
                sFECHADOC,
                sCLASEDOC,
                sTIPODOC,
                sNUMDOC,
                sNITPROV,
                sNOMBRE,
                sCOMPRASEXENTAS,
                sINTEREXENTAS,
                sIMPOREXENTAS,
                sCOMPRASGRAVADAS,
                sINTERGRAVBIENES,
                sIMPORGRAVBIENES,
                sIMPORGRAVSERV,
                sCREDITOFISCAL,
                sTOTALCOMPRAS,
                sDUI,
                sTIPOOPERACION,
                sCLASIFICACION,
                sSECTOR,
                sTIPOCOSTOGASTO,
                sNUMANEXO,
            ])

        return resp


# ─────────────────────────────────────────────────────────────────────────────
# PLAN DE CUENTAS
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def cuentas_lista(request):
    q    = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()

    qs = CuentaContable.objects.select_related('cuenta_padre').all()
    if q:
        qs = qs.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q))
    if tipo:
        qs = qs.filter(tipo=tipo)

    paginator = Paginator(qs, 25)
    page      = request.GET.get('page')
    cuentas   = paginator.get_page(page)

    return render(request, 'contabilidad/cuentas/lista.html', {
        'cuentas': cuentas,
        'q':       q,
        'f_tipo':  tipo,
        'tipos':   CuentaContable.TIPO_CHOICES,
    })


@login_required
def cuentas_crear(request):
    if request.method == 'POST':
        try:
            cuenta = _cuenta_desde_post(request.POST)
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.codigo} creada correctamente.')
            return redirect('cont-cuentas-lista')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'contabilidad/cuentas/form.html', {
        'titulo':      'Nueva cuenta',
        'tipos':       CuentaContable.TIPO_CHOICES,
        'naturalezas': CuentaContable.NATURALEZA_CHOICES,
        'niveles':     CuentaContable.NIVEL_CHOICES,
        'padres':      CuentaContable.objects.filter(nivel='PADRE', activa=True).order_by('codigo'),
    })


@login_required
def cuentas_editar(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)

    if request.method == 'POST':
        try:
            _cuenta_desde_post(request.POST, cuenta)
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.codigo} actualizada.')
            return redirect('cont-cuentas-lista')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'contabilidad/cuentas/form.html', {
        'titulo':      'Editar cuenta',
        'cuenta':      cuenta,
        'tipos':       CuentaContable.TIPO_CHOICES,
        'naturalezas': CuentaContable.NATURALEZA_CHOICES,
        'niveles':     CuentaContable.NIVEL_CHOICES,
        'padres':      CuentaContable.objects.filter(nivel='PADRE', activa=True).exclude(pk=pk).order_by('codigo'),
    })


@login_required
def cuentas_eliminar(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    if request.method == 'POST':
        if cuenta.lineas.exists():
            messages.error(request, 'No se puede eliminar: la cuenta tiene movimientos registrados.')
        elif cuenta.subcuentas.exists():
            messages.error(request, 'No se puede eliminar: la cuenta tiene subcuentas.')
        else:
            nombre = str(cuenta)
            cuenta.delete()
            messages.success(request, f'Cuenta {nombre} eliminada.')
    return redirect('cont-cuentas-lista')


def _cuenta_desde_post(post, cuenta=None):
    if cuenta is None:
        cuenta = CuentaContable()
    cuenta.codigo      = post.get('codigo', '').strip()
    cuenta.nombre      = post.get('nombre', '').strip()
    cuenta.tipo        = post.get('tipo', '')
    cuenta.naturaleza  = post.get('naturaleza', '')
    cuenta.nivel       = post.get('nivel', 'DETALLE')
    cuenta.descripcion = post.get('descripcion', '').strip()
    cuenta.activa      = post.get('activa') == 'on'
    padre_id           = post.get('cuenta_padre') or None
    cuenta.cuenta_padre_id = padre_id

    if not cuenta.codigo:
        raise ValueError('El código es obligatorio.')
    if not cuenta.nombre:
        raise ValueError('El nombre es obligatorio.')
    return cuenta


# ─────────────────────────────────────────────────────────────────────────────
# ASIENTOS CONTABLES
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def asientos_lista(request):
    q       = request.GET.get('q', '').strip()
    periodo = request.GET.get('periodo', '').strip()
    estado  = request.GET.get('estado', '').strip()

    qs = AsientoContable.objects.all()
    if q:
        qs = qs.filter(Q(concepto__icontains=q) | Q(numero__icontains=q))
    if periodo:
        qs = qs.filter(periodo=periodo)
    if estado:
        qs = qs.filter(estado=estado)

    paginator = Paginator(qs, 20)
    page      = request.GET.get('page')
    asientos  = paginator.get_page(page)

    return render(request, 'contabilidad/asientos/lista.html', {
        'asientos':  asientos,
        'q':         q,
        'f_periodo': periodo,
        'f_estado':  estado,
        'estados':   AsientoContable.ESTADO_CHOICES,
    })


@login_required
def asientos_crear(request):
    cuentas_detalle = CuentaContable.objects.filter(nivel='DETALLE', activa=True).order_by('codigo')

    if request.method == 'POST':
        error = _guardar_asiento(request, asiento=None)
        if error is None:
            messages.success(request, 'Asiento creado correctamente.')
            return redirect('cont-asientos-lista')
        messages.error(request, error)

    return render(request, 'contabilidad/asientos/form.html', {
        'titulo':          'Nuevo asiento',
        'cuentas_detalle': cuentas_detalle,
        'estados':         AsientoContable.ESTADO_CHOICES,
    })


@login_required
def asientos_ver(request, pk):
    asiento = get_object_or_404(AsientoContable, pk=pk)
    lineas  = asiento.lineas.select_related('cuenta').all()
    return render(request, 'contabilidad/asientos/detalle.html', {
        'asiento': asiento,
        'lineas':  lineas,
    })


@login_required
def asientos_editar(request, pk):
    asiento         = get_object_or_404(AsientoContable, pk=pk)
    cuentas_detalle = CuentaContable.objects.filter(nivel='DETALLE', activa=True).order_by('codigo')

    if asiento.estado == 'CONFIRMADO':
        messages.error(request, 'No se puede editar un asiento confirmado.')
        return redirect('cont-asientos-ver', pk=pk)

    if request.method == 'POST':
        error = _guardar_asiento(request, asiento=asiento)
        if error is None:
            messages.success(request, 'Asiento actualizado.')
            return redirect('cont-asientos-ver', pk=pk)
        messages.error(request, error)

    lineas_existentes = list(asiento.lineas.select_related('cuenta').all())
    return render(request, 'contabilidad/asientos/form.html', {
        'titulo':            'Editar asiento',
        'asiento':           asiento,
        'lineas_existentes': lineas_existentes,
        'cuentas_detalle':   cuentas_detalle,
        'estados':           AsientoContable.ESTADO_CHOICES,
    })


@login_required
def asientos_confirmar(request, pk):
    asiento = get_object_or_404(AsientoContable, pk=pk)
    if request.method == 'POST':
        if not asiento.lineas.exists():
            messages.error(request, 'El asiento no tiene líneas.')
        elif not asiento.esta_cuadrado:
            messages.error(request, f'El asiento no cuadra: Debe={asiento.total_debe} / Haber={asiento.total_haber}.')
        else:
            asiento.estado = 'CONFIRMADO'
            asiento.save()
            messages.success(request, f'Asiento #{asiento.numero} confirmado.')
    return redirect('cont-asientos-ver', pk=pk)


@login_required
def asientos_eliminar(request, pk):
    asiento = get_object_or_404(AsientoContable, pk=pk)
    if request.method == 'POST':
        if asiento.estado == 'CONFIRMADO':
            messages.error(request, 'No se puede eliminar un asiento confirmado.')
            return redirect('cont-asientos-ver', pk=pk)
        num = asiento.numero
        asiento.delete()
        messages.success(request, f'Asiento #{num} eliminado.')
    return redirect('cont-asientos-lista')


def _guardar_asiento(request, asiento=None):
    """Guarda un asiento y sus líneas. Retorna None si ok, string de error si falla."""
    post     = request.POST
    fecha    = post.get('fecha', '').strip()
    concepto = post.get('concepto', '').strip()
    estado   = post.get('estado', 'BORRADOR')

    if not fecha or not concepto:
        return 'Fecha y concepto son obligatorios.'

    cuentas_ids = post.getlist('linea_cuenta')
    descrips    = post.getlist('linea_descripcion')
    debes       = post.getlist('linea_debe')
    haberes     = post.getlist('linea_haber')

    lineas_data = []
    for i, cid in enumerate(cuentas_ids):
        if not cid:
            continue
        try:
            cuenta = CuentaContable.objects.get(pk=cid)
        except CuentaContable.DoesNotExist:
            return f'Cuenta con id {cid} no existe.'
        try:
            debe  = Decimal(debes[i]  or '0')
            haber = Decimal(haberes[i] or '0')
        except Exception:
            return 'Valores de debe/haber inválidos.'
        lineas_data.append({
            'cuenta':      cuenta,
            'descripcion': descrips[i] if i < len(descrips) else '',
            'debe':        debe,
            'haber':       haber,
        })

    if not lineas_data:
        return 'El asiento debe tener al menos una línea.'

    total_debe  = sum(l['debe']  for l in lineas_data)
    total_haber = sum(l['haber'] for l in lineas_data)

    if estado == 'CONFIRMADO' and total_debe != total_haber:
        return f'El asiento no cuadra: Debe={total_debe} / Haber={total_haber}.'

    if asiento is None:
        asiento = AsientoContable(creado_por=request.user)
    asiento.fecha    = fecha
    asiento.concepto = concepto
    asiento.estado   = estado
    asiento.save()

    asiento.lineas.all().delete()
    for l in lineas_data:
        LineaAsiento.objects.create(
            asiento=asiento,
            cuenta=l['cuenta'],
            descripcion=l['descripcion'],
            debe=l['debe'],
            haber=l['haber'],
        )
    return None


# ─────────────────────────────────────────────────────────────────────────────
# CUENTAS POR COBRAR
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def cpc_lista(request):
    q       = request.GET.get('q', '').strip()
    estado  = request.GET.get('estado', '').strip()
    vencidas = request.GET.get('vencidas', '').strip()

    qs = CuentaPorCobrar.objects.select_related('receptor', 'factura').all()
    if q:
        qs = qs.filter(Q(receptor__nombre__icontains=q) | Q(factura__numero_control__icontains=q))
    if estado:
        qs = qs.filter(estado=estado)
    if vencidas == '1':
        from datetime import date
        qs = qs.filter(fecha_vencimiento__lt=date.today(), estado__in=['PENDIENTE', 'PARCIAL'])

    paginator = Paginator(qs, 20)
    cuentas   = paginator.get_page(request.GET.get('page'))

    return render(request, 'contabilidad/cpc/lista.html', {
        'cuentas':  cuentas,
        'q':        q,
        'f_estado': estado,
        'f_vencidas': vencidas,
        'estados':  CuentaPorCobrar.ESTADO_CHOICES,
    })


@login_required
def cpc_crear(request):
    """Selecciona una FacturaElectronica y registra como Cuenta por Cobrar."""
    # Facturas a crédito que aún no tienen CxC registrada
    facturas = FacturaElectronica.objects.filter(
        condicion_operacion__codigo='2'
    ).exclude(
        cuentas_cobrar__isnull=False
    ).select_related('dtereceptor', 'tipo_dte', 'condicion_operacion').order_by('-fecha_emision')[:200]

    if request.method == 'POST':
        factura_id       = request.POST.get('factura')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        notas            = request.POST.get('notas', '').strip()

        try:
            factura = FacturaElectronica.objects.get(pk=factura_id)
        except FacturaElectronica.DoesNotExist:
            messages.error(request, 'Factura no encontrada.')
            return redirect('cont-cpc-crear')

        if CuentaPorCobrar.objects.filter(factura=factura).exists():
            messages.error(request, 'Esta factura ya tiene una cuenta por cobrar registrada.')
            return redirect('cont-cpc-lista')

        cpc = CuentaPorCobrar.objects.create(
            factura=factura,
            receptor=factura.dtereceptor,
            fecha_emision=factura.fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            monto_original=factura.total_pagar,
            notas=notas,
            creado_por=request.user,
        )
        messages.success(request, f'Cuenta por Cobrar #{cpc.pk} creada correctamente.')
        return redirect('cont-cpc-detalle', pk=cpc.pk)

    return render(request, 'contabilidad/cpc/crear.html', {'facturas': facturas})


@login_required
def cpc_detalle(request, pk):
    cpc   = get_object_or_404(CuentaPorCobrar, pk=pk)
    pagos = cpc.pagos.select_related('asiento', 'cuenta_debito', 'cuenta_credito').all()
    cuentas_detalle = CuentaContable.objects.filter(nivel='DETALLE', activa=True).order_by('codigo')
    return render(request, 'contabilidad/cpc/detalle.html', {
        'cpc':             cpc,
        'pagos':           pagos,
        'cuentas_detalle': cuentas_detalle,
    })


@login_required
def cpc_registrar_pago(request, pk):
    cpc = get_object_or_404(CuentaPorCobrar, pk=pk)

    if cpc.estado == 'PAGADO':
        messages.error(request, 'Esta cuenta ya está completamente pagada.')
        return redirect('cont-cpc-detalle', pk=pk)
    if cpc.estado == 'ANULADO':
        messages.error(request, 'No se puede registrar pago en una cuenta anulada.')
        return redirect('cont-cpc-detalle', pk=pk)

    if request.method == 'POST':
        try:
            monto = Decimal(request.POST.get('monto', '0'))
        except Exception:
            messages.error(request, 'Monto inválido.')
            return redirect('cont-cpc-detalle', pk=pk)

        if monto <= 0:
            messages.error(request, 'El monto debe ser mayor a cero.')
            return redirect('cont-cpc-detalle', pk=pk)
        if monto > cpc.saldo_pendiente:
            messages.error(request, f'El monto excede el saldo pendiente (${cpc.saldo_pendiente}).')
            return redirect('cont-cpc-detalle', pk=pk)

        cuenta_debito_id  = request.POST.get('cuenta_debito')
        cuenta_credito_id = request.POST.get('cuenta_credito')

        pago = PagoCobro(
            cuenta_cobrar=cpc,
            fecha=request.POST.get('fecha'),
            monto=monto,
            forma_pago=request.POST.get('forma_pago', 'EFECTIVO'),
            referencia=request.POST.get('referencia', '').strip(),
            notas=request.POST.get('notas', '').strip(),
            creado_por=request.user,
        )
        if cuenta_debito_id:
            pago.cuenta_debito_id = cuenta_debito_id
        if cuenta_credito_id:
            pago.cuenta_credito_id = cuenta_credito_id
        pago.save()

        if pago.cuenta_debito and pago.cuenta_credito:
            pago.generar_asiento()
            messages.success(request, f'Pago de ${monto} registrado con asiento contable generado.')
        else:
            messages.success(request, f'Pago de ${monto} registrado. Sin asiento (no se seleccionaron cuentas).')

        cpc.actualizar_estado()

    return redirect('cont-cpc-detalle', pk=pk)


@login_required
def cpc_anular(request, pk):
    cpc = get_object_or_404(CuentaPorCobrar, pk=pk)
    if request.method == 'POST':
        if cpc.estado == 'PAGADO':
            messages.error(request, 'No se puede anular una cuenta completamente pagada.')
        else:
            cpc.estado = 'ANULADO'
            cpc.save(update_fields=['estado'])
            messages.success(request, f'Cuenta por Cobrar #{cpc.pk} anulada.')
    return redirect('cont-cpc-lista')


# ─────────────────────────────────────────────────────────────────────────────
# CUENTAS POR PAGAR
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def cpp_lista(request):
    q       = request.GET.get('q', '').strip()
    estado  = request.GET.get('estado', '').strip()
    vencidas = request.GET.get('vencidas', '').strip()

    qs = CuentaPorPagar.objects.select_related('proveedor', 'compra').all()
    if q:
        qs = qs.filter(Q(proveedor__nombre__icontains=q) | Q(compra__numero_documento__icontains=q))
    if estado:
        qs = qs.filter(estado=estado)
    if vencidas == '1':
        from datetime import date
        qs = qs.filter(fecha_vencimiento__lt=date.today(), estado__in=['PENDIENTE', 'PARCIAL'])

    paginator = Paginator(qs, 20)
    cuentas   = paginator.get_page(request.GET.get('page'))

    return render(request, 'contabilidad/cpp/lista.html', {
        'cuentas':    cuentas,
        'q':          q,
        'f_estado':   estado,
        'f_vencidas': vencidas,
        'estados':    CuentaPorPagar.ESTADO_CHOICES,
    })


@login_required
def cpp_crear(request):
    """Selecciona una Compra y registra como Cuenta por Pagar."""
    # Compras pendientes de pago que aún no tienen CxP registrada
    compras = Compra.objects.filter(
        estado='Pendiente'
    ).exclude(
        cuentas_pagar__isnull=False
    ).select_related('proveedor').order_by('-fecha')[:200]

    if request.method == 'POST':
        compra_id        = request.POST.get('compra')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        notas            = request.POST.get('notas', '').strip()

        try:
            compra = Compra.objects.get(pk=compra_id)
        except Compra.DoesNotExist:
            messages.error(request, 'Compra no encontrada.')
            return redirect('cont-cpp-crear')

        if CuentaPorPagar.objects.filter(compra=compra).exists():
            messages.error(request, 'Esta compra ya tiene una cuenta por pagar registrada.')
            return redirect('cont-cpp-lista')

        cpp = CuentaPorPagar.objects.create(
            compra=compra,
            proveedor=compra.proveedor,
            fecha_emision=compra.fecha.date() if hasattr(compra.fecha, 'date') else compra.fecha,
            fecha_vencimiento=fecha_vencimiento,
            monto_original=compra.total,
            notas=notas,
            creado_por=request.user,
        )
        messages.success(request, f'Cuenta por Pagar #{cpp.pk} creada correctamente.')
        return redirect('cont-cpp-detalle', pk=cpp.pk)

    return render(request, 'contabilidad/cpp/crear.html', {'compras': compras})


@login_required
def cpp_detalle(request, pk):
    cpp   = get_object_or_404(CuentaPorPagar, pk=pk)
    pagos = cpp.pagos.select_related('asiento', 'cuenta_debito', 'cuenta_credito').all()
    cuentas_detalle = CuentaContable.objects.filter(nivel='DETALLE', activa=True).order_by('codigo')
    return render(request, 'contabilidad/cpp/detalle.html', {
        'cpp':             cpp,
        'pagos':           pagos,
        'cuentas_detalle': cuentas_detalle,
    })


@login_required
def cpp_registrar_pago(request, pk):
    cpp = get_object_or_404(CuentaPorPagar, pk=pk)

    if cpp.estado == 'PAGADO':
        messages.error(request, 'Esta cuenta ya está completamente pagada.')
        return redirect('cont-cpp-detalle', pk=pk)
    if cpp.estado == 'ANULADO':
        messages.error(request, 'No se puede registrar pago en una cuenta anulada.')
        return redirect('cont-cpp-detalle', pk=pk)

    if request.method == 'POST':
        try:
            monto = Decimal(request.POST.get('monto', '0'))
        except Exception:
            messages.error(request, 'Monto inválido.')
            return redirect('cont-cpp-detalle', pk=pk)

        if monto <= 0:
            messages.error(request, 'El monto debe ser mayor a cero.')
            return redirect('cont-cpp-detalle', pk=pk)
        if monto > cpp.saldo_pendiente:
            messages.error(request, f'El monto excede el saldo pendiente (${cpp.saldo_pendiente}).')
            return redirect('cont-cpp-detalle', pk=pk)

        cuenta_debito_id  = request.POST.get('cuenta_debito')
        cuenta_credito_id = request.POST.get('cuenta_credito')

        pago = PagoPagar(
            cuenta_pagar=cpp,
            fecha=request.POST.get('fecha'),
            monto=monto,
            forma_pago=request.POST.get('forma_pago', 'EFECTIVO'),
            referencia=request.POST.get('referencia', '').strip(),
            notas=request.POST.get('notas', '').strip(),
            creado_por=request.user,
        )
        if cuenta_debito_id:
            pago.cuenta_debito_id = cuenta_debito_id
        if cuenta_credito_id:
            pago.cuenta_credito_id = cuenta_credito_id
        pago.save()

        if pago.cuenta_debito and pago.cuenta_credito:
            pago.generar_asiento()
            messages.success(request, f'Pago de ${monto} registrado con asiento contable generado.')
        else:
            messages.success(request, f'Pago de ${monto} registrado. Sin asiento (no se seleccionaron cuentas).')

        cpp.actualizar_estado()

    return redirect('cont-cpp-detalle', pk=pk)


@login_required
def cpp_anular(request, pk):
    cpp = get_object_or_404(CuentaPorPagar, pk=pk)
    if request.method == 'POST':
        if cpp.estado == 'PAGADO':
            messages.error(request, 'No se puede anular una cuenta completamente pagada.')
        else:
            cpp.estado = 'ANULADO'
            cpp.save(update_fields=['estado'])
            messages.success(request, f'Cuenta por Pagar #{cpp.pk} anulada.')
    return redirect('cont-cpp-lista')


# ─────────────────────────────────────────────────────────────────────────────
# LIBRO MAYOR
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def libro_mayor(request):
    from django.db.models import Sum, Q
    from datetime import date

    cuenta_id  = request.GET.get('cuenta', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()

    cuentas_detalle = CuentaContable.objects.filter(nivel='DETALLE', activa=True).order_by('codigo')
    cuenta_sel      = None
    movimientos     = []
    saldo_inicial   = Decimal('0')
    total_debe      = Decimal('0')
    total_haber     = Decimal('0')
    saldo_final     = Decimal('0')

    if cuenta_id:
        cuenta_sel = get_object_or_404(CuentaContable, pk=cuenta_id)

        # Líneas de asientos confirmados para esta cuenta
        lineas_qs = LineaAsiento.objects.filter(
            cuenta=cuenta_sel,
            asiento__estado='CONFIRMADO',
        ).select_related('asiento').order_by('asiento__fecha', 'asiento__numero')

        # Saldo inicial: movimientos ANTES de fecha_desde
        if fecha_desde:
            lineas_antes = lineas_qs.filter(asiento__fecha__lt=fecha_desde)
            d_antes = lineas_antes.aggregate(t=Sum('debe'))['t']  or Decimal('0')
            h_antes = lineas_antes.aggregate(t=Sum('haber'))['t'] or Decimal('0')
            if cuenta_sel.naturaleza == 'DEUDORA':
                saldo_inicial = d_antes - h_antes
            else:
                saldo_inicial = h_antes - d_antes
            lineas_qs = lineas_qs.filter(asiento__fecha__gte=fecha_desde)

        if fecha_hasta:
            lineas_qs = lineas_qs.filter(asiento__fecha__lte=fecha_hasta)

        saldo_acum = saldo_inicial
        for linea in lineas_qs:
            if cuenta_sel.naturaleza == 'DEUDORA':
                saldo_acum += linea.debe - linea.haber
            else:
                saldo_acum += linea.haber - linea.debe
            movimientos.append({
                'fecha':    linea.asiento.fecha,
                'numero':   linea.asiento.numero,
                'asiento_pk': linea.asiento.pk,
                'concepto': linea.asiento.concepto,
                'detalle':  linea.descripcion,
                'debe':     linea.debe,
                'haber':    linea.haber,
                'saldo':    saldo_acum,
            })
            total_debe  += linea.debe
            total_haber += linea.haber

        saldo_final = saldo_inicial + (total_debe - total_haber if cuenta_sel.naturaleza == 'DEUDORA'
                                       else total_haber - total_debe)

    return render(request, 'contabilidad/reportes/libro_mayor.html', {
        'cuentas_detalle': cuentas_detalle,
        'cuenta_sel':      cuenta_sel,
        'movimientos':     movimientos,
        'saldo_inicial':   saldo_inicial,
        'total_debe':      total_debe,
        'total_haber':     total_haber,
        'saldo_final':     saldo_final,
        'fecha_desde':     fecha_desde,
        'fecha_hasta':     fecha_hasta,
    })


# ─────────────────────────────────────────────────────────────────────────────
# BALANCE DE COMPROBACIÓN
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def balance_comprobacion(request):
    from django.db.models import Sum

    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()

    lineas_qs = LineaAsiento.objects.filter(asiento__estado='CONFIRMADO')
    if fecha_desde:
        lineas_qs = lineas_qs.filter(asiento__fecha__gte=fecha_desde)
    if fecha_hasta:
        lineas_qs = lineas_qs.filter(asiento__fecha__lte=fecha_hasta)

    # Agrupar por cuenta
    totales = (
        lineas_qs
        .values('cuenta__id', 'cuenta__codigo', 'cuenta__nombre',
                'cuenta__tipo', 'cuenta__naturaleza')
        .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
        .order_by('cuenta__codigo')
    )

    filas = []
    gran_debe = gran_haber = gran_saldo_d = gran_saldo_a = Decimal('0')

    for t in totales:
        debe  = t['total_debe']  or Decimal('0')
        haber = t['total_haber'] or Decimal('0')
        if t['cuenta__naturaleza'] == 'DEUDORA':
            saldo_d = max(debe - haber, Decimal('0'))
            saldo_a = max(haber - debe, Decimal('0'))
        else:
            saldo_a = max(haber - debe, Decimal('0'))
            saldo_d = max(debe - haber, Decimal('0'))

        filas.append({
            'id':        t['cuenta__id'],
            'codigo':    t['cuenta__codigo'],
            'nombre':    t['cuenta__nombre'],
            'tipo':      t['cuenta__tipo'],
            'naturaleza': t['cuenta__naturaleza'],
            'debe':      debe,
            'haber':     haber,
            'saldo_d':   saldo_d,
            'saldo_a':   saldo_a,
        })
        gran_debe    += debe
        gran_haber   += haber
        gran_saldo_d += saldo_d
        gran_saldo_a += saldo_a

    return render(request, 'contabilidad/reportes/balance_comprobacion.html', {
        'filas':       filas,
        'gran_debe':   gran_debe,
        'gran_haber':  gran_haber,
        'gran_saldo_d': gran_saldo_d,
        'gran_saldo_a': gran_saldo_a,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    })


# ─────────────────────────────────────────────────────────────────────────────
# BALANCE GENERAL
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def balance_general(request):
    from django.db.models import Sum

    fecha_hasta = request.GET.get('fecha_hasta', '').strip()

    lineas_qs = LineaAsiento.objects.filter(asiento__estado='CONFIRMADO')
    if fecha_hasta:
        lineas_qs = lineas_qs.filter(asiento__fecha__lte=fecha_hasta)

    totales = (
        lineas_qs
        .values('cuenta__id', 'cuenta__codigo', 'cuenta__nombre',
                'cuenta__tipo', 'cuenta__naturaleza')
        .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
        .order_by('cuenta__codigo')
    )

    activos   = []
    pasivos   = []
    capital   = []
    ingresos  = []
    gastos    = []

    for t in totales:
        debe  = t['total_debe']  or Decimal('0')
        haber = t['total_haber'] or Decimal('0')
        if t['cuenta__naturaleza'] == 'DEUDORA':
            saldo = debe - haber
        else:
            saldo = haber - debe

        fila = {
            'id':     t['cuenta__id'],
            'codigo': t['cuenta__codigo'],
            'nombre': t['cuenta__nombre'],
            'saldo':  saldo,
        }
        tipo = t['cuenta__tipo']
        if   tipo == 'ACTIVO':   activos.append(fila)
        elif tipo == 'PASIVO':   pasivos.append(fila)
        elif tipo == 'CAPITAL':  capital.append(fila)
        elif tipo == 'INGRESO':  ingresos.append(fila)
        elif tipo == 'GASTO':    gastos.append(fila)

    total_activos  = sum(f['saldo'] for f in activos)
    total_pasivos  = sum(f['saldo'] for f in pasivos)
    total_capital  = sum(f['saldo'] for f in capital)
    total_ingresos = sum(f['saldo'] for f in ingresos)
    total_gastos   = sum(f['saldo'] for f in gastos)
    utilidad       = total_ingresos - total_gastos
    total_pasivos_capital = total_pasivos + total_capital + utilidad

    return render(request, 'contabilidad/reportes/balance_general.html', {
        'activos':               activos,
        'pasivos':               pasivos,
        'capital':               capital,
        'ingresos':              ingresos,
        'gastos':                gastos,
        'total_activos':         total_activos,
        'total_pasivos':         total_pasivos,
        'total_capital':         total_capital,
        'total_ingresos':        total_ingresos,
        'total_gastos':          total_gastos,
        'utilidad':              utilidad,
        'total_pasivos_capital': total_pasivos_capital,
        'cuadra':                abs(total_activos - total_pasivos_capital) < Decimal('0.01'),
        'fecha_hasta':           fecha_hasta,
    })


# ─────────────────────────────────────────────────────────────────────────────
# ESTADO DE RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def estado_resultados(request):
    from django.db.models import Sum

    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()

    lineas_qs = LineaAsiento.objects.filter(
        asiento__estado='CONFIRMADO',
        cuenta__tipo__in=['INGRESO', 'GASTO'],
    )
    if fecha_desde:
        lineas_qs = lineas_qs.filter(asiento__fecha__gte=fecha_desde)
    if fecha_hasta:
        lineas_qs = lineas_qs.filter(asiento__fecha__lte=fecha_hasta)

    totales = (
        lineas_qs
        .values('cuenta__id', 'cuenta__codigo', 'cuenta__nombre',
                'cuenta__tipo', 'cuenta__naturaleza', 'cuenta__cuenta_padre__nombre')
        .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
        .order_by('cuenta__tipo', 'cuenta__codigo')
    )

    ingresos = []
    gastos   = []

    for t in totales:
        debe  = t['total_debe']  or Decimal('0')
        haber = t['total_haber'] or Decimal('0')
        # Ingresos son acreedoras: saldo = haber - debe
        # Gastos son deudoras: saldo = debe - haber
        if t['cuenta__tipo'] == 'INGRESO':
            saldo = haber - debe
            ingresos.append({
                'id':     t['cuenta__id'],
                'codigo': t['cuenta__codigo'],
                'nombre': t['cuenta__nombre'],
                'padre':  t['cuenta__cuenta_padre__nombre'],
                'saldo':  saldo,
            })
        else:
            saldo = debe - haber
            gastos.append({
                'id':     t['cuenta__id'],
                'codigo': t['cuenta__codigo'],
                'nombre': t['cuenta__nombre'],
                'padre':  t['cuenta__cuenta_padre__nombre'],
                'saldo':  saldo,
            })

    total_ingresos = sum(f['saldo'] for f in ingresos)
    total_gastos   = sum(f['saldo'] for f in gastos)
    utilidad_bruta = total_ingresos - total_gastos

    return render(request, 'contabilidad/reportes/estado_resultados.html', {
        'ingresos':       ingresos,
        'gastos':         gastos,
        'total_ingresos': total_ingresos,
        'total_gastos':   total_gastos,
        'utilidad_bruta': utilidad_bruta,
        'es_utilidad':    utilidad_bruta >= 0,
        'fecha_desde':    fecha_desde,
        'fecha_hasta':    fecha_hasta,
    })