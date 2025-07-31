from datetime import date
from django.db import models

from administration.models import Currencies


class Subscription(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    subscription = models.CharField(max_length=50, null=False)
    monetary_value = models.FloatField()
    currencies = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    days_validity = models.IntegerField()
    is_active = models.BooleanField(default=True)
