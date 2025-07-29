import os
import sys

# Agrega el path del proyecto Django
sys.path.insert(0, '/home/linkbhxz/api.linkey.digital')

# Define el módulo de configuración
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soyyo_api.settings")

# Lanza la aplicación
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
