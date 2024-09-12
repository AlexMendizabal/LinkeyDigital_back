from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models

from soyyo_api import settings
from decimal import Decimal


@dataclass
class ProductosDto:
    title : str
    description : str
    price : Decimal
    image : str

class Productos(models.Model):
    STATUS_CHOICES = [
        (0, 'Available'),
        (1, 'Unavailable'),
    ]
    
    TYPE_CHOICES = [
        ('tarjeta', 'tarjeta'),
        ('accesorio', 'accesorio'),
    ]

    title = models.CharField(max_length=50, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="productos_images", blank=True, default="productos_images/undefined.png") 
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    type = models.CharField(max_length=60, choices=TYPE_CHOICES, blank=True, default="tarjeta")
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        from pay.services.productServices import assign_order 
        assign_order(self)
        super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
