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

    title = models.CharField(max_length=50, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=300 )
    image = models.ImageField(upload_to="productos_images", blank='', default="productos_images/undefined.png") 
   





