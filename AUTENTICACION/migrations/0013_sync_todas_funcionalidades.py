"""
Sincroniza todas las funcionalidades que se crearon via scripts.
Garantiza que existan en cualquier entorno (producción, staging, etc).
"""
from django.db import migrations

TODAS = [
    # Sistema
    ('sistema.dashboard',       'Dashboard',                'sistema',      'bi-speedometer2'),
    ('sistema.config_empresa',  'Configurar empresa',       'sistema',      'bi-gear'),
    ('sistema.usuarios',        'Gestión de usuarios',      'sistema',      'bi-people'),
    # Ventas
    ('ventas.inicio',           'Inicio Ventas',            'ventas',       'bi-house-door-fill'),
    ('ventas.clientes',         'Clientes',                 'ventas',       'bi-people'),
    ('ventas.ventas',           'Ventas',                   'ventas',       'bi-cart-check'),
    ('ventas.catalogo',         'Catálogo',                 'ventas',       'bi-journal-bookmark-fill'),
    ('ventas.devoluciones',     'Devoluciones',             'ventas',       'bi-arrow-return-left'),
    ('ventas.reportes',         'Reportes',                 'ventas',       'bi-clipboard-data'),
    ('ventas.rep_periodo',      'Reporte ventas por período','ventas',      'bi-calendar-range'),
    ('ventas.rep_clientes',     'Reporte top clientes',     'ventas',       'bi-people'),
    ('ventas.rep_productos',    'Reporte productos vendidos','ventas',      'bi-box-seam'),
    ('ventas.rep_tipo_doc',     'Reporte por tipo documento','ventas',      'bi-file-earmark-bar-graph'),
    ('ventas.rep_devoluciones', 'Reporte devoluciones',     'ventas',       'bi-arrow-return-left'),
    # Compras
    ('compras.inicio',          'Inicio Compras',           'compras',      'bi-house-door-fill'),
    ('compras.compras',         'Compras',                  'compras',      'bi-calculator'),
    ('compras.proveedores',     'Proveedores',              'compras',      'bi-people'),
    ('compras.reportes',        'Reporte',                  'compras',      'bi-bar-chart-line'),
    ('compras.rep_periodo',     'Reporte compras por período','compras',    'bi-calendar-range'),
    ('compras.rep_proveedor',   'Reporte por proveedor',    'compras',      'bi-people'),
    ('compras.rep_productos',   'Reporte productos comprados','compras',    'bi-box-seam'),
    ('compras.rep_cxp',         'Reporte cuentas por pagar','compras',      'bi-exclamation-triangle'),
    ('compras.rep_comparativo', 'Reporte comparativo',      'compras',      'bi-arrow-left-right'),
    # Facturación
    ('facturacion.inicio',              'Inicio Facturación',       'facturacion', 'bi-house-door-fill'),
    ('facturacion.generar',             'Generar DTE',              'facturacion', 'bi-file-earmark-plus'),
    ('facturacion.correcciones',        'Generar Correcciones',     'facturacion', 'bi-pencil-square'),
    ('facturacion.listado',             'Listado de Facturas',      'facturacion', 'bi-journal-text'),
    ('facturacion.sujeto_excluido',     'Sujeto Excluido',         'facturacion', 'bi-person-x'),
    ('facturacion.contingencias',       'Contingencias',            'facturacion', 'bi-exclamation-triangle'),
    ('facturacion.consolidar',          'Consolidar del mes',       'facturacion', 'bi-calendar-check'),
    ('facturacion.dte_01',              'DTE 01 - Factura',         'facturacion', 'bi-file-earmark-text'),
    ('facturacion.dte_03',              'DTE 03 - Crédito Fiscal',  'facturacion', 'bi-receipt'),
    ('facturacion.dte_04',              'DTE 04 - Nota de Remisión','facturacion', 'bi-truck'),
    ('facturacion.dte_05',              'DTE 05 - Nota de Crédito', 'facturacion', 'bi-file-earmark-minus'),
    ('facturacion.dte_06',              'DTE 06 - Nota de Débito',  'facturacion', 'bi-file-earmark-plus'),
    ('facturacion.dte_11',              'DTE 11 - Exportación',     'facturacion', 'bi-globe2'),
    ('facturacion.dte_14',              'DTE 14 - Sujeto Excluido', 'facturacion', 'bi-person-x'),
    ('facturacion.rep_libro_ccf',       'Libro ventas CCF',         'facturacion', 'bi-journal-text'),
    ('facturacion.rep_libro_cf',        'Libro ventas consumidor',  'facturacion', 'bi-journal-bookmark'),
    ('facturacion.rep_resumen_dte',     'Resumen por tipo DTE',     'facturacion', 'bi-pie-chart'),
    ('facturacion.rep_anulados',        'Documentos anulados',      'facturacion', 'bi-x-octagon'),
    ('facturacion.rep_retenciones',     'Retenciones IVA/Renta',    'facturacion', 'bi-percent'),
    # Inventario
    ('inventario.inicio',           'Inicio Inventario',        'inventario',  'bi-house-door-fill'),
    ('inventario.gestion',          'Gestión',                  'inventario',  'bi-arrow-left-right'),
    ('inventario.ajuste',           'Ajuste de Inventario',     'inventario',  'bi-sliders'),
    ('inventario.productos',        'Productos',                'inventario',  'bi-box-seam'),
    ('inventario.servicios',        'Servicios',                'inventario',  'bi-tools'),
    ('inventario.rep_kardex',       'Kardex por producto',      'inventario',  'bi-card-list'),
    ('inventario.rep_valorizado',   'Inventario valorizado',    'inventario',  'bi-currency-dollar'),
    ('inventario.rep_bajo_stock',   'Bajo stock mínimo',        'inventario',  'bi-exclamation-triangle'),
    ('inventario.rep_sin_movimiento','Sin movimiento',          'inventario',  'bi-pause-circle'),
    ('inventario.rep_movimientos',  'Movimientos por período',  'inventario',  'bi-arrow-left-right'),
    # Contabilidad
    ('contabilidad.cuentas',            'Plan de Cuentas',              'contabilidad', 'bi-journal-text'),
    ('contabilidad.asientos',           'Asientos Contables',           'contabilidad', 'bi-journal-bookmark'),
    ('contabilidad.cxc',                'Cuentas por Cobrar',           'contabilidad', 'bi-arrow-down-circle'),
    ('contabilidad.cxp',                'Cuentas por Pagar',            'contabilidad', 'bi-arrow-up-circle'),
    ('contabilidad.libro_mayor',        'Libro Mayor',                  'contabilidad', 'bi-book'),
    ('contabilidad.balance_comp',       'Balance de Comprobación',      'contabilidad', 'bi-clipboard-data'),
    ('contabilidad.balance_gen',        'Balance General',              'contabilidad', 'bi-bar-chart-line'),
    ('contabilidad.estado_res',         'Estado de Resultados',         'contabilidad', 'bi-graph-up'),
    ('contabilidad.anexos',             'Reportes de Anexos',           'contabilidad', 'bi-file-earmark-spreadsheet'),
    ('contabilidad.rep_flujo',          'Flujo de efectivo',            'contabilidad', 'bi-cash-stack'),
    ('contabilidad.rep_cxc',            'Antigüedad saldos CxC',       'contabilidad', 'bi-arrow-down-circle'),
    ('contabilidad.rep_cxp',            'Antigüedad saldos CxP',       'contabilidad', 'bi-arrow-up-circle'),
    ('contabilidad.rep_retenciones',    'Retenciones IVA/Renta',       'contabilidad', 'bi-percent'),
    ('contabilidad.rep_conciliacion',   'Conciliación bancaria',       'contabilidad', 'bi-bank'),
    # Restaurante
    ('restaurante.caja',            'Caja',                 'restaurante', 'bi-cash-stack'),
    ('restaurante.cajeros',         'Cajeros',              'restaurante', 'bi-person-badge'),
    ('restaurante.billetes',        'Billetes y monedas',   'restaurante', 'bi-cash-coin'),
    ('restaurante.cocina',          'Cocina / Comandas',    'restaurante', 'bi-fire'),
    ('restaurante.cocineros',       'Cocineros',            'restaurante', 'bi-person-fill'),
    ('restaurante.areas_cocina',    'Áreas de cocina',      'restaurante', 'bi-map'),
    ('restaurante.meseros',         'Meseros',              'restaurante', 'bi-person-workspace'),
    ('restaurante.mesas',           'Mesas',                'restaurante', 'bi-grid-3x3-gap'),
    ('restaurante.asignaciones',    'Asignación de mesas',  'restaurante', 'bi-arrow-left-right'),
    ('restaurante.categorias',      'Categorías menú',      'restaurante', 'bi-tag'),
    ('restaurante.menu',            'Menú',                 'restaurante', 'bi-egg-fried'),
    ('restaurante.areas',           'Áreas',                'restaurante', 'bi-diagram-3'),
    ('restaurante.rep_ventas_mesa', 'Ventas por mesa',      'restaurante', 'bi-grid-3x3-gap'),
    ('restaurante.rep_platillos',   'Platillos vendidos',   'restaurante', 'bi-egg-fried'),
    ('restaurante.rep_caja',        'Reporte de caja',      'restaurante', 'bi-cash-stack'),
    ('restaurante.rep_meseros',     'Ventas por mesero',    'restaurante', 'bi-person-workspace'),
    ('restaurante.rep_comandas',    'Comandas por área',    'restaurante', 'bi-fire'),
]

