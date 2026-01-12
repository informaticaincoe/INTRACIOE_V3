# AUTENTICACION/forms.py
from django import forms
from .models import Perfilusuario, UsuarioEmisor
from FE.models import Emisor_fe  # ajusta app

class PerfilUsuarioForm(forms.ModelForm):
    emisor_activo = forms.ModelChoiceField(
        label="Emisor activo",
        queryset=Emisor_fe.objects.none(),
        required=False
    )

    class Meta:
        model = Perfilusuario
        fields = ("nombre", "apellido", "telefono", "direccion", "fecha_nacimiento", "emisor_activo")
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Emisores permitidos (activos) para este usuario
        qs = Emisor_fe.objects.filter(usuarios_rel__user=user, usuarios_rel__activo=True).distinct()
        # Si no hay vínculos, puedes decidir si mostrar todos los emisores a superuser
        if not qs.exists() and user and user.is_superuser:
            qs = Emisor_fe.objects.all()

        self.fields["emisor_activo"].queryset = qs
