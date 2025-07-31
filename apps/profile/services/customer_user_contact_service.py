from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from apps.profile.models import CustomerUserWhatsapp, CustomerUserEmail, CustomerUserMap, CustomerUserPhone


class Contactservices:

    def create_or_update_whatsapp(self, dto):
        customer_user_whatsapp, created = CustomerUserWhatsapp.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_whatsapp.phone_number = dto.phone_number
        customer_user_whatsapp.message = dto.message
        customer_user_whatsapp.is_active = dto.is_active
        customer_user_whatsapp.is_visible = dto.is_visible
        customer_user_whatsapp.save()
        return customer_user_whatsapp

    def get_whatsapp(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_whatsapp = get_object_or_404(CustomerUserWhatsapp, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_whatsapp = get_object_or_404(CustomerUserWhatsapp, customer_user_id=customer_user)
        else:
            customer_user_whatsapp = CustomerUserWhatsapp.objects.all()
        return customer_user_whatsapp

    def create_or_update_email(self, dto):
        customer_user_email, created = CustomerUserEmail.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_email.email = dto.email
        customer_user_email.subject = dto.subject
        customer_user_email.body = dto.body
        customer_user_email.is_active = dto.is_active
        customer_user_email.is_visible = dto.is_visible
        customer_user_email.save()
        return customer_user_email

    def get_email(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_email = get_object_or_404(CustomerUserEmail, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_email = get_object_or_404(CustomerUserEmail, customer_user=customer_user)
        else:
            customer_user_email = CustomerUserEmail.objects.all()
        return customer_user_email

    def create_or_update_map(self, dto):
        customer_user_map, created = CustomerUserMap.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_map.longitude = dto.longitude
        customer_user_map.latitude = dto.latitude
        customer_user_map.is_active = dto.is_active
        customer_user_map.is_visible = dto.is_visible
        customer_user_map.save()
        return customer_user_map

    def get_map(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_map = get_object_or_404(CustomerUserMap, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_map = get_object_or_404(CustomerUserMap, customer_user_id=customer_user)
        else:
            customer_user_map = CustomerUserMap.objects.all()
        return customer_user_map

    def create_or_update_phone(self, dto):
        customer_user_phone, created = CustomerUserPhone.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_phone.phone = dto.phone
        customer_user_phone.is_active = dto.is_active
        customer_user_phone.is_visible = dto.is_visible
        customer_user_phone.save()
        return customer_user_phone

    def get_phone(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_phone = get_object_or_404(CustomerUserPhone, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_phone = get_object_or_404(CustomerUserPhone, customer_user_id=customer_user)
        else:
            customer_user_phone = CustomerUserPhone.objects.all()
        return customer_user_phone
