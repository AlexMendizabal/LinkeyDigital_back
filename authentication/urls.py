from rest_framework import routers
from django.urls import path, include

from .views import AuthenticatedView, RegisterUser, CustomerUserViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('login', AuthenticatedView.as_view()),
    path('register', RegisterUser.as_view()),

    path('user', CustomerUserViewSet.as_view(), name="user_list_or_create_or_update_or_delete"),
]
