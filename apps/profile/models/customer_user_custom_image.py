from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models

from django.conf import settings


@dataclass
class CustomImageDto:
    customer_user: int
    title: str
    is_active: bool
    is_visible: bool


class CustomerUserCustomImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="custom_social_media", blank='', default="custom_social_media/undefined.png")
    imageQR = models.ImageField(upload_to="custom_image", blank='', default="custom_social_media/undefined.png")
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.image.path)

        img_qr = Image.open(self.imageQR.path)
        if img_qr.height > 300 or img_qr.width > 300:
            new_img_qr = (200, 200)
            img_qr.thumbnail(new_img_qr)
            img_qr.save(self.imageQR.path)