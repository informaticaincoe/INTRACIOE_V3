# Generated by Django 5.1.3 on 2025-03-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0052_eventoinvalidacion_recibido_mh_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoinvalidacion',
            name='tipo_documento_solicita',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
