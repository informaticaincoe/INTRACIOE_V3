from django import forms

class MeseroLoginForm(forms.Form):
    codigo = forms.CharField(max_length=20, label="Código de mesero")

class CocineroLoginForm(forms.Form):
    pin = forms.CharField(
        label="PIN",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su PIN"})
    )