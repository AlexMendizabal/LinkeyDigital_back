import os
from pathlib import Path

import dj_database_url
from decouple import config

from conf_fire_base import DATABASES_CONF, BOLIVIA_MODE, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-xj(nht#rwob#jz#8z&jpv(a5%(kw#16!9q)79#+rzt2+hau@-x'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'authentication',
    'administration',
    'profile',
    'contact',
    'pay',
    'mercado_pago',
    'booking',
    'client_contact',
    'ecommerce',


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
]

ROOT_URLCONF = 'soyyo_api.urls'

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

WSGI_APPLICATION = 'soyyo_api.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'linkbhxz_linkey',
        'USER': 'linkbhxz_postgres',
        'PASSWORD': 'mhYPQV0G97lo',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/soyyo-services-django/staticfiles/'

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
        'authentication.authentication.FirebaseAuthentication',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True

ALLOWED_HOSTS = ['api.linkey.digital', 'linkey.digital', '*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

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
