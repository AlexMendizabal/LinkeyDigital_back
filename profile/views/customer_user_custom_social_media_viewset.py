import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from profile.models import CustomerUserCustomSocialMedia, CustomSocialMediaDto
from profile.services import SocialMediaService

from authentication.models import CustomerUser
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import transaction
import json

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
            utilitiesC = customerUserUtilities()
            data = utilitiesC.put_image_with_type(customer_custom_social_media_serializers)

            return Response({"success": True, "data": data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request):
        data = request.data.copy()
        data["customer_user"] = request.user.id
        if 'type' not in data :
            data["type"] = "socialMedia"
        serializer = CustomerUserCustomSocialMediaSerializer(data=data)


        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        utilities = customerUserUtilities()
        dto = utilities.buid_dto_from_validated_data(serializer)
        social_media_service = SocialMediaService()

        try:
            response = social_media_service.create_custom_social_media(dto)
            if 'type' in data and data['type'] == 'image':
                if 'imageQR' in data and not isinstance(data['imageQR'], str):
                    try:
                        response = utilities.replace_url_in_image_type(data,response)
                        response.save()
                    except Exception as e:
                        print(e)
                        return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=False)
        utilitiesC = customerUserUtilities()
        data = utilitiesC.put_image_with_type(customer_custom_social_media_serializers)
        return Response({"success": True, "data": data},
                        status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, id=pk)

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

        if 'type' in request.data and request.data['type'] == 'image':
            if 'imageQR' in request.data and not isinstance(request.data['imageQR'], str):
                try:
                    utilities = customerUserUtilities()
                    customer_user_custom_social_media = utilities.replace_url_in_image_type(request.data,customer_user_custom_social_media)
                except Exception as e:
                    print(e)
                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        customer_user_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(
            instance=customer_user_custom_social_media,
            data=request.data, partial=True)

        customer_user_custom_social_media_serializers.is_valid(raise_exception=True)
        customer_user_custom_social_media_serializers.save()

        return Response({"success": True, "data": customer_user_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)

    #WAITING: se debe cambiar la logica de borrado... de manera que en lugar de guardar 
    # img por img se guarde una y vaya preguntando si hay otro registro que aun usa esa msima foto

    def delete (self, request, pk=None):
        # type -> image 
        # borrar de url
        social_media_service = SocialMediaService()
        try:
            response = social_media_service.delete_custom_social_media(pk, request.user.id)
            return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
   
    
class CustomerUserCustomSocialMediaByUserViewSet(APIView):
    # retorna los custom social media del usuario que se mande
    def get(self, request, user_id=None):
        try:
            if not request.user.is_admin:
                return Response({"succes": False, "mensaje": "No tienes permisos"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            social_media_service = SocialMediaService()
            try:
                response = social_media_service.get_custom_social_media(customer_user = user_id)
            except Exception as e:
                return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

            customer_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=True)
            return Response({"success": True, "data": customer_custom_social_media_serializers.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
# crea los social media para los usuarios de la licencia 
    def post(self, request, user_id=None, pk=None):
        if not request.user.is_admin and not request.user.is_superuser:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        customer_user_custom_social_media = get_object_or_404(CustomerUser,
                                                              id=user_id)
        
        data = request.data.copy()
        data["customer_user"] = customer_user_custom_social_media.id
        if 'type' not in data :
            data["type"] = "socialMedia"
        serializer = CustomerUserCustomSocialMediaSerializer(data=data)

        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        utilities = customerUserUtilities()
        dto = utilities.buid_dto_from_validated_data(serializer)
        social_media_service = SocialMediaService()

        try:
            response = social_media_service.create_custom_social_media(dto)
            if 'type' in data and data['type'] == 'image':
                if 'imageQR' in data and not isinstance(data['imageQR'], str):
                    try:
                        response = utilities.replace_url_in_image_type(data,response)
                        response.save()
                    except Exception as e:
                        print(e)
                        return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(response, many=False)
        return Response({"success": True, "data": customer_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)
# actualizar los custom social media para los usuarios en la licencia 
    def put(self, request, user_id=None ,pk=None):
        if not request.user.is_admin and not request.user.is_superuser:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia,
                                                              id=pk)

        if user_id != customer_user_custom_social_media.customer_user_id:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        if 'image' in request.data and customer_user_custom_social_media.image != "custom_social_media/undefined.png":
            try:
                os.remove(customer_user_custom_social_media.image.path)
            except Exception as e:
                pass

        if 'title' in request.data:
            if request.data.get('title').replace(" ", "") == "":
                CustomerUserCustomSocialMedia.objects.filter(customer_user=user_id, pk=pk).delete()
                return Response({"success": True})

        if 'url' in request.data:
            if request.data.get('url').replace(" ", "") == "":
                CustomerUserCustomSocialMedia.objects.filter(customer_user=user_id, pk=pk).delete()
                return Response({"success": True})
        
        if 'type' in request.data and request.data['type'] == 'image':
            if 'imageQR' in request.data and not isinstance(request.data['imageQR'], str):
                try:
                    utilities = customerUserUtilities()
                    customer_user_custom_social_media = utilities.replace_url_in_image_type(request.data,customer_user_custom_social_media)
                except Exception as e:
                    print(e)
                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        customer_user_custom_social_media_serializers = CustomerUserCustomSocialMediaSerializer(
            instance=customer_user_custom_social_media,
            data=request.data, partial=True)

        customer_user_custom_social_media_serializers.is_valid(raise_exception=True)
        customer_user_custom_social_media_serializers.save()

        return Response({"success": True, "data": customer_user_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)
    
    def delete (self, request, user_id=None ,pk=None):

        social_media_service = SocialMediaService()
        try:
            response = social_media_service.delete_custom_social_media(pk, user_id)
            return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

# metodos para creacion masiva de custom_user_social_media
# estos metodos se usan igual que la clase anterior pero se pasa una coleccion de ids
class CustomerUserCustomSocialMediaByAllUserViewSet(APIView):
    def post(self, request):
        if not request.user.is_admin:
            return Response({"success": False, "error": "No tienes permisos de administrador."},
                            status=status.HTTP_403_FORBIDDEN)
        
        try:
            ids = json.loads(request.data.get("ids", []))
            customer_user_list = CustomerUser.objects.filter(id__in=ids,licencia_id_id=request.user.licencia_id)

        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        
        #responses = []
        
        with transaction.atomic():
            for user in customer_user_list:
                data_copy = request.data.copy()
                data_copy["customer_user"] = user.id
                
                if 'type' not in data_copy:
                    data_copy["type"] = "socialMedia"
                                
                serializer = CustomerUserCustomSocialMediaSerializer(data=data_copy)

                if serializer.is_valid():
                    utilities = customerUserUtilities()
                    dto = utilities.buid_dto_from_validated_data(serializer)
                    social_media_service = SocialMediaService()

                    try:
                        response = social_media_service.create_custom_social_media(dto)
                        if 'type' in request.data and request.data['type'] == 'image':
                            if 'imageQR' in request.data and not isinstance(request.data['imageQR'], str):
                                try:
                                    response = utilities.replace_url_in_image_type(data_copy,response)
                                    response.save()
                                except Exception as e:
                                    print(e)
                                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

                        #responses.append(response)
                    except Exception as e:
                        print(e)
                        return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # if not responses:
        #     return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        
        #customer_custom_social_media_serializer = CustomerUserCustomSocialMediaSerializer(responses, many=True)
        return Response({
            "success": True
        }, status=status.HTTP_200_OK)

class customerUserUtilities():

    def put_image_with_type(self, customer_custom_social_media):
        type_mapping = {
                "whatsapp": "icons8-whatsapp-96.png",
                "facebook": "icons8-facebook-96.png",
                "github": "icons8-github-96.png",
                "gitlab": "icons8-gitlab-96.png",
                "maps": "icons8-google-maps-old-96.png",
                "instagram": "icons8-instagram-96.png",
                "linkedin": "icons8-linkedin-96.png",
                "correo": "icons8-mail-96.png",
                "phone": "icons8-phone-96.png",
                "skype": "icons8-skype-96.png",
                "snapchat": "icons8-snapchat-96.png",
                "spotify": "icons8-spotify-96.png",
                "telegram": "icons8-telegram-96.png",
                "tiktok": "icons8-tiktok-96.png",
                "twitch": "icons8-twitch-96.png",
                "twitter": "icons8-twitter-96.png",
                "youtube": "icons8-youtube-96.png",
            }
        if isinstance(customer_custom_social_media.data, list):
            # Si es una colección de objetos
            data = []
            for ccsms in customer_custom_social_media.data:
                if ccsms["type"] in type_mapping:
                    ccsms["image"] = f"/media/custom_social_media/{type_mapping[ccsms['type']]}"
                data.append(ccsms)
            return data
        else:
            # Si es un solo objeto
            ccsms = customer_custom_social_media.data
            if ccsms["type"] in type_mapping:
                ccsms["image"] = f"/media/custom_social_media/{type_mapping[ccsms['type']]}"
            return ccsms
        
    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return CustomSocialMediaDto(
            customer_user=data["customer_user"],
            title=data["title"],
            url=data["url"],
            is_active=True,
            is_visible=data["is_visible"],
            type=data["type"],
            image=data.get("image", None),
        )

    def replace_url_in_image_type(self, data, customer_user_custom_social_media):

        try:
            if not customer_user_custom_social_media.url.endswith("custom_social_media/undefined.png") and not customer_user_custom_social_media.url.startswith("http"):
                os.remove(os.path.normpath(os.path.join(settings.MEDIA_ROOT, customer_user_custom_social_media.url.replace(settings.MEDIA_URL, ''))))
        except Exception as e:
            print(e)
            pass
        imagen = data['imageQR']
        nombre_imagen = imagen.name.replace(" ", "")
        ruta_imagen = default_storage.save('custom_social_media/' + nombre_imagen, imagen)
        new_url = settings.MEDIA_URL + ruta_imagen
        customer_user_custom_social_media.url = new_url
        return customer_user_custom_social_media
