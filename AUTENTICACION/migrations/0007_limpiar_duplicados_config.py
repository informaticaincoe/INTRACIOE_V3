"""Eliminar registros duplicados de ConfiguracionServidor antes de agregar unique."""
from django.db import migrations


def limpiar_duplicados(apps, schema_editor):
    Config = apps.get_model('AUTENTICACION', 'ConfiguracionServidor')
    from django.db.models import Count, Max

    dupes = (
        Config.objects.values('clave')
        .annotate(c=Count('id'), max_id=Max('id'))
        .filter(c__gt=1)
    )
    for d in dupes:
        Config.objects.filter(clave=d['clave']).exclude(id=d['max_id']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('AUTENTICACION', '0006_plan_suscripcion'),
    ]

    operations = [
        migrations.RunPython(limpiar_duplicados, migrations.RunPython.noop),
    ]
