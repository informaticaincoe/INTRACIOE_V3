# Generated by Django 5.1.3 on 2025-03-12 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0059_tributo_porcentaje_tributo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tributo',
            old_name='porcentaje_tributo',
            new_name='valor_tributo',
        ),
    ]
