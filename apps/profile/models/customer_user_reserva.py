from dataclasses import dataclass
from datetime import date
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profile.models import CustomerUserCustomSocialMedia
from django.conf import settings


@dataclass
class ReservaDto:
    custome_user_social_media: int
    date: date
    adults: int
    kids: int
    Nombre: str
    Email: str
    phone: str


class CustomerUserReserva(models.Model):

    adults = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kids = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date = models.DateTimeField()
    custome_user_social_media = models.ForeignKey(CustomerUserCustomSocialMedia, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    Nombre = models.CharField(max_length=50, blank=True)
    Email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)