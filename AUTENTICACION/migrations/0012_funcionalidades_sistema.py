from django.db import migrations


FUNCIONALIDADES_SISTEMA = [
    ('sistema.dashboard',      'Dashboard',           'sistema', 'bi-speedometer2'),
    ('sistema.config_empresa', 'Configurar empresa',  'sistema', 'bi-gear'),
    ('sistema.usuarios',       'Gestión de usuarios', 'sistema', 'bi-people'),
]


def cargar(apps, schema_editor):
    Funcionalidad = apps.get_model('AUTENTICACION', 'Funcionalidad')
    Plan = apps.get_model('AUTENTICACION', 'Plan')

    nuevas = []
    for clave, nombre, modulo, icono in FUNCIONALIDADES_SISTEMA:
        f, _ = Funcionalidad.objects.get_or_create(
            clave=clave,
            defaults={'nombre': nombre, 'modulo': modulo, 'icono': icono},
        )
        nuevas.append(f)

    # Asignar funcionalidades de sistema a todos los planes existentes
    for plan in Plan.objects.all():
        for func in nuevas:
            plan.funcionalidades.add(func)


def revertir(apps, schema_editor):
    Funcionalidad = apps.get_model('AUTENTICACION', 'Funcionalidad')
    Funcionalidad.objects.filter(modulo='sistema').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('AUTENTICACION', '0011_rol_suscriptor'),
    ]

    operations = [
        migrations.RunPython(cargar, revertir),
    ]
