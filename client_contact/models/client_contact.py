from dataclasses import dataclass

from django.core.validators import MinValueValidator

from django.db import models

from soyyo_api import settings
from authentication.models import CustomerUser
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    # Expresión regular para validar un número de teléfono
    pattern = r'^\+?\d{1,3}?\s?\d{3,}$'
    if not re.match(pattern, value):
        raise ValidationError("El número de teléfono ingresado no es válido")
def validate_comment(value):
    # Aquí implementa tu lógica de validación
    if "malicious_code" in value:
        raise ValidationError("Error de contenido")

class Register(models.Model):
    customer_user_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=60) 
    country_code = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True, validators=[validate_phone_number])
    email = models.EmailField(max_length=254, null=True)
    comment = models.TextField(max_length=280, null=True, validators=[validate_comment])
    created_at = models.DateTimeField(auto_now_add=True)
