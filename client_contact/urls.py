from django.urls import path
from client_contact.views.client_contact_config_viewset import ConfigurationAPIView
from client_contact.views.client_contact_config_public_viewset import ConfigurationDetail
from client_contact.views.client_contact_viewset import RegisterListCreateAPIView, RegisterRetrieveUpdateDestroyAPIView
from client_contact.views.client_contact_public_viewset import RegisterCreateAPIView
from client_contact.views.multiple_contact_config_viewset import MultipleConfigurationViewSet

urlpatterns = [
    path('config/', ConfigurationAPIView.as_view(), name='configuration-list'),
    path('config/<int:customer_user>/', ConfigurationAPIView.as_view(), name='configuration-detail'),
    path('detail/<int:customer_user>/', ConfigurationDetail.as_view(), name='configuration-detail'),

    path('register/', RegisterListCreateAPIView.as_view(), name='register-list-create'),
    path('register/<int:pk>/', RegisterRetrieveUpdateDestroyAPIView.as_view(), name='register-detail'),
    
    path('get/<int:customer_user_id>/', RegisterListCreateAPIView.as_view(), name='customer-register-list'),

    path('create/', RegisterCreateAPIView.as_view(), name='register-create'),

    path('config/all_users/', MultipleConfigurationViewSet.as_view({'get': 'list', 'post': 'create'}), name='multiple-configuration-list-create'),
]
