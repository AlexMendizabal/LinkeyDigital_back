from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from profile.models import CustomerUserProfile, CustomerUserCustomSocialMedia
from profile.services import ProfileService,  SocialMediaService
from profile.views import customerUserUtilities
from authentication.models import CustomerUser
from authentication.views import CustomerUserSerializer
from administration.UtilitiesAdministration import UtilitiesAdm

class CustomerUserProfileStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = ('counter', 'image', 'public_name')

class CustomerUserCustomSocialMediaStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = ('title', 'counter', 'image', 'type', 'url')

class CustomerUserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('username', 'rubro')


class CustomerUserStatistics(APIView):

    def get(self, request):

        user_id = request.GET.get('user_id', request.user)

        if user_id == request.user.id:
            user = request.user
        else:
            try:
                user = CustomerUser.objects.get(id = user_id)
            except Exception as e:
                return Response({"success": False, 'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
            
        utilities = Utilities()
        profile_service = ProfileService()
        social_media_service = SocialMediaService()

        customer_profile_serializers = utilities.get_profile(profile_service, None, user_id)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(social_media_service, None,
                                                                                user_id)

        customer_custom_social_media_serializers_formated = customer_custom_social_media_serializers if customer_custom_social_media_serializers else None

        return Response({"success": True, "data": {
            "profile": customer_profile_serializers.data['counter'],
            "custom_social_list": customer_custom_social_media_serializers_formated,
        }}, status=status.HTTP_200_OK)

class StaticsForAdminViewSet(APIView):
    def get(self, request):
        

        user_id = request.GET.get('user_id', request.user.id)

        if user_id == request.user.id:
            user = request.user
        else:
            try:
                user = CustomerUser.objects.get(id = user_id)
            except Exception as e:
                return Response({"success": False, 'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        licencia_id = user.licencia_id

        utilities = Utilities()
        profile_service = ProfileService()
        social_media_service = SocialMediaService()

        customer_profile = utilities.get_profile_and_social_medias_by_licencia(profile_service=profile_service,
                                                                               licencia_id=licencia_id,
                                                                               contact_service = social_media_service
                                                                               )
        if not customer_profile:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": customer_profile}, status=status.HTTP_200_OK)
    
class StaticsForSuperViewSet(APIView):
    def get(self, request):
        if not request.user.is_superuser:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile_service = ProfileService()
            data = profile_service.cantobjs()
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    
class Utilities():
    def get_profile(self, profile_service, pk, customer_user):
        try:
            response = profile_service.get_profile(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_profile_serializers = CustomerUserProfileStatisticsSerializer(response, many=False)
        return customer_profile_serializers

    def get_profile_and_social_medias_by_licencia(self, profile_service, contact_service, licencia_id):
        try:
            response = profile_service.get_users_by_licencia(licencia_id)
            if not response:
                return None
            profiles = []
            for usr in response:
                obj = profile_service.get_profile(customer_user=usr.id)
                obj = CustomerUserProfileStatisticsSerializer(obj, many=False)
                custom = contact_service.get_custom_social_media(customer_user=usr.id)
                custom = CustomerUserCustomSocialMediaStatisticsSerializer(custom,many=True)

                utilitiesC = customerUserUtilities()
                custom = utilitiesC.put_image_with_type(custom)

                user = CustomerUserStatisticsSerializer(usr, many=False)
                profiles.append({   **user.data, **obj.data, "statistics": {"custom_social_list": custom}})
            return profiles

        except Exception as e:
            return Response(None)



    def get_custom_social_media(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_custom_social_media(pk, customer_user)
            metodos = customerUserUtilities()
        except Exception as e:
            return Response(None)
        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaStatisticsSerializer(response,
                                                                                                     many=True)
        data = metodos.put_image_with_type(customer_custom_social_media_serializers)
        return data
