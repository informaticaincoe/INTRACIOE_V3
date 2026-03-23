import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from FE.models import (
    Ambiente, Emisor_fe, Municipio, TiposDocIDReceptor, TiposEstablecimientos,
)

from .models import ConfiguracionServidor

logger = logging.getLogger('AUTENTICACION')

# Claves agrupadas por sección para mostrar en la UI
GRUPOS_CONFIG = {
    'hacienda': {
        'titulo': 'Hacienda / API DTE',
        'icono': 'bi-cloud-upload',
        'claves': [
            ('hacienda_url_prod',       'URL Producción Hacienda',          'url_endpoint', 'https://apiefe.dtes.mh.gob.sv/fesv/recepciondte'),
            ('hacienda_url_test',       'URL Pruebas Hacienda',             'url_endpoint', 'https://apitest.dtes.mh.gob.sv/fesv/recepciondte'),
            ('url_autenticacion',       'URL Autenticación Hacienda',       'url_endpoint', 'https://apitest.dtes.mh.gob.sv/seguridad/auth'),
            ('consulta_dte',            'URL Consulta DTE',                 'url_endpoint', 'https://admin.factura.gob.sv/consultaPublica'),
            ('url_invalidar_dte',       'URL Invalidar DTE',                'url_endpoint', ''),
            ('hacienda_contingencia_url','URL Contingencia Hacienda',       'url_endpoint', ''),
        ],
    },
    'firmador': {
        'titulo': 'Firmador y Servidor',
        'icono': 'bi-shield-lock',
        'claves': [
            ('firmador',    'URL del Firmador',         'url',          'http://127.0.0.1:8113/firmardocumento/'),
            ('server_url',  'URL del Servidor (Django)', 'url',         'http://127.0.0.1:8000'),
            ('certificado', 'Ruta al Certificado (.p12)', 'url',        'FE/cert/mi_certificado.p12'),
        ],
    },
    'rutas': {
        'titulo': 'Rutas de Archivos',
        'icono': 'bi-folder2-open',
        'claves': [
            ('ruta_comprobantes_dte',   'Carpeta comprobantes DTE',     'url', 'FE/comprobantes_dte/'),
            ('ruta_comprobante_json',   'Carpeta comprobantes JSON',    'url', 'FE/comprobantes_json/'),
            ('json_factura',            'Carpeta JSON facturas',        'url', 'FE/json_facturas/'),
            ('json_facturas_firmadas',  'Carpeta JSON firmados',        'url', 'FE/json_firmados/'),
            ('schema_json',             'Ruta esquema JSON',            'url', 'FE/json_schemas/fe-fc-v1.json'),
        ],
    },
    'api': {
        'titulo': 'Parámetros de API',
        'icono': 'bi-code-square',
        'claves': [
            ('user_agent',                  'User-Agent',                       'valor', 'INTRACOE/1.0'),
            ('headers',                     'Headers',                          'valor', 'application/json'),
            ('content_type',               'Content-Type',                     'valor', 'application/json'),
            ('version_evento_invalidacion', 'Versión evento invalidación',      'valor', '1'),
            ('version_evento_contingencia', 'Versión evento contingencia',      'valor', '1'),
            ('email_host_fe',              'Correo para envío de facturas',    'valor', ''),
        ],
    },
}


def _get_config():
    """Devuelve dict {clave: instancia ConfiguracionServidor}."""
    return {c.clave: c for c in ConfiguracionServidor.objects.all()}


def _es_admin(user):
    return user.is_staff or user.is_superuser or getattr(user, 'is_admin', False)


