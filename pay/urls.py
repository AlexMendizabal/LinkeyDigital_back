from django.urls import path
from rest_framework import routers

from pay.views import SolicitudViewSet, ConsultaViewSet, ConsultaExtendViewSet, webhook

router = routers.DefaultRouter()

urlpatterns = [

    path('solicitud', SolicitudViewSet.as_view(), name="solicitud_pago"), 

    path('consulta_transaccion', ConsultaViewSet.as_view(), name="consulta_transaccion"), 
    path('consulta_extend/<int:pk>', ConsultaExtendViewSet.as_view(), name="consulta_transaccion"),

    
    path('webhook', webhook.as_view(), name="consulta_transaccion"),
    


]

# TODO: a consulta extend agregarle el datelle de la compra 
# TODO: que solo retorne datos ya pagados (con status 2)