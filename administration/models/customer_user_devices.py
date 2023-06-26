from datetime import date
from django.db import models

from administration.models.devices import Devices
#from authentication.models import CustomerUser


class CustomerUserDevices(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    # TODO Relacion entre Usuario y Dispositivo
    #customer_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    url_linked = models.CharField(max_length=50)
    name = models.CharField(max_length=50)