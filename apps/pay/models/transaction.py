from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime

from django.conf import settings
from decimal import Decimal


from apps.pay.models.productos import Productos
from apps.authentication.models import CustomerUser

@dataclass
class TransactionDto:
    customer_user: int
    discount_id: int
    discount_value: float
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


class Discount(models.Model):
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    verification_code=models.CharField(max_length=60,unique=True)
    social_media = models.CharField(max_length=60, blank=True)
    initial_date=models.DateField()
    final_date=models.DateField()
    discount_type=models.CharField(max_length=10,choices=[('price', 'Price Value'), ('percentage', 'Pecentage Value')],default="percentage")
    discount_rate=models.DecimalField(max_digits=5, decimal_places=2)
    status=models.BooleanField(default=True)
    # Agrega una relación con el modelo de productos
    product_id = models.ForeignKey(Productos, on_delete=models.CASCADE, default=1)

    def es_valido(self):
        """
        Verifica si el cupón de descuento es válido en la fecha actual.
        """

        # Verificar el estado del cupón
        if not self.status:
            return False

        #Verificar que monto no supere el 100%
        if self.discount_type == 'percentage' and self.discount_rate > 100:
            return False


        # ESTE CUPÓN SOLO ES VÁLIDO PARA LA HORA BOLIVIANA
        # SE OBTIENE LA HORA GLOBAL Y SE RESTA 4 HORAS PORQUE BOLIVIA
        # ESTÁ EN GMT-4
        fecha_actual = timezone.now().date() - timedelta(hours=4)
        
        # Verificar si la fecha actual está dentro del rango de inicio y finalización
        if self.initial_date <= fecha_actual <= self.final_date:
            return True
        else:
            return False
        
    def calculate_discount_value(self, amount):
        """
        Calcula el valor de descuento aplicado al monto dado, según el tipo y tasa de descuento.
        """
        if self.discount_type == 'percentage':
            discount_rate = self.discount_rate / 100  # Convertir el porcentaje a decimal
            return amount * discount_rate
        elif self.discount_type == 'price':
            return min(amount, self.discount_rate)
        else:
            return 0  # Tipo de descuento no válido
    

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
    documentoComprador = models.CharField(max_length=15, blank=True, null=True)
    modalidad = models.CharField(max_length=100 )
    extra1 = models.CharField(max_length=300, blank=True, null=True)
    extra2 = models.CharField(max_length=300, blank=True, null=True)
    extra3 = models.CharField(max_length=300, blank=True, null=True)
    direccionComprador = models.CharField(max_length=300, blank=False, null=False)
    ciudad = models.CharField(max_length=300,  )
    codigoTransaccion = models.CharField(max_length=300, blank=False, null=False,  unique=True)
    urlRespuesta = models.CharField(max_length=300, blank=False, null=False)

    correo = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=20, blank=False, null=False)

    discount_id = models.ForeignKey(Discount, on_delete=models.SET_NULL,blank=True, null=True )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def discount_type(self):
        if self.discount_id:
            return self.discount_id.discount_type
        return None