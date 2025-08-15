# Middleware para desactivar CSRF en métodos PUT (solo desarrollo)
class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.method == 'PUT':
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)

# Permitir CSRF en desarrollo para localhost y 127.0.0.1
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Opcional: para APIs y desarrollo, puedes desactivar la verificación CSRF en SessionAuthentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}
import os
from pathlib import Path

from conf_fire_base import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-xj(nht#rwob#jz#8z&jpv(a5%(kw#16!9q)79#+rzt2+hau@-x'

DEBUG = True
ALLOWED_HOSTS = ['api.linkey.digital', 'linkey.digital', '*']

INSTALLED_APPS = [
    'django.contrib.sites',  # Necesario para allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Proveedores sociales que quieras (ejemplo: Google, Facebook)
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.authentication',
    'apps.administration',
    'apps.profile',
    'apps.contact',
    'apps.pay',
    'apps.mercado_pago',
    'apps.booking',
    'apps.client_contact',
    'apps.ecommerce',
    'soyyo_api',
    'dj_rest_auth',


]

AUTH_USER_MODEL = 'authentication.CustomerUser'

MIDDLEWARE = [
'common.middleware.DisableCSRFMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linkbhxz_linkey',
        'USER': 'linkbhxz_postgres',
        'PASSWORD': 'mhYPQV0G97lo',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#FORCE_SCRIPT_NAME = '/backend'



# Permitir solicitudes desde frontend local
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://api.linkey.digital",
    "https://www.api.linkey.digital",
    "https://www.linkey.digital",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False

# Configuración de cookies de sesión para desarrollo
SESSION_COOKIE_HTTPONLY = False  # Permitir acceso desde JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Permitir cookies cross-site en desarrollo
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)



EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

EMAIL_USE_SSL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # O 'mandatory' si quieres forzar verificación

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'