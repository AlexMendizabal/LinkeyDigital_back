from rest_framework import routers
from django.urls import path, include

from .views import AuthenticatedView, RegisterUser, CustomerUserViewSet, CustomerUserPutRubroViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('login', AuthenticatedView.as_view()),
    path('register', RegisterUser.as_view()),

    path('user', CustomerUserViewSet.as_view(), name="user_list_or_create_or_update_or_delete"),
    #README: Metodo para cambiar el rubro de muchos usuarios
    path('rubro', CustomerUserPutRubroViewSet.as_view(), name="user_list_or_create_or_update_or_delete"),
]
