import uuid
from enum import unique
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import AbstractUser
from django.db import models
#from simple_history.models import HistoricalRecords
from datetime import date, timedelta

from apps.administration.models import Licencia

class CustomerUser(AbstractUser):
    # Id administrado por el orm
    password = models.CharField("password", max_length=128, null=True, blank=True)
    uid = models.CharField(max_length=100, blank=False, unique=True, default=uuid.uuid4)
    public_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_sponsor=models.BooleanField(default=False)
    is_booking=models.BooleanField(default=False)
    is_sales_manager=models.BooleanField(default=False)
    is_ecommerce=models.BooleanField(default=False)

    dependency_id=models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True)

    customer_user_admin = models.ForeignKey('self', null=True, blank=True, related_name='owner',
                                            on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    is_editable = models.BooleanField(default=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.CharField(max_length=100, blank=False, unique=True)
    phone_number = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    birth_genre = models.CharField(max_length=100, blank=True)
    identification_genre = models.CharField(max_length=100, blank=True)
    rubro = models.CharField(max_length=100, blank=True)

    licencia_id = models.ForeignKey(Licencia, on_delete=models.SET_NULL, null=True)
    #history = HistoricalRecords()

# este metodo es para bloquar cuando el usuario ya no tenga acceso por falta de licencia
    def has_access_to_protected_views(self):
        # Verifica que la cuenta esté activa
        if self.is_superuser:
            return True
        if not self.is_active:
            return False

        # Obtiene la licencia asociada al usuario
        licencia = Licencia.objects.filter(id=self.licencia_id_id).first()
        if not licencia:
            return False

        # Verifica que la licencia no esté bloqueada
        if licencia.status == 3:
            return False

        # Verifica que la licencia sea eterna
        if licencia.status == 4:
            return True

        # Verifica que la licencia no esté vencida
        if licencia.status == 2:
            return False

        # Validación de fechas
        if not licencia.fecha_inicio or not licencia.duracion:
            return False

        fecha_inicio = licencia.fecha_inicio.date()
        duracion_dias = licencia.duracion
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        fecha_actual = date.today()

        # Bloquea licencias vencidas
        if fecha_actual > fecha_fin:
            licencia.status = 2
            licencia.save()
            return False

        # Bloquea otras licencias asociadas al mismo admin
        Licencia.objects.filter(customer_user_admin=self.customer_user_admin, status__in=[1, 2]).exclude(id=licencia.id).update(status=3)

        return True
