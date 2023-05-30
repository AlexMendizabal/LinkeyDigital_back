from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import CustomerUser
from profile.views import CustomerUserProfileSerializer, CustomerUserSocialMediaSerializer, \
    CustomerUserWhatsappSerializer, CustomerUserPhoneSerializer, CustomerUserEmailSerializer, CustomerUserMapSerializer, \
    CustomerUserCustomSocialMediaSerializer
from public.services import PublicCustomerUserService


class PublicCustomerUserViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, param):
        try:
            customer_user = CustomerUser.objects.get(username=param)
        except:
            try:
                customer_user = CustomerUser.objects.get(public_id=param)
            except:
                raise Http404
                
        customer_user_public_service = PublicCustomerUserService()

        customer_profile_serializers = self.get_profile(customer_user_public_service, customer_user)
        customer_social_media_serializers = self.get_social_media(customer_user_public_service, customer_user)
        customer_custom_social_media_serializers = self.get_custom_social_media(customer_user_public_service,
                                                                                customer_user)
        customer_whatsapp_serializers = self.get_whatsapp(customer_user_public_service, customer_user)
        customer_phone_serializers = self.get_phone(customer_user_public_service, customer_user)
        customer_email_serializers = self.get_email(customer_user_public_service, customer_user)
        customer_map_serializers = self.get_map(customer_user_public_service, customer_user)

        customer_whatsapp_serializers_formated = customer_whatsapp_serializers.data if customer_whatsapp_serializers else None
        customer_phone_serializers_formated = customer_phone_serializers.data if customer_phone_serializers else None
        customer_email_serializers_formated = customer_email_serializers.data if customer_email_serializers else None
        customer_map_serializers_formated = customer_map_serializers.data if customer_map_serializers else None

        return Response({"success": True, "data": {"public_id": customer_user.public_id,
                                                   "profile": customer_profile_serializers.data,
                                                   "social_media": customer_social_media_serializers.data,
                                                   "custom_social_media": customer_custom_social_media_serializers.data,
                                                   "whatsapp": customer_whatsapp_serializers_formated,
                                                   "phone": customer_phone_serializers_formated,
                                                   "email": customer_email_serializers_formated,
                                                   "map": customer_map_serializers_formated}},
                        status=status.HTTP_200_OK)

    def get_profile(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_profile(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileSerializer(response, many=False)
        return customer_profile_serializers

    def get_social_media(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_social_media(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_social_media_serializers = CustomerUserSocialMediaSerializer(response, many=True)
        return customer_social_media_serializers

    def get_custom_social_media(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_custom_social_media(None, customer_user.pk)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=True)
        return customer_social_media_serializers

    def get_whatsapp(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_whatsapp(None, customer_user.pk)
        except Exception as e:
            return None

        customer_whatsapp_serializers = CustomerUserWhatsappSerializer(response, many=False)
        return customer_whatsapp_serializers

    def get_phone(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_phone(None, customer_user.pk)
        except Exception as e:
            return None

        customer_phone_serializers = CustomerUserPhoneSerializer(response, many=False)
        return customer_phone_serializers

    def get_email(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_email(None, customer_user.pk)
        except Exception as e:
            return None

        customer_email_serializers = CustomerUserEmailSerializer(response, many=False)
        return customer_email_serializers

    def get_map(self, customer_user_public_service, customer_user):
        try:
            response = customer_user_public_service.get_map(None, customer_user.pk)
        except Exception as e:
            return None

        customer_map_serializers = CustomerUserMapSerializer(response, many=False)
        return customer_map_serializers
