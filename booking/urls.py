from rest_framework import routers
from django.urls import path, include

from booking.views import BookingViewset, ConfBookingViewset, PublicBookingViewset, PublicConfBookingViewset \
    ,PUblicSearchBookingViewset, PublicBusyViewset
from booking.views.booking_settings_viewset import ConfBookingListView, ConfBookingCreateView,ConfBookingUpdateView,ConfBookingDeleteView,ConfBookingRetrieveView



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

    #método para múltiples configuraciones por usuario
    path('conf/<int:customer_user_id>/', ConfBookingListView.as_view(), name='conf_booking_list'),
    path('conf/<int:customer_user_id>/create', ConfBookingCreateView.as_view(), name='conf_booking_create'),
    path('conf/<int:pk>/update/', ConfBookingUpdateView.as_view(), name='conf_booking_update'),
    path('conf/<int:pk>/delete/', ConfBookingDeleteView.as_view(), name='conf_booking_delete'),
    path('conf/get/<int:pk>/', ConfBookingRetrieveView.as_view(), name='conf_booking_detail'),
]
