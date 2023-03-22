from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from profile.models import CustomerUserProfile, CustomerUserWhatsapp, CustomerUserEmail, CustomerUserPhone, \
    CustomerUserSocialMedia, CustomerUserMap, SocialMedia, CustomerUserCustomSocialMedia
from profile.services import ProfileService, ContactService, SocialMediaService


class SocialMediaStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ('title', 'image')


class CustomerUserProfileStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = ('counter', 'image')


class CustomerUserWhatsappStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserWhatsapp
        fields = ('counter', 'image')


class CustomerUserEmailStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserEmail
        fields = ('counter', 'image')


class CustomerUserPhoneStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserPhone
        fields = ('counter', 'image')


class CustomerUserMapStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserMap
        fields = ('counter',)


class CustomerUserCustomSocialMediaStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = ('title', 'counter', 'image')


class CustomerUserSocialMediaStatisticsSerializer(serializers.ModelSerializer):
    social_media = SocialMediaStatisticsSerializer(many=False, read_only=True)

    class Meta:
        model = CustomerUserSocialMedia
        fields = ('social_media', 'counter')


class CustomerUserStatistics(APIView):

    def get(self, request):
        profile_service = ProfileService()
        contact_service = ContactService()
        social_media_service = SocialMediaService()

        customer_profile_serializers = self.get_profile(profile_service, None, request.user.id)
        customer_whatsapp_serializers = self.get_whatsapp(contact_service, None, request.user.id)
        customer_email_serializers = self.get_email(contact_service, None, request.user.id)
        customer_phone_serializers = self.get_phone(contact_service, None, request.user.id)
        customer_map_serializers = self.get_map(contact_service, None, request.user.id)
        customer_social_media_serializers = self.get_social_media(social_media_service, None, request.user.id)
        customer_custom_social_media_serializers = self.get_custom_social_media(social_media_service, None,
                                                                                request.user.id)

        customer_whatsapp_serializers_formate = customer_whatsapp_serializers.data if customer_whatsapp_serializers.data else None
        customer_email_serializers_formated = customer_email_serializers.data if customer_email_serializers.data else None
        customer_phone_serializers_formated = customer_phone_serializers.data if customer_phone_serializers.data else None
        customer_map_serializers_formated = customer_map_serializers.data if customer_map_serializers.data else None

        customer_social_media_serializers_formated = customer_social_media_serializers.data if customer_social_media_serializers.data else None
        customer_custom_social_media_serializers_formated = customer_custom_social_media_serializers.data if customer_custom_social_media_serializers.data else None

        return Response({"success": True, "data": {
            "profile": customer_profile_serializers.data['counter'],
            "whatsapp": customer_whatsapp_serializers_formate,
            "email": customer_email_serializers_formated,
            "phone": customer_phone_serializers_formated,
            "map": customer_map_serializers_formated,
            "social_media_list": customer_social_media_serializers_formated,
            "custom_social_list": customer_custom_social_media_serializers_formated,
        }}, status=status.HTTP_200_OK)

    def get_profile(self, profile_service, pk, customer_user):
        try:
            response = profile_service.get_profile(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_profile_serializers = CustomerUserProfileStatisticsSerializer(response, many=False)
        return customer_profile_serializers

    def get_whatsapp(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_whatsapp(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_whatsapp_serializers = CustomerUserWhatsappStatisticsSerializer(response, many=False)
        return customer_whatsapp_serializers

    def get_email(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_email(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_email_serializers = CustomerUserEmailStatisticsSerializer(response, many=False)
        return customer_email_serializers

    def get_map(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_map(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_map_serializers = CustomerUserMapStatisticsSerializer(response, many=False)
        return customer_map_serializers

    def get_phone(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_phone(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_phone_serializers = CustomerUserPhoneStatisticsSerializer(response, many=False)
        return customer_phone_serializers

    def get_social_media(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_social_media(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_social_media_serializers = CustomerUserSocialMediaStatisticsSerializer(response, many=True)
        return customer_social_media_serializers

    def get_custom_social_media(self, contact_service, pk, customer_user):
        try:
            response = contact_service.get_custom_social_media(pk, customer_user)
        except Exception as e:
            return Response(None)
        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaStatisticsSerializer(response,
                                                                                                     many=True)
        return customer_custom_social_media_serializers
