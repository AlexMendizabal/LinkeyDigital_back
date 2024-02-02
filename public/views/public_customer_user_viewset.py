from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import CustomerUser
from profile.views import CustomerUserProfileSerializer, \
    CustomerUserCustomSocialMediaSerializer, customerUserUtilities
from public.services import PublicCustomerUserService
from administration.models import Licencia


class PublicCustomerUserViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, public_id):
        utilities = CustomUserUtilities()
        customer_user = utilities.getUsers(public_id)
        if not customer_user:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        if not customer_user.has_access_to_protected_views():
            return Response({"succes": False, "message": "El usuario no tiene licencia"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        customer_user_admin = utilities.getAdminLicencia(customer_user)
        customer_user_public_service = PublicCustomerUserService()

        customer_profile_serializers = utilities.get_profile(customer_user_public_service, customer_user)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(customer_user_public_service,
                                                                                    customer_user, True)

        customer_profile_serializers_admin = None
        customer_custom_social_media_serializers_admin = None

        if customer_user_admin:
            customer_profile_serializers_admin = utilities.get_profile(customer_user_public_service,
                                                                       customer_user_admin)
            customer_custom_social_media_serializers_admin = utilities.get_custom_social_media(
                customer_user_public_service, customer_user_admin, True)

        data = utilities.makeData(customer_user, customer_profile_serializers, customer_custom_social_media_serializers,
                                  customer_user_admin, customer_profile_serializers_admin,
                                  customer_custom_social_media_serializers_admin)
        return Response({"success": True, "data": data},
                        status=status.HTTP_200_OK)

    

class CustomUserUtilities():
    def get_profile(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_profile(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileSerializer(response, many=False)
        return customer_profile_serializers


    def get_custom_social_media(self, customer_user_public_service, customer_user, trues = False):
        try:
            if trues:
                response = customer_user_public_service.get_custom_social_media_only_true(None, customer_user.pk)
            else:
                response = customer_user_public_service.get_custom_social_media(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=True)
        metodos = customerUserUtilities()
        data = metodos.put_image_with_type(customer_social_media_serializers)
        return data
    
    def getAdminLicencia(self, customer_user):
        try:
            licencia = Licencia.objects.get(id=customer_user.licencia_id_id)
            #validamos que no sea el mismo usuario
            if licencia.customer_user_admin.id != customer_user.id:            
                customer_user_admin = licencia.customer_user_admin
            else :
                return None
        except :
            return None
        return customer_user_admin
    

    def getUsers(self,public_id ):
        try:
            customer_user = CustomerUser.objects.get(username=public_id)
        except:
            try:
                customer_user = CustomerUser.objects.get(public_id=public_id)
            except:
                return  None
        return customer_user
    
    def makeData(self, customer_user, customer_profile_serializers, customer_custom_social_media_serializers, customer_user_admin, customer_profile_serializers_admin, customer_custom_social_media_serializers_admin):
        if customer_user_admin:
            data = {"public_id": customer_user.public_id,
                    "username": customer_user.username,
                    "is_booking": customer_user.is_booking,
                    "profile": customer_profile_serializers.data,
                    "custom_social_media": customer_custom_social_media_serializers,
                    "admin":    {"public_id": customer_user_admin.public_id,
                                "profile": customer_profile_serializers_admin.data,
                                "custom_social_media": customer_custom_social_media_serializers_admin,}}
        else : 
            data = {"public_id": customer_user.public_id,
                    "username": customer_user.username,
                    "is_booking": customer_user.is_booking,
                    "profile": customer_profile_serializers.data,
                    "custom_social_media": customer_custom_social_media_serializers}
        return data