from pathlib import Path
import os
from decouple import config

# =============================
# CONFIGURACIÓN GENERAL
# =============================

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = []

# =============================
# APLICACIONES INSTALADAS
# =============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuentas',
    'django.contrib.humanize', 
]

# =============================
# MIDDLEWARE
# =============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================
# RUTEO
# =============================

ROOT_URLCONF = 'mi_proyecto.urls'

# =============================
# TEMPLATES
# =============================

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

# =============================
# WSGI
# =============================

WSGI_APPLICATION = 'mi_proyecto.wsgi.application'

# =============================
# BASE DE DATOS
# =============================

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'GourmetDB',
        'HOST': 'localhost\\SQLEXPRESS',
        'PORT': None,  # <- CORREGIDO
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}

# =============================
# VALIDACIÓN DE CONTRASEÑAS
# =============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================
# LOCALIZACIÓN
# =============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =============================
# ARCHIVOS ESTÁTICOS
# =============================

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'cuentas', 'static')]

# =============================
# CONFIG. AVANZADAS
# =============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
AUTH_USER_MODEL = 'cuentas.CustomUser'
AUTHENTICATION_BACKENDS = ['cuentas.backend.EmailBackend']
