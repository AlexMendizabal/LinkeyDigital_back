from datetime import date
from django.db import models



class Currencies(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    currencies = models.CharField(max_length=20)
    triliteral_symbols = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)




