# Generated by Django 5.1.3 on 2025-03-13 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('INVENTARIO', '0006_tipounidadmedida_alter_producto_unidad_medida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='descuento',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='tiene_descuento',
        ),
        migrations.DeleteModel(
            name='Descuento',
        ),
    ]
