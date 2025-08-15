import sys
sys.path.append('c:/xampp/htdocs/LinkeyDigital_back')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.authentication.models.customer_user import CustomerUser

# Obtenemos el usuario existente
username = input("Ingresa el nombre de usuario del superusuario que necesitas corregir: ")
try:
    user = CustomerUser.objects.get(username=username)
    
    # Aseguramos que todos los permisos estén activados
    user.is_superuser = True
    user.is_staff = True
    user.is_admin = True
    user.is_sales_manager = True
    user.is_active = True
    
    # Opcional: Activar otros permisos según necesidades
    user.is_sponsor = True
    user.is_booking = True
    user.is_ecommerce = True
    
    # Guardar cambios
    user.save()
    
    print(f"¡Éxito! El usuario {username} ahora tiene todos los permisos necesarios.")
    print(f"Permisos actualizados:")
    print(f"- is_superuser: {user.is_superuser}")
    print(f"- is_staff: {user.is_staff}")
    print(f"- is_admin: {user.is_admin}")
    print(f"- is_sales_manager: {user.is_sales_manager}")
    print(f"- is_sponsor: {user.is_sponsor}")
    print(f"- is_booking: {user.is_booking}")
    print(f"- is_ecommerce: {user.is_ecommerce}")
    
except CustomerUser.DoesNotExist:
    print(f"Error: No se encontró un usuario con el nombre '{username}'")
except Exception as e:
    print(f"Error inesperado: {str(e)}")
