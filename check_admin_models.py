import sys
sys.path.append('c:/xampp/htdocs/LinkeyDigital_back')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.apps import apps
from django.contrib.admin.sites import site

print('Modelos registrados en el admin:')
for model in site._registry:
    print(f'- {model.__name__} (app: {model._meta.app_label})')
