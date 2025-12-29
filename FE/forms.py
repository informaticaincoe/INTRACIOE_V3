from django import forms

from django_select2.forms import Select2MultipleWidget
from .models import ActividadEconomica, Emisor_fe, representanteEmisor

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


class RepresentanteEmisorForm(forms.ModelForm):
    class Meta:
        model = representanteEmisor
        fields = ["nombre", "tipo_documento", "numero_documento"]
        labels = {
            "nombre": "Nombre del representante",
            "tipo_documento": "Tipo de documento",
            "numero_documento": "Número de documento",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre completo"}),
            "tipo_documento": forms.Select(attrs={"class": "form-select"}),
            "numero_documento": forms.TextInput(attrs={"class": "form-control", "placeholder": "DUI/NIT"}),
        }

    def clean_numero_documento(self):
        num = (self.cleaned_data.get("numero_documento") or "").strip()
        if not num:
            raise forms.ValidationError("Debe indicar el número de documento.")
        # La unicidad ya la garantiza el modelo; permitimos el mismo si es el propio (en edición).
        qs = representanteEmisor.objects.filter(numero_documento__iexact=num)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un representante con ese número de documento.")
        return num


class EmisorForm(forms.ModelForm):
    actividades_economicas = forms.ModelMultipleChoiceField(
        queryset=ActividadEconomica.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "6"}),
        label="Actividades económicas"
    )

    class Meta:
        model = Emisor_fe
        fields = [
            "nit", "nrc", "nombre_razon_social", "actividades_economicas",
            "tipoestablecimiento", "nombre_comercial", "municipio",
            "direccion_comercial", "telefono", "email",
            "codigo_establecimiento", "codigo_punto_venta",
            "ambiente", "nombre_establecimiento",
            "tipo_documento", "logo",
            "clave_privada", "clave_publica",
            "imprime_termica", "imprime_termica",
        ]
        labels = {
            "nit": "NIT del Emisor",
            "nrc": "NRC",
            "nombre_razon_social": "Nombre o Razón social",
            "tipoestablecimiento": "Tipo de establecimiento",
            "municipio": "Municipio",
            "direccion_comercial": "Dirección comercial",
            "codigo_establecimiento": "Código de Establecimiento (MH)",
            "codigo_punto_venta": "Código de Punto de Venta (MH)",
            "ambiente": "Ambiente",
            "tipo_documento": "Tipo de documento (Emisor)",
            "logo": "Logo de la empresa",
            "clave_privada": "Contraseña/Clave privada (firmador)",
            "clave_publica": "Clave pública / Password Hacienda",
            "tipoContribuyente": "Tipo de Contribuyente",
        }
        widgets = {
            "nit": forms.TextInput(attrs={"class": "form-control"}),
            "nrc": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "tipoestablecimiento": forms.Select(attrs={"class": "form-select"}),
            "nombre_comercial": forms.TextInput(attrs={"class": "form-control"}),
            "municipio": forms.Select(attrs={"class": "form-select"}),
            "direccion_comercial": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "codigo_establecimiento": forms.TextInput(attrs={"class": "form-control"}),
            "codigo_punto_venta": forms.TextInput(attrs={"class": "form-control"}),
            "ambiente": forms.Select(attrs={"class": "form-select"}),
            "nombre_establecimiento": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_documento": forms.Select(attrs={"class": "form-select"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "clave_privada": forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
            "clave_publica": forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
            "tipoContribuyente": forms.Select(attrs={"class": "form-select"}),
            "imprime_termica": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        # Validaciones suaves de ejemplo:
        if not cleaned.get("nit"):
            self.add_error("nit", "El NIT es obligatorio.")
        if not cleaned.get("nombre_razon_social"):
            self.add_error("nombre_razon_social", "Debe indicar la razón social.")
        if not cleaned.get("ambiente"):
            self.add_error("ambiente", "Seleccione un ambiente.")

        return cleaned