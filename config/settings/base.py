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
    'apps.authentication',
    'apps.administration',
    'apps.profile',
    'apps.contact',
    'apps.pay',
    'apps.mercado_pago',
    'apps.booking',
    'apps.client_contact',
    'apps.ecommerce',


]

AUTH_USER_MODEL = 'authentication.CustomerUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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


CORS_ALLOWED_ORIGINS = [
    "https://api.linkey.digital",
    "https://www.api.linkey.digital",
    "https://www.linkey.digital",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True

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