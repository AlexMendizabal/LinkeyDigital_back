# Scripts y Plantillas para la Migración Modular

## 1. Script Bash/Powershell para mover carpetas principales

### a) Powershell (Windows)

```powershell
# Crear carpetas principales
New-Item -ItemType Directory -Force -Path .\apps
New-Item -ItemType Directory -Force -Path .\config
New-Item -ItemType Directory -Force -Path .\common

# Mover apps existentes
Move-Item .\authentication .\apps\authentication
Move-Item .\profile .\apps\profile
Move-Item .\pay .\apps\pay
Move-Item .\public .\apps\public
Move-Item .\booking .\apps\booking
Move-Item .\client_contact .\apps\client_contact
Move-Item .\contact .\apps\contact
Move-Item .\ecommerce .\apps\ecommerce
Move-Item .\mercado_pago .\apps\mercado_pago
Move-Item .\administration .\apps\administration

# Mover settings y archivos de configuración
Move-Item .\soyyo_api\settings.py .\config\settings.py
Move-Item .\soyyo_api\urls.py .\config\urls.py
Move-Item .\soyyo_api\asgi.py .\config\asgi.py
Move-Item .\soyyo_api\wsgi.py .\config\wsgi.py

# (Opcional) Mover utilidades globales
# Move-Item .\UtilitiesAdministration.py .\common\UtilitiesAdministration.py
# Move-Item .\utilitiesPay.py .\common\utilitiesPay.py
```

### b) Bash (Linux/Mac)

```bash
# Crear carpetas principales
mkdir -p apps config common

# Mover apps existentes
mv authentication apps/
mv profile apps/
mv pay apps/
mv public apps/
mv booking apps/
mv client_contact apps/
mv contact apps/
mv ecommerce apps/
mv mercado_pago apps/
mv administration apps/

# Mover settings y archivos de configuración
mv soyyo_api/settings.py config/settings.py
mv soyyo_api/urls.py config/urls.py
mv soyyo_api/asgi.py config/asgi.py
mv soyyo_api/wsgi.py config/wsgi.py

# (Opcional) Mover utilidades globales
# mv UtilitiesAdministration.py common/
# mv utilitiesPay.py common/
```

---

## 2. Plantillas de Archivos Base

### a) apps/profile/models.py

```python
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # ...otros campos...

    def __str__(self):
        return self.user.username
```

### b) apps/profile/serializers.py

```python
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
```

### c) apps/profile/services.py

```python
def get_user_profile(user_id):
    from .models import UserProfile
    return UserProfile.objects.get(user_id=user_id)
```

### d) apps/profile/views.py

```python
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
```

### e) apps/profile/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## 3. Scripts Complementarios para la Migración

### a) Crear subcarpetas internas en cada app (Powershell)

```powershell
$apps = @('authentication','profile','pay','public','booking','client_contact','contact','ecommerce','mercado_pago','administration')
foreach ($app in $apps) {
    $base = ".\apps\$app"
    New-Item -ItemType Directory -Force -Path "$base\tests"
    New-Item -ItemType Directory -Force -Path "$base\migrations"
    if (-not (Test-Path "$base\__init__.py")) { New-Item -ItemType File -Path "$base\__init__.py" }
}
```

### b) Renombrar archivos a plural (Powershell)

```powershell
Get-ChildItem -Path .\apps -Recurse -File | Where-Object {
    $_.Name -eq 'serializer.py' -or $_.Name -eq 'service.py' -or $_.Name -eq 'test.py'
} | ForEach-Object {
    $newName = $_.Name -replace 'serializer','serializers' -replace 'service','services' -replace 'test','tests'
    Rename-Item $_.FullName $newName
}
```

### c) Actualizar imports en todos los archivos Python (Bash/Linux/Mac)

```bash
find apps/ -type f -name '*.py' -exec sed -i 's/from \(.*\)\.serializer/from \1.serializers/g' {} +
find apps/ -type f -name '*.py' -exec sed -i 's/from \(.*\)\.service/from \1.services/g' {} +
find apps/ -type f -name '*.py' -exec sed -i 's/from \(.*\)\.test/from \1.tests/g' {} +
```

### d) Crear archivos **init**.py donde falten (Bash/Linux/Mac)

```bash
find apps/ -type d -exec bash -c 'touch "$0/__init__.py"' {} \;
```

---

## 4. Plantilla de settings modular (config/settings/base.py)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps locales
    'apps.authentication',
    'apps.profile',
    'apps.pay',
    # ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ...
```

---

## 5. Estructura sugerida para common/

```
common/
    __init__.py
    utils.py
    permissions.py
    mixins.py
    i18n/
        __init__.py
        translation_helpers.py
```

---

Con estos scripts y plantillas puedes automatizar la mayor parte de la migración y estandarización. Recuerda revisar manualmente los cambios y probar el proyecto tras cada paso importante.
