from rest_framework import routers
from django.urls import path, include

from booking.views import BookingViewset, ConfBookingViewset, PublicBookingViewset, PublicConfBookingViewset \
    ,PUblicSearchBookingViewset, PublicBusyViewset


router = routers.DefaultRouter()

urlpatterns = [
    # metodos para reservas publicas
    path('', PublicBookingViewset.as_view()),
    # metodos para reservas de los clientes
    path('get', BookingViewset.as_view()),
    path('get/<int:pk>', BookingViewset.as_view()),

    # metodos para conf de reservas publicas y los horarios 
    path('setting/<str:user>', PublicConfBookingViewset.as_view()),
    # metodos para conf de reservas 
    path('setting', ConfBookingViewset.as_view()),
    
    # metodo public para ver reservas
    path('public/<int:codigo>', PUblicSearchBookingViewset.as_view()),
    # metodos para get reservas ocupadas 
    path('public/busy/<int:user>', PublicBusyViewset.as_view()),
]
