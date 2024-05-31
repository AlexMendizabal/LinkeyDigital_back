from django.db import models
from authentication.models import CustomerUser


class Button(models.Model):
    customer_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    button_title = models.CharField(max_length=45)
    url = models.URLField(max_length=120)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer_user.username} - {self.title}'
