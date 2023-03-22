from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from profile.models import CustomerUserWhatsapp, CustomerUserEmail, CustomerUserMap, CustomerUserPhone, \
    CustomerUserProfile, CustomerUserSocialMedia, CustomerUserCustomSocialMedia


class PublicCustomerUserService:

    def get_profile(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)
        else:
            customer_user_profile = CustomerUserProfile.objects.all()
        new_counter_value = customer_user_profile.counter + 1
        CustomerUserProfile.objects.filter(pk=customer_user_profile.pk).update(counter=new_counter_value)
        return customer_user_profile

    def get_whatsapp(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_whatsapp = get_object_or_404(CustomerUserWhatsapp, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_whatsapp = get_object_or_404(CustomerUserWhatsapp, customer_user_id=customer_user,
                                                       is_visible=True)
        else:
            customer_user_whatsapp = CustomerUserWhatsapp.objects.all()
        return customer_user_whatsapp

    def get_email(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_email = get_object_or_404(CustomerUserEmail, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_email = get_object_or_404(CustomerUserEmail, customer_user=customer_user, is_visible=True)
        else:
            customer_user_email = CustomerUserEmail.objects.all()
        return customer_user_email

    def get_map(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_map = get_object_or_404(CustomerUserMap, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_map = get_object_or_404(CustomerUserMap, customer_user_id=customer_user, is_visible=True)
        else:
            customer_user_map = CustomerUserMap.objects.all()
        return customer_user_map

    def get_phone(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_phone = get_object_or_404(CustomerUserPhone, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_phone = get_object_or_404(CustomerUserPhone, customer_user_id=customer_user, is_visible=True)
        else:
            customer_user_phone = CustomerUserPhone.objects.all()
        return customer_user_phone

    def get_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_social_media = get_object_or_404(CustomerUserSocialMedia, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_social_media = CustomerUserSocialMedia.objects.all().filter(customer_user_id=customer_user,
                                                                                      is_visible=True)
        else:
            customer_user_social_media = CustomerUserSocialMedia.objects.all()
        return customer_user_social_media

    def get_custom_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, pk=pk,
                                                                  customer_user=customer_user)
        elif customer_user:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().filter(
                customer_user_id=customer_user, is_visible=True)
        else:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all()
        return customer_user_custom_social_media

