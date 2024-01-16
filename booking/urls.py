from rest_framework import routers
from django.urls import path, include

from booking.views import BookingViewset

router = routers.DefaultRouter()

urlpatterns = [
    #metodos para reservas
    path('', BookingViewset.as_view()),
    path('<int:pk>', BookingViewset.as_view()),
]
