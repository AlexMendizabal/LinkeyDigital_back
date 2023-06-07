import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from profile.models import CustomerUserCustomSocialMedia, CustomSocialMediaDto
from profile.services import SocialMediaService


class CustomerUserCustomSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = (
            'id', 'customer_user', 'title', 'url', 'image', 'is_active', 'is_visible', 'type')
        extra_kwargs = {'title': {'required': True}, 'url': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserCustomSocialMediaViewSet(APIView):
    def get(self, request, pk=None):
        try:
            social_media_service = SocialMediaService()
            try:
                response = social_media_service.get_custom_social_media(pk, request.user.id)
            except Exception as e:
                return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

            customer_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=True)
            print(customer_custom_social_media_serializers)
            print("aaaaaaaaaaaaaah")
            data = self.put_image_with_type(customer_custom_social_media_serializers)

            return Response({"success": True, "data": data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        if 'type' not in request.data :
            request.data["type"] = "socialMedia"
        serializer = CustomerUserCustomSocialMediaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(serializer)
        social_media_service = SocialMediaService()

        try:
            response = social_media_service.create_custom_social_media(dto)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=False)
        return Response({"success": True, "data": customer_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia,
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
                CustomerUserCustomSocialMedia.objects.filter(customer_user=request.user.id, pk=pk).delete()
                return Response({"success": True})

        if 'url' in request.data:
            if request.data.get('url').replace(" ", "") == "":
                CustomerUserCustomSocialMedia.objects.filter(customer_user=request.user.id, pk=pk).delete()
                return Response({"success": True})

        customer_user_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(
            instance=customer_user_custom_social_media,
            data=request.data, partial=True)

        customer_user_custom_social_media_serializers.is_valid(raise_exception=True)
        customer_user_custom_social_media_serializers.save()

        return Response({"success": True, "data": customer_user_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)
    
    def delete (self, request, pk=None):

        social_media_service = SocialMediaService()
        try:
            response = social_media_service.delete_custom_social_media(pk, request.user.id)
            return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)


    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return CustomSocialMediaDto(
            customer_user=data["customer_user"],
            title=data["title"],
            url=data["url"],
            is_active=True,
            is_visible=data["is_visible"],
            type=data["type"],
        )
    
    def put_image_with_type(self, customer_custom_social_media_serializers): 
        data = []
        for ccsms in customer_custom_social_media_serializers.data:
            # Calcular el valor de fecha_fin y agregarlo al diccionario
            if ccsms["type"] == "whatsappp" :
                ccsms["image"] = "/media/custom_social_media/icons8-whatsapp-96.png"
            elif ccsms["type"] == "facebook" :
                ccsms["image"] = "/media/custom_social_media/icons8-facebook-96.png"
            elif ccsms["type"] == "github" :
                ccsms["image"] = "/media/custom_social_media/icons8-github-96.png"
            elif ccsms["type"] == "gitlab" :
                ccsms["image"] = "/media/custom_social_media/icons8-gitlab-96.png"
            elif ccsms["type"] == "maps" :
                ccsms["image"] = "/media/custom_social_media/icons8-google-maps-old-96.png"
            elif ccsms["type"] == "instagram" :
                ccsms["image"] = "/media/custom_social_media/icons8-instagram-96.png"
            elif ccsms["type"] == "linkedin" :
                ccsms["image"] = "/media/custom_social_media/icons8-linkedin-96.png"
            elif ccsms["type"] == "correo" :
                ccsms["image"] = "/media/custom_social_media/icons8-mail-96.png"
            elif ccsms["type"] == "phone" :
                ccsms["image"] = "/media/custom_social_media/icons8-phone-96.png"
            elif ccsms["type"] == "skype" :
                ccsms["image"] = "/media/custom_social_media/icons8-skype-96.png"
            elif ccsms["type"] == "snapchat" :
                ccsms["image"] = "/media/custom_social_media/icons8-snapchat-96.png"
            elif ccsms["type"] == "spotify" :
                ccsms["image"] = "/media/custom_social_media/icons8-spotify-96.png"
            elif ccsms["type"] == "telegram" :
                ccsms["image"] = "/media/custom_social_media/icons8-telegram-96.png"
            elif ccsms["type"] == "tiktok" :
                ccsms["image"] = "/media/custom_social_media/icons8-tiktok-96.png"
            elif ccsms["type"] == "twitch" :
                ccsms["image"] = "/media/custom_social_media/icons8-twitch-96.png"
            elif ccsms["type"] == "twitter" :
                ccsms["image"] = "/media/custom_social_media/icons8-twitter-96.png"
            elif ccsms["type"] == "youtube" :
                ccsms["image"] = "/media/custom_social_media/icons8-youtube-96.png"
            # Añadir el diccionario modificado a la lista
            data.append (ccsms)
        return data
