# Generated by Django 5.1.3 on 2025-02-19 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0026_remove_detallefactura_unidad_medida'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefactura',
            name='unidad_medida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FE.tipounidadmedida'),
        ),
    ]
