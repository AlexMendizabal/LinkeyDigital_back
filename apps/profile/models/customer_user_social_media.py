from dataclasses import dataclass

from django.core.validators import MinValueValidator
from django.db import models

from apps.profile.models import SocialMedia
from django.conf import settings


@dataclass
class SocialMediaDto:
    customer_user: int
    social_media: int
    url_complete: str
    is_active: bool
    is_visible: bool
    


class CustomerUserSocialMedia(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    url_complete = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])
