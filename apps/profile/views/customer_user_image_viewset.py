import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from apps.profile.models import CustomerUserCustomImage , CustomImageDto
from apps.profile.services import Contactservices


class CustomerUserCustomImageserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomImage
        fields = (
            'id', 'customer_user', 'title',  'image', 'imageQR', 'is_active', 'is_visible')
        extra_kwargs = {'title': {'required': True}, 
                        'is_visible': {'required': True}}


class CustomerUserImageViewSet(APIView):
    def get(self, request, pk=None):
        try:
            social_image = Contactservices()
            try:
                response = social_image.get_custom_image(pk, request.user.id)
            except Exception as e:
                return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

            customer_custom_image_serializers = CustomerUserCustomImageserializers(response, many=True)
            return Response({"success": True, "data": customer_custom_image_serializers.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializers = CustomerUserCustomImageserializers(data=request.data)

        if not serializers.is_valid():
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.build_dto_from_validated_data(serializers)
        social_image = Contactservices()

        try:
            response = social_image.create_or_update_image(dto)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)

        customer_custom_image_serializers = CustomerUserCustomImageserializers(response, many=False)
        return Response({"success": True, "data": customer_custom_image_serializers.data},
                        status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        customer_user_custom_social_media = get_object_or_404(CustomerUserCustomImage,
                                                              id=pk)

        if request.user.id != customer_user_custom_social_media.customer_user_id:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        if 'image' in request.data and customer_user_custom_social_media.image != "custom_social_media/undefined.png":
            try:
                os.remove(customer_user_custom_social_media.image.path)
            except Exception as e:
                pass

        if 'title' in request.data:
            if request.data.get('title').replace(" ", "") == "":
                CustomerUserCustomImage.objects.filter(customer_user=request.user.id, pk=pk).delete()
                return Response({"success": True})

        # if 'url' in request.data:
        #     if request.data.get('url').replace(" ", "") == "":
        #         CustomerUserCustomImage.objects.filter(customer_user=request.user.id, pk=pk).delete()
        #         return Response({"success": True})

        customer_user_custom_social_media_serializers = CustomerUserCustomImageserializers(
            instance=customer_user_custom_social_media,
            data=request.data, partial=True)

        customer_user_custom_social_media_serializers.is_valid(raise_exception=True)
        customer_user_custom_social_media_serializers.save()

        return Response({"success": True, "data": customer_user_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)


    def build_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
        return CustomImageDto(
            customer_user=data["customer_user"],
            title=data["title"],
            is_active=True,
            is_visible=data["is_visible"],
        )
