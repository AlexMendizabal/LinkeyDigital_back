import uuid
from enum import unique

from django.contrib.auth.models import AbstractUser
from django.db import models

from soyyo_api import settings


class CustomerUser(AbstractUser):
    # Id administrado por el orm
    password = models.CharField("password", max_length=128, null=True, blank=True)
    uid = models.CharField(max_length=100, blank=False, unique=True)
    public_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    customer_user_admin = models.ForeignKey('self', null=True, blank=True, related_name='owner',
                                            on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.CharField(max_length=100, blank=False, unique=True)
    phone_number = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    paternal_surname = models.CharField(max_length=100, blank=True)
    maternal_surname = models.CharField(max_length=100, blank=True)
    birth_genre = models.CharField(max_length=100, blank=True)
    identification_genre = models.CharField(max_length=100, blank=True)
