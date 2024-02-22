from dataclasses import dataclass
from datetime import date
import string
import secrets
import random

from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import CustomerUser


@dataclass
class BookingDto:
    adults: int
    kids: int
    teen: int
    date: date
    nombre: str
    email: str
    phone: str
    customer_user: int


class Booking(models.Model):

    adults = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kids = models.IntegerField(blank = True, default=0, validators=[MinValueValidator(0)])
    teen = models.IntegerField(blank = True,default=0, validators=[MinValueValidator(0)])
    date = models.DateTimeField()
    customer_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    status_booking = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        # Genera un código único de 5 dígitos
        unique_code = ''.join(random.choices(string.digits, k=5))
        self.code = unique_code
        super().save(*args, **kwargs)
