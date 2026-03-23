from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .api_views import LoginAPIView, ChangePasswordAPIView
from .serializers import LoginSerializer, ChangePasswordSerializer
from .models import PasswordResetCode

User = get_user_model()


# ---------------------------------------------------------------------------
# Modelo User
# ---------------------------------------------------------------------------

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='admin'
        )

    def test_rol_admin(self):
        self.assertTrue(self.user.is_admin)
        self.assertFalse(self.user.is_vendedor)

    def test_rol_vendedor(self):
        user = User.objects.create_user(username='vendedor1', password='pass1234', role='vendedor')
        self.assertTrue(user.is_vendedor)
        self.assertFalse(user.is_admin)

    def test_rol_default_es_cliente(self):
        user = User.objects.create_user(username='cliente1', password='pass1234')
        self.assertEqual(user.role, 'cliente')

    def test_roles_mesero_cocinero_cajero(self):
        for rol in ('mesero', 'cocinero', 'cajero'):
            u = User.objects.create_user(username=f'u_{rol}', password='pass1234', role=rol)
            self.assertEqual(u.role, rol)


# ---------------------------------------------------------------------------
# Serializer de Login
# ---------------------------------------------------------------------------

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser', password='securepass123', role='admin'
        )

    def test_login_valido(self):
        s = LoginSerializer(data={'username': 'loginuser', 'password': 'securepass123'})
        self.assertTrue(s.is_valid(), s.errors)
        self.assertEqual(s.validated_data['user'], self.user)

    def test_password_incorrecta(self):
        s = LoginSerializer(data={'username': 'loginuser', 'password': 'wrong'})
        self.assertFalse(s.is_valid())
        self.assertIn('non_field_errors', s.errors)

    def test_usuario_inexistente(self):
        s = LoginSerializer(data={'username': 'noexiste', 'password': 'cualquier'})
        self.assertFalse(s.is_valid())

    def test_usuario_inactivo(self):
        self.user.is_active = False
        self.user.save()
        s = LoginSerializer(data={'username': 'loginuser', 'password': 'securepass123'})
        self.assertFalse(s.is_valid())


# ---------------------------------------------------------------------------
# API View: Login
# ---------------------------------------------------------------------------

class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='apiuser', password='securepass123', role='admin'
        )
        self.view = LoginAPIView.as_view()

    def test_login_exitoso_retorna_token(self):
        request = self.factory.post('/login/', {
            'username': 'apiuser', 'password': 'securepass123'
        }, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_credenciales_invalidas(self):
        request = self.factory.post('/login/', {
            'username': 'apiuser', 'password': 'incorrecta'
        }, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_login_sin_datos(self):
        request = self.factory.post('/login/', {}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)


# ---------------------------------------------------------------------------
# API View: Cambio de contraseña
# ---------------------------------------------------------------------------

class ChangePasswordAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='pwduser', password='oldpassword123', role='admin'
        )
        self.view = ChangePasswordAPIView.as_view()

    def test_cambio_exitoso(self):
        request = self.factory.post('/change-password/', {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword456'
        }, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword456'))

    def test_password_antigua_incorrecta(self):
        request = self.factory.post('/change-password/', {
            'old_password': 'incorrecta',
            'new_password': 'newpassword456'
        }, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_requiere_autenticacion(self):
        request = self.factory.post('/change-password/', {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword456'
        }, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 401)


# ---------------------------------------------------------------------------
# Vistas de template: CRUD usuarios (con validación)
# ---------------------------------------------------------------------------

class UsuariosViewValidacionTest(TestCase):
    def setUp(self):
        self.client = Client(raise_request_exception=False)
        self.admin = User.objects.create_user(
            username='admin', password='adminpass123', role='admin',
            is_staff=True, is_superuser=True
        )
        self.client.login(username='admin', password='adminpass123')

    def test_crear_usuario_valido(self):
        response = self.client.post('/autentications/usuarios/crear/', {
            'username': 'nuevousuario',
            'password': 'securepass123',
            'role': 'vendedor',
        })
        # Debe redirigir (302) si fue exitoso
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevousuario').exists())

    def test_crear_usuario_sin_username_no_crea(self):
        self.client.post('/autentications/usuarios/crear/', {
            'username': '',
            'password': 'securepass123',
            'role': 'vendedor',
        })
        # No debe crear ningún usuario sin username
        self.assertFalse(User.objects.filter(username='').exists())

    def test_crear_usuario_password_corta_no_crea(self):
        self.client.post('/autentications/usuarios/crear/', {
            'username': 'usuarionuevo',
            'password': 'corta',
            'role': 'vendedor',
        })
        self.assertFalse(User.objects.filter(username='usuarionuevo').exists())

    def test_crear_usuario_duplicado_no_crea_segundo(self):
        User.objects.create_user(username='existente', password='pass12345')
        self.client.post('/autentications/usuarios/crear/', {
            'username': 'existente',
            'password': 'otropass123',
            'role': 'cliente',
        })
        self.assertEqual(User.objects.filter(username='existente').count(), 1)

    def test_editar_usuario_con_username_vacio_no_guarda(self):
        user = User.objects.create_user(username='parateditar', password='pass12345')
        original_username = user.username
        self.client.post(f'/autentications/usuarios/{user.pk}/editar/', {
            'username': '',
            'role': 'vendedor',
        })
        user.refresh_from_db()
        self.assertEqual(user.username, original_username)

    def test_lista_usuarios_requiere_login(self):
        self.client.logout()
        response = self.client.get('/autentications/usuarios/')
        self.assertIn(response.status_code, [302, 403])


# ---------------------------------------------------------------------------
# Modelo PasswordResetCode
# ---------------------------------------------------------------------------

class PasswordResetCodeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='resetuser', password='pass12345')

    def test_crear_codigo_reset(self):
        code = PasswordResetCode.objects.create(user=self.user, code='123456')
        self.assertFalse(code.used)
        self.assertEqual(code.code, '123456')

    def test_marcar_codigo_usado(self):
        code = PasswordResetCode.objects.create(user=self.user, code='654321')
        code.used = True
        code.save()
        code.refresh_from_db()
        self.assertTrue(code.used)
