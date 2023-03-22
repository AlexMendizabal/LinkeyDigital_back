from django.urls import path, include
from rest_framework import routers

from public.views import PublicCustomerUserViewSet, PublicCustomerUserEmailViewSet, PublicCustomerUserPhoneViewSet, \
    PublicCustomerUserWhatsappViewSet, PublicCustomerUserMapViewSet, PublicCustomerUserSocialMediaViewSet, \
    PublicCustomerUserCustomSocialMediaViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('user/<str:username>', PublicCustomerUserViewSet.as_view(), name="get_user_public_app"),

    path('user/<str:username>/email', PublicCustomerUserEmailViewSet.as_view(), name="visit_email_public_app"),
    path('user/<str:username>/phone', PublicCustomerUserPhoneViewSet.as_view(), name="visit_phone_public_app"),
    path('user/<str:username>/whatsapp', PublicCustomerUserWhatsappViewSet.as_view(),
         name="visit_whatsapp_public_app"),
    path('user/<str:username>/map', PublicCustomerUserMapViewSet.as_view(), name="visit_map_public_app"),
    path('user/<str:username>/social_media', PublicCustomerUserSocialMediaViewSet.as_view(),
         name="visit_social_media_public_app"),
    path('user/<str:username>/custom_social_media', PublicCustomerUserCustomSocialMediaViewSet.as_view(),
         name="visit_custom_social_media_public_app"),

]
