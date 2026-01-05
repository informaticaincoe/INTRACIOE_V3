from django import forms

class MeseroLoginForm(forms.Form):
    codigo = forms.CharField(max_length=20, label="Código de mesero")
