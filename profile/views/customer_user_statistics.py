from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from profile.models import CustomerUserProfile, CustomerUserCustomSocialMedia
from profile.services import ProfileService,  SocialMediaService


class CustomerUserProfileStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = ('counter', 'image')

class CustomerUserCustomSocialMediaStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = ('title', 'counter', 'image')

class CustomerUserStatistics(APIView):

    def get(self, request):
        profile_service = ProfileService()
        social_media_service = SocialMediaService()

        customer_profile_serializers = self.get_profile(profile_service, None, request.user.id)
        customer_custom_social_media_serializers = self.get_custom_social_media(social_media_service, None,
                                                                                request.user.id)

        customer_custom_social_media_serializers_formated = customer_custom_social_media_serializers.data if customer_custom_social_media_serializers.data else None

        return Response({"success": True, "data": {
            "profile": customer_profile_serializers.data['counter'],
            "custom_social_list": customer_custom_social_media_serializers_formated,
        }}, status=status.HTTP_200_OK)

    def get_profile(self, profile_service, pk, customer_user):
        try:
            response = profile_service.get_profile(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_profile_serializers = CustomerUserProfileStatisticsSerializer(response, many=False)
        return customer_profile_serializers


    def get_custom_social_media(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_custom_social_media(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaStatisticsSerializer(response,
                                                                                                     many=True)
        return customer_custom_social_media_serializers
