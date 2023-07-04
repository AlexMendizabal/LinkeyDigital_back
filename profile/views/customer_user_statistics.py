from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from profile.models import CustomerUserProfile, CustomerUserCustomSocialMedia
from profile.services import ProfileService,  SocialMediaService
from profile.views import customerUserUtilities

class CustomerUserProfileStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = ('counter', 'image', 'public_name')

class CustomerUserCustomSocialMediaStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = ('title', 'counter', 'image', 'type', 'url')

class CustomerUserStatistics(APIView):

    def get(self, request):
        utilities = Utilities()
        profile_service = ProfileService()
        social_media_service = SocialMediaService()

        customer_profile_serializers = utilities.get_profile(profile_service, None, request.user.id)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(social_media_service, None,
                                                                                request.user.id)

        customer_custom_social_media_serializers_formated = customer_custom_social_media_serializers if customer_custom_social_media_serializers else None

        return Response({"success": True, "data": {
            "profile": customer_profile_serializers.data['counter'],
            "custom_social_list": customer_custom_social_media_serializers_formated,
        }}, status=status.HTTP_200_OK)

class StaticsForAdminViewSet(APIView):
    def get(self, request):

        utilities = Utilities()
        profile_service = ProfileService()
        social_media_service = SocialMediaService()

        customer_profile = utilities.get_profile_and_social_medias_by_licencia(profile_service=profile_service,
                                                                               licencia_id=request.user.licencia_id,
                                                                               contact_service = social_media_service
                                                                               )
        if not customer_profile:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": customer_profile}, status=status.HTTP_200_OK)

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
                profiles.append({"profile": obj.data, "custom_social_list": custom.data})
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
