from pathlib import Path
import os  # Necesario para manejar rutas
from decouple import config


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para Django (mantenela en secreto en producción)
SECRET_KEY = config('SECRET_KEY')


# Modo de desarrollo
DEBUG = True
ALLOWED_HOSTS = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuentas',  # Tu app personalizada
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Enrutador principal
ROOT_URLCONF = 'mi_proyecto.urls'

# Configuración de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'cuentas', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'mi_proyecto.wsgi.application'

# 🔧 Configuración de base de datos: SQL Server Express + autenticación de Windows
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'GourmetDB',
        'HOST': 'localhost\\SQLEXPRESS',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración regional
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'cuentas', 'static')]

# Campo automático por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL para login (si usás @login_required)
LOGIN_URL = '/login/'

AUTH_USER_MODEL = 'cuentas.CustomUser'
AUTHENTICATION_BACKENDS = ['cuentas.backend.EmailBackend']
