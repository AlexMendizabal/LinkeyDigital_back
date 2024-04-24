from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import CustomerUser
from django.core.validators import MinValueValidator
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
    STATUS_CHOICES = [
        (0, 'No Leído'),
        (1, 'Leído'),
        # Puedes agregar más opciones según sea necesario
    ]

    customer_user_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=60) 
    country_code = models.CharField(max_length=6, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True, validators=[validate_phone_number])
    email = models.EmailField(max_length=254, null=True,blank=True)
    comment = models.TextField(max_length=280, null=True,blank=True, validators=[validate_comment])
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
