from django.db import models


class DesignProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=50)
    is_active = models.BooleanField()

