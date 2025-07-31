from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from apps.profile.models import CustomerUserSocialMedia, CustomerUserCustomSocialMedia


class PublicSocialMediaservices:

    def visit_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_social_media = get_object_or_404(CustomerUserSocialMedia, pk=pk, customer_user=customer_user)
            new_counter_value = customer_user_social_media.counter + 1
            CustomerUserSocialMedia.objects.filter(pk=customer_user_social_media.pk, is_visible=True).update(
                counter=new_counter_value)
            return customer_user_social_media

    def visit_custom_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, pk=pk, customer_user=customer_user)
            new_counter_value = customer_user_custom_social_media.counter + 1
            CustomerUserCustomSocialMedia.objects.filter(pk=customer_user_custom_social_media.pk, is_visible=True).update(
                counter=new_counter_value)
            return customer_user_custom_social_media
