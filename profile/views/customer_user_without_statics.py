from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService
from public.services import PublicCustomerUserService
from public.views import CustomUserUtilities


class CustomerUserWithoutStatics(APIView):

    def get(self, request, public_id):
        utilities = CustomUserUtilities()
        customer_user = utilities.getUsers(public_id)
        if not customer_user:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        

        customer_user_public_service = PublicCustomerUserService()
        customer_user_profile_service = ProfileService()

        customer_profile_serializers = utilities.get_profile(customer_user_profile_service, customer_user)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(customer_user_public_service,
                                                                               customer_user)

        data = {"public_id": customer_user.public_id,
                "username": customer_user.username,
                "profile": customer_profile_serializers.data,
                "custom_social_media": customer_custom_social_media_serializers}
        
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)

        #if not customer_user.has_access_to_protected_views():
        #        return Response({"succes": False, "message": "El usuario no tiene licencia"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        #customer_user_admin = utilities.getAdminLicencia(customer_user)
        
        customer_user_public_service = PublicCustomerUserService()
        #customer_user_profile_service = ProfileService()
        

        #customer_profile_serializers = utilities.get_profile(customer_user_profile_service, customer_user)
        #customer_custom_social_media_serializers = utilities.get_custom_social_media(customer_user_public_service,
        #                                                                        customer_user)
        
        #customer_profile_serializers_admin = None
        #customer_custom_social_media_serializers_admin = None

        #if customer_user_admin: 
        #    customer_profile_serializers_admin = utilities.get_profile(customer_user_profile_service, customer_user_admin)
        #    customer_custom_social_media_serializers_admin = utilities.get_custom_social_media(customer_user_public_service,
        #                                                                        customer_user_admin)
        #data = utilities.makeData(customer_user, customer_profile_serializers, customer_custom_social_media_serializers,
        #                          customer_user_admin, customer_profile_serializers_admin,
        #                          customer_custom_social_media_serializers_admin)
        #return Response({"success": True, "data": data},
        #                status=status.HTTP_200_OK)

    

