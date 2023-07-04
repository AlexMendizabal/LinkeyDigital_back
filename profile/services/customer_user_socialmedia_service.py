import os

from rest_framework.generics import get_object_or_404

from profile.models import CustomerUserSocialMedia, CustomerUserCustomSocialMedia
from django.conf import settings


class SocialMediaService:
    def create_or_update_social_media(self, dto):
        customer_user_social_media, created = CustomerUserSocialMedia.objects.update_or_create(
            customer_user=dto.customer_user, social_media=dto.social_media)
        customer_user_social_media.url_complete = dto.url_complete
        customer_user_social_media.is_active = dto.is_active
        customer_user_social_media.is_visible = dto.is_visible
        customer_user_social_media.save()
        return customer_user_social_media

    def get_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_social_media = get_object_or_404(CustomerUserSocialMedia, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_social_media = CustomerUserSocialMedia.objects.all().filter(customer_user_id=customer_user)
        else:
            customer_user_social_media = CustomerUserSocialMedia.objects.all()
        return customer_user_social_media

    def create_custom_social_media(self, dto):
        customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.create(
            customer_user=dto.customer_user, url=dto.url, title=dto.title, is_active=dto.is_active,
            is_visible=dto.is_visible, type=dto.type, image=dto.image)
        return customer_user_custom_social_media

    def get_custom_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, pk=pk,
                                                                  customer_user=customer_user)
        elif customer_user:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().filter(
                customer_user_id=customer_user)
        else:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all()
        return customer_user_custom_social_media

    def delete_custom_social_media(self, pk=None, customer_user=None):
        # esta parte queda censurada *******************
        # customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.filter(id=pk,
        #                                                                                  customer_user_id=customer_user).delete()
        # return customer_user_custom_social_media
        #*******************************************
    
        # busca el objeto y si lo encuentra lo borra 
        cusm = get_object_or_404(CustomerUserCustomSocialMedia, id=pk, customer_user_id=customer_user)
        if cusm.type=="socialmedia" and cusm.image != "custom_social_media/undefined.png":
            try:
                os.remove(cusm.image.path)
            except Exception as e:
                pass
        if cusm.type=="image" :
            try:
                if not cusm.url.endswith("custom_social_media/undefined.png") and not cusm.url.startswith("http"):
                    os.remove(os.path.normpath(os.path.join(settings.MEDIA_ROOT, cusm.url.replace(settings.MEDIA_URL, ''))))
            except Exception as e:
                pass
        # Borra el objeto de la base de datos
        cusm.delete()
