from dataclasses import dataclass
from PIL import Image
from django.core.validators import MinValueValidator
from django.db import models

from soyyo_api import settings


@dataclass
class CustomSocialMediaDto:
    customer_user: int
    title: str
    url: str
    is_active: bool
    is_visible: bool
    type : str
    image: str


class CustomerUserCustomSocialMedia(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to="custom_social_media", blank='', default="custom_social_media/undefined.png")
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    type = models.CharField(max_length=50, blank=True, default='socialMedia')

#FIXME: DA ERROR AL CREARLO POR LA IMG
    def save(self, **kwargs):
        super().save()
        #FIXME: Da error, self.image esta nulo pero 
        if(self.image):
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.image.path)
