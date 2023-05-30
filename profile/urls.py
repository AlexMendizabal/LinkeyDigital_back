from django.urls import path, include
from rest_framework import routers

from profile.views import CustomerUserProfileViewSet, CustomerUserWhatsappViewSet, CustomerUserReservaViewSet,\
    CustomerUserEmailViewSet, CustomerUserMapViewSet, CustomerUserPhoneViewSet, CustomerUserSocialMediaViewSet, CustomerUserImageViewSet, \
    CustomerUserCustomSocialMediaViewSet, CustomerUserStatistics, DesignProfileViewSet, SocialmediaViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('user', CustomerUserProfileViewSet.as_view(), name="customer_user_profile_get_or_create_or_update"),
    path('user/<int:pk>', CustomerUserProfileViewSet.as_view(), name="customer_user_profile_get_one"),

    path('whatsapp', CustomerUserWhatsappViewSet.as_view(), name="customer_user_whatsapp_get_or_create_or_update"),
    path('whatsapp/<int:pk>', CustomerUserWhatsappViewSet.as_view(), name="customer_user_whatsapp_get_one"),

    path('email', CustomerUserEmailViewSet.as_view(), name="customer_user_email_get_or_create_or_update"),
    path('email/<int:pk>', CustomerUserEmailViewSet.as_view(), name="customer_user_email_get_one"),

    path('map', CustomerUserMapViewSet.as_view(), name="customer_user_map_get_or_create_or_update"),
    path('map/<int:pk>', CustomerUserMapViewSet.as_view(), name="customer_user_map_get_one"),

    path('phone', CustomerUserPhoneViewSet.as_view(), name="customer_user_phone_get_or_create_or_update"),
    path('phone/<int:pk>', CustomerUserPhoneViewSet.as_view(), name="customer_user_phone_get_one"),

    path('social_media', CustomerUserSocialMediaViewSet.as_view(),
         name="customer_user_social_media_get_or_create_or_update"),
    path('social_media/<int:pk>', CustomerUserSocialMediaViewSet.as_view(), name="customer_user_social_media_get_one"),

    path('custom_social_media', CustomerUserCustomSocialMediaViewSet.as_view(),
         name="customer_user_custom_social_media_get_or_create"),
    path('custom_social_media/<int:pk>', CustomerUserCustomSocialMediaViewSet.as_view(),
         name="customer_user_custom_social_media_get_one_or_update_or_delete"),

    path('base_social_media', SocialmediaViewSet.as_view(), name="socialmedia_list"),
    path('base_social_media/<int:pk>', SocialmediaViewSet.as_view(), name="socialmedia_get"),

    path('base_design_profile', DesignProfileViewSet.as_view(), name="design_profile_list"),
    path('base_design_profile/<int:pk>', DesignProfileViewSet.as_view(), name="design_profile_get"),

    path('statistics', CustomerUserStatistics.as_view(),
         name="get_customer_user_statistics"),

     path('image', CustomerUserImageViewSet.as_view(), name="customer_user_image_get_or_create_or_update"),
    path('image/<int:pk>', CustomerUserImageViewSet.as_view(), name="customer_user_whatsapp_get_one"),

    path('reserva/<int:social>', CustomerUserReservaViewSet.as_view(),  name="get_reserva"),
]
