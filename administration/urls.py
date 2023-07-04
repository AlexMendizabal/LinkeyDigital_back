from django.urls import path, include
from rest_framework import routers

from administration.views import LicenciaViewSet, LicenciaSuperViewSet, LicenciaCoonectViewSet,\
      LicenciaAdminViewSet, BlockersUsersViewSet, EditableUsersViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('licencia', LicenciaViewSet.as_view(), name="get_licencias"), 
    
    path('licenciasup', LicenciaSuperViewSet.as_view(), name="get_or_create_all_licenses"),
    path('licenciasup/<int:pk>', LicenciaSuperViewSet.as_view(), name="patch_licenses"), 

    path('licenciaConnect/<int:pk>', LicenciaCoonectViewSet.as_view(), name="connect_licenses_users"), 

    path('licenciaadm', LicenciaAdminViewSet.as_view(), name="get_licencias_adm"),

    #README: end points para bloquear usuarios... cambia el bolleano(si es true pasa a false y viceversa)
    path('edit/<int:pk>', EditableUsersViewSet.as_view(), name="block_or_desblock_user"),
    path('block/<int:pk>', BlockersUsersViewSet.as_view(), name="block_or_desblock_user")

]
