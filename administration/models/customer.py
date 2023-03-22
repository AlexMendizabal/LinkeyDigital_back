from datetime import date
from django.db import models

from administration.models import CustomerType


class Customer(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    customer_type = models.ForeignKey( CustomerType, on_delete=models.CASCADE)

