import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import CustomerUser

API_URL = "http://localhost:8000/api/auth/password/reset/"

usuarios = CustomerUser.objects.filter(is_active=True, email__isnull=False).exclude(email='').filter(password__isnull=True) | CustomerUser.objects.filter(password='')

for user in usuarios:
    data = {"email": user.email}
    try:
        response = requests.post(API_URL, data=data)
        print(f"Enviado a: {user.email} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error enviando a {user.email}: {e}")