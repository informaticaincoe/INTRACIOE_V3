from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RESTAURANTE', '0024_alter_cuentapedido_options_alter_platillo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesa',
            name='propina_porcentaje',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=5,
                null=True,
                verbose_name='% Propina sugerida (deja vacío para usar el global)',
            ),
        ),
    ]