@login_required
@user_passes_test(_es_admin)
def configuracion_empresa(request):
    emisor = Emisor_fe.objects.first()
    config = _get_config()

    if request.method == 'POST':
        seccion = request.POST.get('seccion', '')

        # ── Sección: Datos de la empresa ─────────────────────────────────
        if seccion == 'empresa':
            if emisor is None:
                messages.error(request, 'No hay un emisor configurado. Usa el asistente de configuración inicial.')
                return redirect('configuracion_empresa')

            emisor.nit                  = request.POST.get('nit', emisor.nit).strip()
            emisor.nrc                  = request.POST.get('nrc', '').strip() or None
            emisor.nombre_razon_social  = request.POST.get('nombre_razon_social', emisor.nombre_razon_social).strip()
            emisor.nombre_comercial     = request.POST.get('nombre_comercial', '').strip() or None
            emisor.nombre_establecimiento = request.POST.get('nombre_establecimiento', '').strip() or None
            emisor.direccion_comercial  = request.POST.get('direccion_comercial', '').strip()
            emisor.telefono             = request.POST.get('telefono', '').strip() or None
            emisor.email                = request.POST.get('email', '').strip() or None
            emisor.codigo_establecimiento = request.POST.get('codigo_establecimiento', '').strip() or None
            emisor.codigo_punto_venta   = request.POST.get('codigo_punto_venta', '').strip() or None
            emisor.tipoContribuyente    = request.POST.get('tipoContribuyente', emisor.tipoContribuyente)
            emisor.imprime_termica      = request.POST.get('imprime_termica') == 'on'
            emisor.es_restaurante       = request.POST.get('es_restaurante') == 'on'

            ambiente_id = request.POST.get('ambiente')
            if ambiente_id:
                try:
                    emisor.ambiente = Ambiente.objects.get(pk=ambiente_id)
                except Ambiente.DoesNotExist:
                    pass

            municipio_id = request.POST.get('municipio')
            if municipio_id:
                try:
                    emisor.municipio = Municipio.objects.get(pk=municipio_id)
                except Municipio.DoesNotExist:
                    pass

            if request.FILES.get('logo'):
                emisor.logo = request.FILES['logo']

            emisor.save()
            messages.success(request, 'Datos de la empresa actualizados.')
            logger.info('Emisor_fe actualizado por %s', request.user)

        # ── Secciones de ConfiguracionServidor ───────────────────────────
        elif seccion in GRUPOS_CONFIG:
            grupo = GRUPOS_CONFIG[seccion]
            for clave, _, campo_principal, _ in grupo['claves']:
                valor       = request.POST.get(f'{clave}__valor', '').strip()
                url         = request.POST.get(f'{clave}__url', '').strip()
                url_endpoint = request.POST.get(f'{clave}__url_endpoint', '').strip()
                contraseña  = request.POST.get(f'{clave}__contraseña', '').strip()
                descripcion = request.POST.get(f'{clave}__descripcion', '').strip()

                obj = config.get(clave)
                if obj:
                    obj.valor        = valor
                    obj.url          = url
                    obj.url_endpoint = url_endpoint
                    if contraseña:
                        obj.contraseña = contraseña
                    obj.descripcion  = descripcion
                    obj.save()
                else:
                    ConfiguracionServidor.objects.create(
                        clave=clave, valor=valor, url=url,
                        url_endpoint=url_endpoint, contraseña=contraseña,
                        descripcion=descripcion,
                    )
                    config = _get_config()

            messages.success(request, f'Sección "{grupo["titulo"]}" guardada.')
            logger.info('ConfiguracionServidor [%s] actualizado por %s', seccion, request.user)

        return redirect('configuracion_empresa')

    # ── GET ──────────────────────────────────────────────────────────────
    context = {
        'emisor':       emisor,
        'config':       config,
        'grupos':       GRUPOS_CONFIG,
        'ambientes':    Ambiente.objects.all(),
        'municipios':   Municipio.objects.select_related('departamento').order_by('departamento__nombre', 'nombre'),
        'tipos_doc':    TiposDocIDReceptor.objects.all(),
        'tipos_estab':  TiposEstablecimientos.objects.all(),
    }
    return render(request, 'autenticacion/configuracion_empresa.html', context)
