import io
import os
from io import BytesIO
from sys import getsizeof

from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers
from profile.models import CustomerUserProfile, ProfileDto, DesignProfile
from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService


class CustomerUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = (
            'customer_user', 'career', 'public_name', 'description', 'color', 'background',
            'image')


class CustomerUserProfileViewSet(APIView):
    def get(self, request, pk=None):
        profile_service = ProfileService()
        try:
            response = profile_service.get_profile(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileSerializer(response, many=False)
        return Response({"success": True, "data": customer_profile_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id

        try:
            instance = CustomerUserProfile.objects.get(customer_user=request.user.id)
        except Exception as e:
            instance = None

        serializer = CustomerUserProfileSerializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(serializer)
        profile_service = ProfileService()

        try:
            response = profile_service.create_profile(dto)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_email_serializers = CustomerUserProfileSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def put(self, request):
        customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=request.user.id)

        if request.user.id != customer_user_profile.customer_user_id:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        if 'image' in request.data and customer_user_profile.image != "profile/icon_perfil.png":
            try:
                os.remove(customer_user_profile.image.path)
            except Exception as e:
                pass

        if 'background' in request.data and customer_user_profile.background != "background/image_background.png":
            try:
                os.remove(customer_user_profile.background.path)
            except Exception as e:
                pass

        customer_user_profile_serializers = CustomerUserProfileSerializer(
            instance=customer_user_profile,
            data=request.data, partial=True)

        customer_user_profile_serializers.is_valid(raise_exception=True)
        customer_user_profile_serializers.save()

        return Response({"success": True, "data": customer_user_profile_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return ProfileDto(
            customer_user=data["customer_user"],
            public_id=data["public_id"],
            career=data["career"],
            public_name=data["public_name"],
            description=data["description"],
        )
