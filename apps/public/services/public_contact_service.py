from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from apps.profile.models import CustomerUserWhatsapp, CustomerUserEmail, CustomerUserMap, CustomerUserPhone, \
    CustomerUserProfile, CustomerUserSocialMedia, CustomerUserCustomSocialMedia


class PublicContactservices:

    def visit_whatsapp(self, customer_user=None):
        if customer_user:
            customer_user_whatsapp = get_object_or_404(CustomerUserWhatsapp, customer_user_id=customer_user,
                                                       is_visible=True)
            new_counter_value = customer_user_whatsapp.counter + 1
            CustomerUserWhatsapp.objects.filter(pk=customer_user_whatsapp.pk, is_visible=True).update(
                counter=new_counter_value)
            return customer_user_whatsapp

    def visit_email(self, customer_user=None):
        if customer_user:
            customer_user_email = get_object_or_404(CustomerUserEmail, customer_user=customer_user, is_visible=True)
            new_counter_value = customer_user_email.counter + 1
            CustomerUserEmail.objects.filter(pk=customer_user_email.pk, is_visible=True).update(counter=new_counter_value)
            return customer_user_email

    def visit_map(self, customer_user=None):
        if customer_user:
            customer_user_map = get_object_or_404(CustomerUserMap, customer_user_id=customer_user, is_visible=True)
            new_counter_value = customer_user_map.counter + 1
            CustomerUserMap.objects.filter(pk=customer_user_map.pk, is_visible=True).update(counter=new_counter_value)
            return customer_user_map

    def visit_phone(self, customer_user=None):
        if customer_user:
            customer_user_phone = get_object_or_404(CustomerUserPhone, customer_user_id=customer_user, is_visible=True)
            new_counter_value = customer_user_phone.counter + 1
            CustomerUserPhone.objects.filter(pk=customer_user_phone.pk, is_visible=True).update(counter=new_counter_value)
            return customer_user_phone

