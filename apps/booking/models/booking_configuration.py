from dataclasses import dataclass
from django.core.validators import MinValueValidator
from django.db import models
from datetime import time

from apps.authentication.models import CustomerUser


@dataclass
class ConfigurationBookingDto:
    customer_user : int
    max_personas : int
    max_reservas : int
    time_bet_booking : int
    holiday : str
    hora_inicio : str
    hora_fin : str
    hora_inicio_tarde : str
    hora_fin_tarde : str
    hora_inicio_noche : str
    hora_fin_noche : str
    status_conf : int
    kids : bool
    teen : bool
    btn : str
    phone : str
    email : str
    description : str
    title : str

class ConfigurationBooking(models.Model):

    customer_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    max_personas = models.IntegerField(default= 5,  blank = True, null=True, validators=[MinValueValidator(0)])
    max_reservas = models.IntegerField(default= 1,  blank = True, null=True, validators=[MinValueValidator(0)])
    time_bet_booking = models.IntegerField(default = 60, blank = True, validators=[MinValueValidator(0)])
    holiday = models.CharField(
        max_length=100, 
        blank=True, 
        default='[true,false,false,false,false,false,true]'
    )
    # hora mañana
    hora_inicio = models.TimeField(default=time(7, 0, 0), blank=True, null=True)
    hora_fin = models.TimeField(default=time(11, 0, 0), blank=True, null=True)
    # hora tarde
    hora_inicio_tarde = models.TimeField(default=time(15, 0, 0) , blank=True,null=True)
    hora_fin_tarde = models.TimeField(default=time(17, 0, 0) , blank=True,null=True)
    # hora noche
    hora_inicio_noche = models.TimeField(default=time(19, 0, 0), blank=True,null=True)
    hora_fin_noche = models.TimeField(default=time(19, 0, 0), blank=True,null=True)
    status_conf = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    kids = models.BooleanField(default=False)
    teen = models.BooleanField(default=False)

    title = models.CharField(max_length=30, default="Programar Reserva")
    btn = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)




