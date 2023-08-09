from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models

from soyyo_api import settings
from decimal import Decimal


@dataclass
class TransactionDto:
    customer_user: int
    status: int
    canal : str
    monto : Decimal
    moneda : str
    descripcion : str
    nombreComprador : str
    apellidoComprador: str
    documentoComprador : str
    modalidad : str 
    extra1 : str
    extra2 : str
    extra3 : str
    direccionComprador : str
    ciudad : str
    codigoTransaccion : str
    urlRespuesta : str
    id_transaccion : int
    correo: str
    telefono: str

class Transaction(models.Model):
    #datos de soyYo
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    id_transaccion = models.CharField(max_length=300, blank=True, null=True,  unique=True)
    date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.IntegerField(default=0, validators=[MinValueValidator(0)], null=False)
    # datos requeridos para ScrumPay
    canal = models.CharField(max_length=10, blank=False, null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    moneda = models.CharField(max_length=10, blank=False, null=False)
    descripcion = models.CharField(max_length=300 )
    nombreComprador = models.CharField(max_length=100, blank=False, null=False)
    apellidoComprador = models.CharField(max_length=100, blank=False, null=False)
    documentoComprador = models.CharField(max_length=15, blank=False, null=False)
    modalidad = models.CharField(max_length=100 )
    extra1 = models.CharField(max_length=300, blank=True)
    extra2 = models.CharField(max_length=300, blank=True)
    extra3 = models.CharField(max_length=300, blank=True)
    direccionComprador = models.CharField(max_length=300, blank=False, null=False)
    ciudad = models.CharField(max_length=300,  )
    codigoTransaccion = models.CharField(max_length=300, blank=False, null=False,  unique=True)
    urlRespuesta = models.CharField(max_length=300, blank=False, null=False)

    correo = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=20, blank=False, null=False)


#Status del transaction
# 1 --> no_pago
# 2 --> pagada


