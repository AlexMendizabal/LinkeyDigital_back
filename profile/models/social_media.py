from datetime import date
from django.db import models


class SocialMedia(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    url_base = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank='', default="base_social_media/undefined.png")
    is_active = models.BooleanField()
