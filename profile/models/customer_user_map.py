from dataclasses import dataclass

from django.core.validators import MinValueValidator
from django.db import models

from soyyo_api import settings


@dataclass
class MapDto:
    customer_user: int
    longitude: str
    latitude: str
    is_active: bool
    is_visible: bool


class CustomerUserMap(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank='', default="contact/icon_ubicacion.png")
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])
