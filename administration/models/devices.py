from datetime import date

from django.db import models


class Devices(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    device_type = models.CharField(max_length=50)
    device_specifications = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
