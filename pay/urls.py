from django.urls import path
from rest_framework import routers

from pay.views import SolicitudViewSet, ConsultaViewSet

router = routers.DefaultRouter()

urlpatterns = [

    path('solicitud', SolicitudViewSet.as_view(), name="solicitud_pago"), 

    path('consulta_transaccion', ConsultaViewSet.as_view(), name="consulta_transaccion"), 
    path('consulta_transaccion/<int:pk>', ConsultaViewSet.as_view(), name="consulta_transaccion"), 

]
