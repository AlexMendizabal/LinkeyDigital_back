from django.urls import path, include
from rest_framework import routers

from apps.mercado_pago.views import MercadoPago, MercadoPagoWebhook

router = routers.DefaultRouter()

urlpatterns = [
    # ******************  APARTADO PARA USUARIOS NORMALES ******************
    path('', MercadoPago.as_view(), name="mercado_pago"),
    # ******************  Web hooks ******************
    path('webhook', MercadoPagoWebhook.as_view(), name="mercado_pago_webhook")

   
]
