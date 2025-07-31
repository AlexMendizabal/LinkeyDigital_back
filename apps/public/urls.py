from django.urls import path, include
from rest_framework import routers

from apps.public.views.public_customer_user_viewset import PublicCustomerUserViewSet
from apps.public.views.public_email_viewset import PublicCustomerUserEmailViewSet
from apps.public.views.public_phone_viewset import PublicCustomerUserPhoneViewSet
from apps.public.views.public_whatsapp_viewset import PublicCustomerUserWhatsappViewSet
from apps.public.views.public_map_viewset import PublicCustomerUserMapViewSet
from apps.public.views.public_social_media_viewset import PublicCustomerUserSocialMediaViewSet
from apps.public.views.public_custom_social_media import PublicCustomerUserCustomSocialMediaViewSet
from apps.public.views.public_reserva_viewset import CustomerUserReservaViewSet

router = routers.DefaultRouter()

urlpatterns = [
    #README: Ahora treaera el usaurio admin relacionado del que solicita 
    path('user/<str:public_id>', PublicCustomerUserViewSet.as_view(), name="get_user_public_app"),

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
