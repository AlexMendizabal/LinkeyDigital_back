from dataclasses import dataclass
from django.core.validators import MinValueValidator
from django.db import models
from datetime import time

from authentication.models import CustomerUser


@dataclass
class ConfigurationBookingDto:
    customer_user : int
    max_personas : int
    time_bet_booking : int
    holiday : str
    hora_inicio : str
    hora_fin : str
    status_conf : int
    kids : bool
    teen : bool

class ConfigurationBooking(models.Model):

    customer_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    max_personas = models.IntegerField(default= 20,  blank = True, validators=[MinValueValidator(0)])
    time_bet_booking = models.IntegerField(blank = True, validators=[MinValueValidator(0)])
    holiday = models.CharField(max_length=100, blank=True)
    hora_inicio = models.TimeField(default=time(7, 0, 0))
    hora_fin = models.TimeField(default=time(18, 0, 0))
    status_conf = models.IntegerField(default = 1, validators=[MinValueValidator(0)])
    kids = models.BooleanField(default=False)
    teen = models.BooleanField(default=False)