MODULO_CAMPO = {
    'sistema': None,
    'ventas': 'tiene_ventas',
    'compras': 'tiene_compras',
    'facturacion': 'tiene_facturacion',
    'inventario': 'tiene_inventario',
    'contabilidad': 'tiene_contabilidad',
    'rrhh': 'tiene_rrhh',
    'restaurante': 'tiene_restaurante',
}


def cargar(apps, schema_editor):
    Funcionalidad = apps.get_model('AUTENTICACION', 'Funcionalidad')
    Plan = apps.get_model('AUTENTICACION', 'Plan')

    funcionalidades_por_modulo = {}
    for clave, nombre, modulo, icono in TODAS:
        f, _ = Funcionalidad.objects.get_or_create(
            clave=clave,
            defaults={'nombre': nombre, 'modulo': modulo, 'icono': icono},
        )
        funcionalidades_por_modulo.setdefault(modulo, []).append(f)

    # Asignar a planes según módulos activos
    for plan in Plan.objects.all():
        for modulo, campo in MODULO_CAMPO.items():
            if campo is None:
                # Sistema: asignar a todos
                for func in funcionalidades_por_modulo.get(modulo, []):
                    plan.funcionalidades.add(func)
            elif getattr(plan, campo, False):
                for func in funcionalidades_por_modulo.get(modulo, []):
                    plan.funcionalidades.add(func)


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('AUTENTICACION', '0012_funcionalidades_sistema'),
    ]

    operations = [
        migrations.RunPython(cargar, revertir),
    ]
