from django.urls import path, include
from rest_framework import routers

from mercado_pago.views import MercadoPago

router = routers.DefaultRouter()

urlpatterns = [
    # ******************  APARTADO PARA USUARIOS NORMALES ******************
    path('', MercadoPago.as_view(), name="mercado_pago")

   
]
