from dataclasses import dataclass
from django.core.validators import MinValueValidator
from django.db import models

from pay.models import Productos, Transaction


@dataclass
class DetalleTransactionDto:
    producto : int
    transaction : int
    cantidad : int

class DetalleTransaction(models.Model):

    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])





