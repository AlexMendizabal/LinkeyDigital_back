import os
import django

# Ajusta al path de tu settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password_default():
    email = "kenntjm12@gmail.com"
    new_password = "123456"

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        print(f"✅ Contraseña reseteada para {email}")
    except User.DoesNotExist:
        print(f"⚠️ No se encontró un usuario con el correo {email}")

if __name__ == "__main__":
    reset_password_default()
