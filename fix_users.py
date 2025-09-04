import os
import django

# 🔹 Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 🔹 Buscar usuarios con password=None o vacío
for u in User.objects.all():
    if not u.password:
        print(f"Usuario corrupto: {u.email}")
        u.set_password("123456")  # ⚠️ contraseña temporal
        u.save()
        print(f"✅ Password reparado para {u.email}")
