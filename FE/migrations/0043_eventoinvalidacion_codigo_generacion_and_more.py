# Generated by Django 5.1.3 on 2025-03-07 17:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0042_emisor_fe_tipo_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoinvalidacion',
            name='codigo_generacion',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='eventoinvalidacion',
            name='fecha_anulacion',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='eventoinvalidacion',
            name='hora_anulacion',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='eventoinvalidacion',
            name='solicita_invalidacion',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='eventoinvalidacion',
            name='codigo_generacion_r',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='eventoinvalidacion',
            name='nombre_solicita',
            field=models.CharField(max_length=255, null=True, verbose_name='Nombre o Razón Social'),
        ),
    ]
