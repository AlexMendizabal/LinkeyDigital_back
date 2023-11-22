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


class Discount(models.Model):
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    verification_code=models.CharField(max_length=60,unique=True)
    social_media = models.CharField(max_length=60, blank=True)
    initial_date=models.DateField()
    final_date=models.DateField()
    discount_type=models.CharField(max_length=10,choices=[('price', 'Price Value'), ('percentage', 'Pecentage Value')],default="percentage")
    discount_rate=models.DecimalField(max_digits=5, decimal_places=2)
    status=models.BooleanField(default=True)
    
    def apply_discounts(self):
        """
        Aplica descuentos al precio del producto.
        """
        # Obtén todos los descuentos asociados al producto
        descuentos = self.discounts.all()

        # Calcula el precio final aplicando descuentos
        precio_final = self.price

        for descuento in descuentos:
            if descuento.discount_type == 'price':
                # Descuento en valor fijo
                precio_final -= descuento.discount_rate
            elif descuento.discount_type == 'percentage':
                # Descuento en porcentaje
                precio_final -= (precio_final * descuento.discount_rate)

        return max(precio_final, 0)  # Asegura que el precio final no sea negativo
    
 

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

    def save(self, *args, **kwargs):
    # If there is a discount_id, calculate the discount_value based on discount_type and discount_rate
        if self.discount_id:
            if self.discount_id.discount_type == 'percentage':
                discount_rate = self.discount_id.discount_rate / 100  # Convert percentage to decimal
                self.discount_value = self.monto * discount_rate
            elif self.discount_id.discount_type == 'price':
                self.discount_value = min(self.monto, self.discount_id.discount_rate)

            # Subtract the calculated discount_value from the monto
            self.monto -= self.discount_value

        super().save(*args, **kwargs)

    def discount_type(self):
        if self.discount_id:
            return self.discount_id.discount_type
        return None
