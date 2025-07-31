from django.urls import path
from apps.ecommerce.views.button_viewset import ButtonListCreateAPIView, ButtonRetrieveUpdateDestroyAPIView
from apps.ecommerce.views.button_public_viewset import ButtonListByCustomerUserAPIView


urlpatterns = [
    path('buttons/', ButtonListCreateAPIView.as_view(), name='button-list-create'),
    path('buttons/<int:pk>/', ButtonRetrieveUpdateDestroyAPIView.as_view(), name='button-detail'),
    path('get/<int:customer_user_id>/', ButtonListByCustomerUserAPIView.as_view(), name='button-list-by-customer-user'),
]
