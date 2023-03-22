from rest_framework.views import APIView

from rest_framework import serializers

from profile.models import CustomerUserSocialMedia, SocialMedia, SocialMediaDto
from rest_framework.response import Response
from rest_framework import status

from profile.services import SocialMediaService
from profile.views import SocialMediaSerializer


class CustomerUserSocialMediaSerializer(serializers.ModelSerializer):
    social_media_id = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=SocialMedia.objects.all(),
        source="social_media"
    )
    social_media = SocialMediaSerializer(many=False, read_only=True)

    class Meta:
        model = CustomerUserSocialMedia
        fields = (
            'id', 'customer_user', 'social_media_id', 'social_media', 'url_complete',
            'is_active',
            'is_visible')
        extra_kwargs = {'url_complete': {'required': True}, 'social_media_id': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserSocialMediaViewSet(APIView):
    def get(self, request, pk=None):
        social_media_service = SocialMediaService()
        try:
            response = social_media_service.get_social_media(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        if pk:
            customer_social_media_serializers = CustomerUserSocialMediaSerializer(response, many=False)
        else:
            customer_social_media_serializers = CustomerUserSocialMediaSerializer(response, many=True)
        return Response({"success": True, "data": customer_social_media_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializer = CustomerUserSocialMediaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if 'social_media_id' in request.data and 'url_complete' in request.data:
            if request.data.get('url_complete').replace(" ", "") == "":
                CustomerUserSocialMedia.objects.filter(customer_user_id=request.data["customer_user"],
                                                       social_media_id=request.data['social_media_id']).delete()
                return Response({"success": True})

        dto = self.buid_dto_from_validated_data(serializer)
        social_media_service = SocialMediaService()

        try:
            response = social_media_service.create_or_update_social_media(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_social_media_serializers = CustomerUserSocialMediaSerializer(response, many=False)
        return Response({"success": True, "data": customer_social_media_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return SocialMediaDto(
            customer_user=data["customer_user"],
            social_media=data["social_media"],
            url_complete=data["url_complete"],
            is_active=True,
            is_visible=data["is_visible"],
        )
