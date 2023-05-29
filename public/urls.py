from django.urls import path, include
from rest_framework import routers

from public.views import PublicCustomerUserViewSet, PublicCustomerUserEmailViewSet, PublicCustomerUserPhoneViewSet, CustomerUserReservaViewSet, \
    PublicCustomerUserWhatsappViewSet, PublicCustomerUserMapViewSet, PublicCustomerUserSocialMediaViewSet, \
    PublicCustomerUserCustomSocialMediaViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('user/<str:param>', PublicCustomerUserViewSet.as_view(), name="get_user_public_app"),

    path('user/<str:public_id>/email', PublicCustomerUserEmailViewSet.as_view(), name="visit_email_public_app"),
    path('user/<str:public_id>/phone', PublicCustomerUserPhoneViewSet.as_view(), name="visit_phone_public_app"),
    path('user/<str:public_id>/whatsapp', PublicCustomerUserWhatsappViewSet.as_view(),
         name="visit_whatsapp_public_app"),
    path('user/<str:public_id>/map', PublicCustomerUserMapViewSet.as_view(), name="visit_map_public_app"),
    path('user/<str:public_id>/social_media', PublicCustomerUserSocialMediaViewSet.as_view(),
         name="visit_social_media_public_app"),
    path('user/<str:public_id>/custom_social_media', PublicCustomerUserCustomSocialMediaViewSet.as_view(),
         name="visit_custom_social_media_public_app"),

     path('user/<str:public_id>/reserva', CustomerUserReservaViewSet.as_view(), name="make_reserva"),

]
