from django import forms

from django_select2.forms import Select2MultipleWidget
from .models import Emisor_fe

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Archivo Excel')

class EmisorForm(forms.ModelForm):
    class Meta:
        model = Emisor_fe
        fields = [
            'nit',
            'nombre_razon_social',
            'direccion_comercial',
            'telefono',
            'email',
            'actividades_economicas',
            'codigo_establecimiento',
            'nombre_comercial'
        ]
        widgets = {
            'actividades_economicas': Select2MultipleWidget(
                attrs={'data-placeholder': 'Busca actividades...'}
            ),
        }

