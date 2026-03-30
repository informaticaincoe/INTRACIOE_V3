from django.db import migrations


FUNCIONALIDADES = [
    # ── Ventas ──
    ('ventas.inicio',       'Inicio Ventas',     'ventas',       'bi-house-door-fill'),
    ('ventas.clientes',     'Clientes',          'ventas',       'bi-people'),
    ('ventas.ventas',       'Ventas',            'ventas',       'bi-cart-check'),
    ('ventas.catalogo',     'Catálogo',          'ventas',       'bi-journal-bookmark-fill'),
    ('ventas.devoluciones', 'Devoluciones',      'ventas',       'bi-arrow-return-left'),
    ('ventas.reportes',     'Reportes',          'ventas',       'bi-clipboard-data'),
    # ── Compras ──
    ('compras.inicio',      'Inicio Compras',    'compras',      'bi-house-door-fill'),
    ('compras.compras',     'Compras',           'compras',      'bi-calculator'),
    ('compras.proveedores', 'Proveedores',       'compras',      'bi-people'),
    ('compras.reportes',    'Reporte',           'compras',      'bi-bar-chart-line'),
    # ── Facturación ──
    ('facturacion.inicio',        'Inicio Facturación',   'facturacion', 'bi-house-door-fill'),
    ('facturacion.generar',       'Generar Facturas',     'facturacion', 'bi-file-earmark-plus'),
    ('facturacion.correcciones',  'Generar Correcciones', 'facturacion', 'bi-pencil-square'),
    ('facturacion.listado',       'Listado de Facturas',  'facturacion', 'bi-journal-text'),
    ('facturacion.sujeto_excluido','Sujeto Excluido',     'facturacion', 'bi-person-x'),
    ('facturacion.contingencias', 'Contingencias',        'facturacion', 'bi-exclamation-triangle'),
    ('facturacion.consolidar',    'Consolidar del mes',   'facturacion', 'bi-calendar-check'),
    # ── Inventario ──
    ('inventario.inicio',   'Inicio Inventario',    'inventario',  'bi-house-door-fill'),
    ('inventario.gestion',  'Gestión',              'inventario',  'bi-arrow-left-right'),
    ('inventario.ajuste',   'Ajuste de Inventario', 'inventario',  'bi-sliders'),
    ('inventario.productos','Productos',            'inventario',  'bi-box-seam'),
    ('inventario.servicios','Servicios',            'inventario',  'bi-tools'),
    # ── Contabilidad ──
    ('contabilidad.cuentas',     'Plan de Cuentas',          'contabilidad', 'bi-journal-text'),
    ('contabilidad.asientos',    'Asientos Contables',       'contabilidad', 'bi-journal-bookmark'),
    ('contabilidad.cxc',         'Cuentas por Cobrar',       'contabilidad', 'bi-arrow-down-circle'),
    ('contabilidad.cxp',         'Cuentas por Pagar',        'contabilidad', 'bi-arrow-up-circle'),
    ('contabilidad.libro_mayor', 'Libro Mayor',              'contabilidad', 'bi-book'),
    ('contabilidad.balance_comp','Balance de Comprobación',  'contabilidad', 'bi-clipboard-data'),
    ('contabilidad.balance_gen', 'Balance General',          'contabilidad', 'bi-bar-chart-line'),
    ('contabilidad.estado_res',  'Estado de Resultados',     'contabilidad', 'bi-graph-up'),
    ('contabilidad.anexos',      'Reportes de Anexos',       'contabilidad', 'bi-file-earmark-spreadsheet'),
    # ── Restaurante ──
    ('restaurante.caja',        'Caja',              'restaurante', 'bi-cash-stack'),
    ('restaurante.cajeros',     'Cajeros',           'restaurante', 'bi-person-badge'),
    ('restaurante.billetes',    'Billetes y monedas','restaurante', 'bi-cash-coin'),
    ('restaurante.cocina',      'Cocina / Comandas', 'restaurante', 'bi-fire'),
    ('restaurante.cocineros',   'Cocineros',         'restaurante', 'bi-person-fill'),
    ('restaurante.areas_cocina','Áreas de cocina',   'restaurante', 'bi-map'),
    ('restaurante.meseros',     'Meseros',           'restaurante', 'bi-person-workspace'),
    ('restaurante.mesas',       'Mesas',             'restaurante', 'bi-grid-3x3-gap'),
    ('restaurante.asignaciones','Asignación de mesas','restaurante','bi-arrow-left-right'),
    ('restaurante.categorias',  'Categorías menú',   'restaurante', 'bi-tag'),
    ('restaurante.menu',        'Menú',              'restaurante', 'bi-egg-fried'),
    ('restaurante.areas',       'Áreas',             'restaurante', 'bi-diagram-3'),
]


def cargar(apps, schema_editor):
    Funcionalidad = apps.get_model('AUTENTICACION', 'Funcionalidad')
    Plan = apps.get_model('AUTENTICACION', 'Plan')

    # Crear funcionalidades
    funcionalidades_por_modulo = {}
    for clave, nombre, modulo, icono in FUNCIONALIDADES:
        f, _ = Funcionalidad.objects.get_or_create(
            clave=clave,
            defaults={'nombre': nombre, 'modulo': modulo, 'icono': icono},
        )
        funcionalidades_por_modulo.setdefault(modulo, []).append(f)

    # Asignar funcionalidades a planes existentes según sus módulos activos
    MODULO_CAMPO = {
        'ventas': 'tiene_ventas',
        'compras': 'tiene_compras',
        'facturacion': 'tiene_facturacion',
        'inventario': 'tiene_inventario',
        'contabilidad': 'tiene_contabilidad',
        'rrhh': 'tiene_rrhh',
        'restaurante': 'tiene_restaurante',
    }
    for plan in Plan.objects.all():
        for modulo, campo in MODULO_CAMPO.items():
            if getattr(plan, campo, False):
                for func in funcionalidades_por_modulo.get(modulo, []):
                    plan.funcionalidades.add(func)


def revertir(apps, schema_editor):
    Funcionalidad = apps.get_model('AUTENTICACION', 'Funcionalidad')
    Funcionalidad.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('AUTENTICACION', '0009_funcionalidad_y_plan_m2m'),
    ]

    operations = [
        migrations.RunPython(cargar, revertir),
    ]
