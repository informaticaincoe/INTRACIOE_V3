# views.py
from io import BytesIO
import io
import os
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connections
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

