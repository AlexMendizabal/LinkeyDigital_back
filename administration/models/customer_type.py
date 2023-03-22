from datetime import date
from django.db import models


class CustomerType(models.Model):
    created_at = models.DateField(default=date.today)
    update_at = models.DateField(default=date.today)
    type = models.CharField(max_length=100, null=False)
