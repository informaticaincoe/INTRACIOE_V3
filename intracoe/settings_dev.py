"""
Settings para desarrollo local — sobreescribe settings.py.
Uso: python manage.py runserver --settings=intracoe.settings_dev
     o: export DJANGO_SETTINGS_MODULE=intracoe.settings_dev
"""
from .settings import *  # noqa: F401, F403

# Usar SQLite en local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_dev.sqlite3',
    }
}


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# No enviar emails reales en desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
