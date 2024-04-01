from dataclasses import dataclass
from rest_framework.generics import get_object_or_404
from datetime import date

from profile.models import CustomerUserWhatsapp, CustomerUserEmail, CustomerUserMap, CustomerUserCustomImage, CustomerUserPhone, \
    CustomerUserProfile, CustomerUserSocialMedia, CustomerUserCustomSocialMedia, ViewProfile


class PublicCustomerUserService:


    def get_profile(self, pk=None, customer_user=None):
        print("pk:", pk)
        print("customer_user:", customer_user)

        if pk and customer_user:
            # Obtener el perfil de usuario asociado directamente con el usuario consultado
            customer_user_profile = get_object_or_404(CustomerUserProfile, pk=pk, customer_user=customer_user)
        elif customer_user:
            # Obtener el perfil de usuario asociado directamente con el usuario consultado
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)

            today = date.today()
            new_counter_value = customer_user_profile.counter + 1
            print("new_counter_value:", new_counter_value)
            print("Valor de pk en la consulta de actualización:", customer_user_profile.pk, customer_user)

            # Actualizar el contador solo para el perfil del usuario consultado
            CustomerUserProfile.objects.filter(pk=customer_user_profile.pk).update(counter=new_counter_value)
            
            view_profile, created = ViewProfile.objects.get_or_create(custom_user=customer_user_profile, timestamp__date=today)
            view_profile.counter += 1

            print("Usuario para el cual se incrementa el contador:", customer_user_profile.customer_user)
            print("view_profile:", view_profile)
            print("view_profile_counter:", view_profile.counter)
            
            view_profile.save()
            return customer_user_profile


    """ def get_profile(self, pk=None, customer_user=None):

        print("pk:", pk)
        print("customer_user:", customer_user)
        if pk and customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)
        # No tiene sentido... se borrara con el tiempo 
        # else:
        #     customer_user_profile = CustomerUserProfile.objects.all()
        today = date.today()
        new_counter_value = customer_user_profile.counter + 1
        print("new_counter_value:", new_counter_value)
        print("Valor de pk en la consulta de actualización:", customer_user_profile.pk, customer_user)
        CustomerUserProfile.objects.filter(pk=customer_user_profile.pk).update(counter=new_counter_value)
        view_profile, created = ViewProfile.objects.get_or_create(custom_user = customer_user_profile,timestamp__date=today)
        view_profile.counter += 1
        
        print("view_profile:", view_profile)
        print("view_profile_counter:", view_profile.counter)
        
        view_profile.save()
        return customer_user_profile """
        

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
                                                                                      is_visible=True).order_by('id')
        else:
            customer_user_social_media = CustomerUserSocialMedia.objects.all().order_by('id')
        return customer_user_social_media

    def get_custom_social_media(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, pk=pk,
                                                                  customer_user=customer_user)
        elif customer_user:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().filter(
                customer_user_id=customer_user).order_by('id')
        else:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().order_by('id')
        return customer_user_custom_social_media
    
    def get_custom_social_media_only_true(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, pk=pk,
                                                                  customer_user=customer_user)
        elif customer_user:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().filter(
                customer_user_id=customer_user, is_visible=True).order_by('id')
        else:
            customer_user_custom_social_media = CustomerUserCustomSocialMedia.objects.all().order_by('id')
        return customer_user_custom_social_media
    
    def get_image(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_map = get_object_or_404(CustomerUserCustomImage, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_map = get_object_or_404(CustomerUserCustomImage, customer_user_id=customer_user, is_visible=True)
        else:
            customer_user_map = CustomerUserMap.objects.all()
        return customer_user_map

