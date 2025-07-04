from django import forms
from .models import Departamentos, Cargo, Empleados, Boleta_pago

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamentos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class BoletaPagoForm(forms.ModelForm):
    class Meta:
        model = Boleta_pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BoletaPagoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Seleccione el archivo .xlsx")

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

class UploadFileFormEmpleados(forms.Form):
    file  = forms.FileField(label="Seleccione el archivo .xlsx")

    def  __init__(self, *args, **kwargs):
        super(UploadFileFormEmpleados, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

