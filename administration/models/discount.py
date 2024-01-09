from django.db import models

class Discount(models.Model):
    verification_code=models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    discount_rate=models.DecimalField(max_digits=5, decimal_places=2)
    initial_date=models.DateField()
    final_date=models.DateField()

