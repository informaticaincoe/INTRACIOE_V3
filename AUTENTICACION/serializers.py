from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import PasswordResetCode

User = get_user_model()

### SERIALIZER DE AUTENTICACION O LOGIN Y CAMBIO DE CONTRASEÑA

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo")
        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña antigua es incorrecta")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
# LOGOUT INVALIDAR TOKEN
class logoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        #borrar todos los tokens del usuario para orzar re-login
        Token.objects.filter(user=request.user).delete()
        return Response({"detail":"Sesion cerrada con exito"}, status=status.HTTP_200_OK)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe ningún usuario con ese email.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generar código aleatorio de 6 dígitos
        code = ''.join(random.choices(string.digits, k=6))

        # Marcar códigos anteriores como usados (opcional)
        PasswordResetCode.objects.filter(user=user, used=False).update(used=True)

        # Crear nuevo código
        reset_obj = PasswordResetCode.objects.create(user=user, code=code)

        # Enviar email
        send_mail(
            subject="Tu código de restablecimiento de contraseña",
            message=f"Hola {user.username},\n\nTu código para restablecer contraseña es: {code}\n\nEste código expirará en 10 minutos.",
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            recipient_list=[email],
        )
        return reset_obj

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Verificar usuario
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Email inválido.")

        # Verificar código
        try:
            reset_obj = PasswordResetCode.objects.get(
                user=user, code=data['code'], used=False
            )
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Código de confirmación inválido.")

        # Verificar expiración (p. ej. 10 minutos)
        if timezone.now() - reset_obj.created_at > timedelta(minutes=10):
            reset_obj.used = True
            reset_obj.save(update_fields=['used'])
            raise serializers.ValidationError("El código ha expirado.")

        data['user'] = user
        data['reset_obj'] = reset_obj
        return data

    def save(self):
        user = self.validated_data['user']
        reset_obj = self.validated_data['reset_obj']
        new_password = self.validated_data['new_password']

        # Cambiar la contraseña
        user.set_password(new_password)
        user.save()

        # Marcar el código como usado
        reset_obj.used = True
        reset_obj.save(update_fields=['used'])

        return user
