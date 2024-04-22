from django.urls import path
from client_contact.views.client_contact_config_viewset import ConfigurationAPIView
from client_contact.views.client_contact_viewset import RegisterDetail, CreateRegister

urlpatterns = [
    path('config/', ConfigurationAPIView.as_view(), name='configuration-list'),
    path('config/<int:customer_user>/', ConfigurationAPIView.as_view(), name='configuration-detail'),

    path('register/<int:register_id>/', RegisterDetail.as_view(), name='register_detail'),
    path('register/', RegisterDetail.as_view(), name='register_list_or_create'),
]
