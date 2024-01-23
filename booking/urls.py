from rest_framework import routers
from django.urls import path, include

from booking.views import BookingViewset, ConfBookingViewset, PublicBookingViewset

router = routers.DefaultRouter()

urlpatterns = [
    #metodos para reservas publicas
    path('', PublicBookingViewset.as_view()),
    #metodos para reservas de los clientes
    path('get', BookingViewset.as_view()),
    path('get/<int:user_id>', BookingViewset.as_view()),

    #metodos para conf de reservas 
    path('setting', ConfBookingViewset.as_view()),
    path('setting/<int:user_id>', ConfBookingViewset.as_view()),
]
