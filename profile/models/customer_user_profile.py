from dataclasses import dataclass
from datetime import date
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from soyyo_api import settings


@dataclass
class ProfileDto:
    customer_user: int
    public_id: str
    career: str
    public_name: str
    description: str


class CustomerUserProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    customer_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    career = models.CharField(max_length=50, blank=True)
    public_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="profile", blank='', default="profile/icon_perfil.png")
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    background = models.ImageField(upload_to="background", blank='', default="background/image_background.png")
    color = models.CharField(max_length=7, default="#000000")

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        bg = Image.open(self.background.path)

        if img.height > 300 or img.width > 300:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.image.path)

        if bg.height > 1080 or bg.width > 1917:
            new_bg = (1917, 1080)
            bg.thumbnail(new_bg)
            bg.save(self.background.path)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomerUserProfile.objects.create(customer_user=instance)
