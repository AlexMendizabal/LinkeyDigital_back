from datetime import date
from django.db import models

from administration.models import Customer, Subscription


class CustomerSubscription(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
