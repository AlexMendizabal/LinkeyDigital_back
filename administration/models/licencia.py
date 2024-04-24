from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from simple_history.models import HistoricalRecords
from datetime import datetime

from soyyo_api import settings


@dataclass
class LicenciaDto: 
    customer_user_admin: int
    tipo_de_plan: str
    fecha_inicio : datetime
    cobro: Decimal
    duracion : str
    status : str


class Licencia(models.Model):

    customer_user_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tipo_de_plan = models.CharField(max_length=50, blank=True)
    fecha_inicio = models.DateTimeField()
    cobro = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duracion = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    history = HistoricalRecords()
