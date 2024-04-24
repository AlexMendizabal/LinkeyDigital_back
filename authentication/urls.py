from rest_framework import routers
from django.urls import path, include

from .views import AuthenticatedView, RegisterUser, CustomerUserViewSet, CustomerUserPutRubroViewSet \
   ,CreateALotOfUsers, CreateAdmin, CustomerAdminViewSet, VerifyToken, AuthenticationSpecialViewset

router = routers.DefaultRouter()

urlpatterns = [
    path('login', AuthenticatedView.as_view()),
    path('register', RegisterUser.as_view()),

    path('user', CustomerUserViewSet.as_view(), name="user_list_or_create_or_update_or_delete"),
    # Metodo para cambiar el rubro de muchos usuarios
    path('rubro', CustomerUserPutRubroViewSet.as_view(), name="user_list_or_create_or_update_or_delete"),

    # Metodo para crear varios usuarios a la vez
    #TODO: que rubro solo edite rubro 
    path('create', CreateALotOfUsers.as_view(), name="register_user"),
    # Metodo para crear un usuario con su licencia 
    path('create-admin', CreateAdmin.as_view(), name="register_user_admin"),
    path('edit-user/<int:customer_id>', CustomerAdminViewSet.as_view(), name="update_user_admin"),

    path('verifyToken', VerifyToken.as_view(), name="verifyEmail"),

    # Metodo para reiniciar users
    path('reset', AuthenticationSpecialViewset.as_view(), name="reset_user")


]