from django.urls import path, include
from rest_framework import routers

from profile.views import CustomerUserProfileViewSet, CustomerUserWhatsappViewSet, CustomerUserReservaViewSet,\
    CustomerUserEmailViewSet, CustomerUserMapViewSet, CustomerUserPhoneViewSet, CustomerUserSocialMediaViewSet, CustomerUserImageViewSet, \
    CustomerUserCustomSocialMediaViewSet, CustomerUserStatistics, DesignProfileViewSet, SocialmediaViewSet, \
    ViewsViewSet, CustomerUserCustomSocialMediaByAllUserViewSet,\
    StaticsForAdminViewSet, CustomerUserWithoutStatics, CustomerUserAllProfileViewSet, \
    CustomerUserLicensProfileViewSet, StaticsForSuperViewSet, CustomerUserProfileForAdmViewSet , \
    customer_user_custom_order_viewset

from profile.views.customer_user_profile_log import view_profile_log

router = routers.DefaultRouter()

urlpatterns = [
    # ******************  APARTADO PARA USUARIOS NORMALES ******************
    path('user', CustomerUserProfileViewSet.as_view(), name="customer_user_profile_get_or_create_or_update"),
    path('user/<int:pk>', CustomerUserProfileViewSet.as_view(), name="customer_user_profile_get_one"),

    #README: Metodo que trae perfil como "soy-yo/user" pero sin afectar las metricas
    path('userWithoutStatcis/<str:public_id>', CustomerUserWithoutStatics.as_view(), name="get_user_public_app"),

    path('social_media', CustomerUserSocialMediaViewSet.as_view(),
         name="customer_user_social_media_get_or_create_or_update"),
    path('social_media/<int:pk>', CustomerUserSocialMediaViewSet.as_view(), name="customer_user_social_media_get_one"),

    path('custom_social_media', CustomerUserCustomSocialMediaViewSet.as_view(),
         name="customer_user_custom_social_media_get_or_create"),
    path('custom_social_media/<int:pk>', CustomerUserCustomSocialMediaViewSet.as_view(),
         name="customer_user_custom_social_media_get_one_or_update_or_delete"),
     #README: Metodo para cambiar el orden de los social media
    path('custom_social_media_order', customer_user_custom_order_viewset.as_view(),
         name="customer_user_custom_social_media_change_order"),

    path('base_social_media', SocialmediaViewSet.as_view(), name="socialmedia_list"),
    path('base_social_media/<int:pk>', SocialmediaViewSet.as_view(), name="socialmedia_get"),

    path('base_design_profile', DesignProfileViewSet.as_view(), name="design_profile_list"),
    path('base_design_profile/<int:pk>', DesignProfileViewSet.as_view(), name="design_profile_get"),

    path('statistics/', CustomerUserStatistics.as_view(),
         name="get_customer_user_statistics"),

     path('image', CustomerUserImageViewSet.as_view(), name="customer_user_image_get_or_create_or_update"),
    path('image/<int:pk>', CustomerUserImageViewSet.as_view(), name="customer_user_whatsapp_get_one"),

    path('reserva/<int:social>', CustomerUserReservaViewSet.as_view(),  name="get_reserva"),

    path('view/<int:month>/<int:year>/<int:profile>', ViewsViewSet.as_view(),  name="get_views"),

#**************** APARTADO para administradores *********************

    # WAITING: Se debe evitar ids repetidos... se podria hacer una funcion para ahorrar la parte de buscar users en el id
    # README: Esta url sirve para aregrar varios el mismo tiepo
    path('custom_social_media_for_all_user', CustomerUserCustomSocialMediaByAllUserViewSet.as_view(),  name="custom_user_for_all_user"),

    #README: Metodo que traer los perfiles de usuarios en la licencia del admin
    path('myUsers', CustomerUserLicensProfileViewSet.as_view(), name="get_all_enterprises"),

    #README: Traera las metricas de todos los usuarios en la licencia 
    path('statisticsAdm/', StaticsForAdminViewSet.as_view(),
         name="get_customer_user_statistics_for_adm"),

    #README: Trae o edita algun profile
    path('user-profile/<int:customer_user>', CustomerUserProfileForAdmViewSet.as_view(),
         name="get_or_edit_profile"),

#**************** APARTADO para superUsuarios *********************
    #README: Metodo que traer todos los perfiles administradores
    path('allEmpresas/', CustomerUserAllProfileViewSet.as_view(), name="get_all_users"),

    #README: Metodo que traer perfil de usuarios en la licencia del admin(aca se debe mandar la licencia requerida)
    path('myUsers/<int:licencia_id>', CustomerUserLicensProfileViewSet.as_view(), name="get_all_enterprises"),
    #README: Traera las metricas generales para el super admin
    path('statisticsSup', StaticsForSuperViewSet.as_view(),
         name="get_customer_user_statistics_for_adm"),

# ************** DELETEME: METODOS YA INUTILES... EVITAR USAR *************************

    path('whatsapp', CustomerUserWhatsappViewSet.as_view(), name="customer_user_whatsapp_get_or_create_or_update"),
    path('whatsapp/<int:pk>', CustomerUserWhatsappViewSet.as_view(), name="customer_user_whatsapp_get_one"),

    path('email', CustomerUserEmailViewSet.as_view(), name="customer_user_email_get_or_create_or_update"),
    path('email/<int:pk>', CustomerUserEmailViewSet.as_view(), name="customer_user_email_get_one"),

    path('map', CustomerUserMapViewSet.as_view(), name="customer_user_map_get_or_create_or_update"),
    path('map/<int:pk>', CustomerUserMapViewSet.as_view(), name="customer_user_map_get_one"),

    path('phone', CustomerUserPhoneViewSet.as_view(), name="customer_user_phone_get_or_create_or_update"),
    path('phone/<int:pk>', CustomerUserPhoneViewSet.as_view(), name="customer_user_phone_get_one"),

   path('log/<int:custom_user_id>/', view_profile_log, name='view_all_profiles'),
]
