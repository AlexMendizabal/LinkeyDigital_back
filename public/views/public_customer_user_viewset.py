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
        char_public_id = public_id.replace('-', "")

        try:
            customer_user = CustomerUser.objects.get(username=public_id)
        except:
            try:
                customer_user = CustomerUser.objects.get(public_id=public_id)
            except:
                raise Http404
        if not customer_user.has_access_to_protected_views():
                return Response({"succes": False, "message": "El usuario no tiene licencia"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:
            licencia = Licencia.objects.get(id=customer_user.licencia_id_id)
            #validamos que no sea el mismo usuario
            if licencia.customer_user_admin.id != customer_user.id:            
                customer_user_admin = licencia.customer_user_admin
            else :
                customer_user_admin = None
        except :
            customer_user_admin = None
        customer_user_public_service = PublicCustomerUserService()

        customer_profile_serializers = self.get_profile(customer_user_public_service, customer_user)
        customer_custom_social_media_serializers = self.get_custom_social_media(customer_user_public_service,
                                                                                customer_user)

        if customer_user_admin: 
            customer_profile_serializers_admin = self.get_profile(customer_user_public_service, customer_user_admin)
            customer_custom_social_media_serializers_admin = self.get_custom_social_media(customer_user_public_service,
                                                                                customer_user_admin)
            return Response({"success": True, "data": {"public_id": customer_user.public_id,
                                                   "profile": customer_profile_serializers.data,
                                                   "custom_social_media": customer_custom_social_media_serializers,}
                                              ,"admin": {"public_id": customer_user_admin.public_id,
                                                   "profile": customer_profile_serializers_admin.data,
                                                   "custom_social_media": customer_custom_social_media_serializers_admin,}},
                        status=status.HTTP_200_OK)
            
        return Response({"success": True, "data": {"public_id": customer_user.public_id,
                                                   "profile": customer_profile_serializers.data,
                                                   "custom_social_media": customer_custom_social_media_serializers,}},
                        status=status.HTTP_200_OK)

    def get_profile(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_profile(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileSerializer(response, many=False)
        return customer_profile_serializers


    def get_custom_social_media(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_custom_social_media(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=True)
        metodos = customerUserUtilities()
        data = metodos.put_image_with_type(customer_social_media_serializers)


        return data
