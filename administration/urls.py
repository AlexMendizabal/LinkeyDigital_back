from django.urls import path, include
from rest_framework import routers

from administration.views import LicenciaViewSet, LicenciaSuperViewSet, LicenciaCoonectViewSet,\
      LicenciaAdminViewSet, BlockersUsersViewSet, EditableUsersViewSet

from administration.views.licencias_viewset import ListAdminViewSet

router = routers.DefaultRouter()

urlpatterns = [
    #*********** admin users ************************ 

    #retorna la licencia a la que el usuario pertenece
    path('licencia', LicenciaViewSet.as_view(), name="get_licencias"), 



    #*********** super users ************************ 
    
    #README: metodo para crear licencias
    path('licenciasup', LicenciaSuperViewSet.as_view(), name="get_or_create_all_licenses"),
    path('licenciasup/<int:pk>', LicenciaSuperViewSet.as_view(), name="patch_licenses"), 

    # README:actualiza a el campo "licencia_id" de la clase customer usere para conectar estas dos entidades
    path('licenciaConnect/<int:pk>', LicenciaCoonectViewSet.as_view(), name="connect_licenses_users"), 
    # WAITING: Logica redundante... mezclar con licencia', LicenciaViewSet
    # README:retorna los usuarios adjuntados a la licencia del admin 
    path('licenciaadm', LicenciaAdminViewSet.as_view(), name="get_licencias_adm"),

    # README: Retorna las usuarios adjuntados de la licencia del admin, si eres superadmin
    path('licenciaadm/<int:pk>', LicenciaAdminViewSet.as_view(), name="get_licencias_adm_employee"),

    # Licenciaadm pero sin incluir la paginación, útil para listar empleados en la funcion contact
    path('listadm/<int:pk>', ListAdminViewSet.as_view(), name="get_list_adm_employee"),


    #README: end points para bloquear usuarios... cambia el bolleano(si es true pasa a false y viceversa)
    path('edit/<int:pk>', EditableUsersViewSet.as_view(), name="block_or_desblock_user"),
    path('block/<int:pk>', BlockersUsersViewSet.as_view(), name="block_or_desblock_user")

]
