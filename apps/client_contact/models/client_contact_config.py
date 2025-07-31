from django.db import models
from apps.authentication.models import CustomerUser

class Configuration(models.Model):
    customer_user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
    message = models.TextField(max_length=254, default="¿Desea iniciar contacto? Ingrese sus datos por favor")
    phone_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    comment_enabled = models.BooleanField(default=True)

    class Meta:
        # Establecer la restricción de que solo puede haber una configuración por usuario
        unique_together = ('customer_user',)

    def __str__(self):
        return f"Configuration for {self.customer_user}"
