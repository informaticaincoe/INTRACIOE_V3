# Generated by Django 5.1.3 on 2025-02-11 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0020_receptor_fe_tipo_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptor_fe',
            name='tipo_documento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FE.tiposdocidreceptor'),
        ),
    ]
