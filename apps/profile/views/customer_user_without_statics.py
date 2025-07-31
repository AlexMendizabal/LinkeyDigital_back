from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.profile.services import Profileservices
from apps.public.services import PublicCustomerUserservices
from apps.public.views import CustomUserUtilities


class CustomerUserWithoutStatics(APIView):

    def get(self, request, public_id):
        utilities = CustomUserUtilities()
        customer_user = utilities.getUsers(public_id)
        if not customer_user:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        

        customer_user_public_services = PublicCustomerUserservices()
        customer_user_profile_services = Profileservices()

        customer_profile_serializers = utilities.get_profile(customer_user_profile_services, customer_user)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(customer_user_public_services,
                                                                               customer_user)

        data = {"public_id": customer_user.public_id,
                "username": customer_user.username,
                "profile": customer_profile_serializers.data,
                "custom_social_media": customer_custom_social_media_serializers}
        
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


    

