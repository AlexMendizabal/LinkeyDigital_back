from datetime import date
from django.db import models
from django.core.validators import MinValueValidator

from profile.models import CustomerUserProfile


class ViewProfile(models.Model):
    custom_user = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])
