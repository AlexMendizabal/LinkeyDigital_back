from rest_framework import routers
from django.urls import path, include

from contact.views import UserSendMailViewSet, OrderNewCardsViewSet, SendEmailRawViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('send-email', UserSendMailViewSet.as_view()),
    #solicitud de aumento de cuentas/tarjetas
    path('send-email-new-cards', OrderNewCardsViewSet.as_view()),

    path('send-basic-email', SendEmailRawViewSet.as_view())
]
