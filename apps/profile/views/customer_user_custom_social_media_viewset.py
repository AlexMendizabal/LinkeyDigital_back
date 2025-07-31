import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from apps.profile.models import CustomerUserCustomSocialMedia, CustomSocialMediaDto
from apps.profile.services import SocialMediaservices

from apps.authentication.models import CustomerUser
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import transaction
import json
from apps.administration.UtilitiesAdministration import UtilitiesAdm

from django.core.exceptions import ValidationError

class CustomerUserCustomSocialMediaserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = (
            'id', 'customer_user', 'title', 'url', 'image', 'is_active', 'is_visible', 'type', 'order')
        extra_kwargs = {'title': {'required': True}, 'url': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserCustomSocialMediaViewSet(APIView):
    def get(self, request, pk=None):
        try:
            user_id = request.GET.get('user_id', request.user.id)

            social_media_services = SocialMediaservices()
            try:
                response = social_media_services.get_custom_social_media(pk, user_id)
            except Exception as e:
                return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

            customer_custom_social_media_serializers = CustomerUserCustomSocialMediaserializers(response, many=True)
            utilitiesC = customerUserUtilities()
            data = utilitiesC.put_image_with_type(customer_custom_social_media_serializers)

            return Response({"success": True, "data": data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
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
        try:
            data = request.data.copy()
        except Exception as e:
            data = request.data

        data["customer_user"] = user.id
        if 'type' not in data :
            data["type"] = "socialMedia"
        serializers = CustomerUserCustomSocialMediaserializers(data=data)


        if not serializers.is_valid():
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        utilities = customerUserUtilities()
        dto = utilities.buid_dto_from_validated_data(serializers)
        social_media_services = SocialMediaservices()

        try:
            with transaction.atomic():
                response = social_media_services.create_custom_social_media(dto)
                if 'type' in data and data['type'] == 'image':
                    if 'imageQR' in data and not isinstance(data['imageQR'], str):

                            response = utilities.replace_url_in_image_type(data,response)
                            response.save()
                elif 'type' in data and data['type'] == 'file':
                    if 'file' in data and not isinstance(data['file'], str):

                            response = utilities.replace_url_in_file_type(data,response)
                            response.save()
        except Exception as e:
            return Response({"success": False, "error" : str(e)}, status=status.HTTP_404_NOT_FOUND)

        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaserializers(response, many=False)
        utilitiesC = customerUserUtilities()
        data = utilitiesC.put_image_with_type(customer_custom_social_media_serializers)
        return Response({"success": True, "data": data},
                        status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        customer_user_custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, id=pk)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, customer_user_custom_social_media.customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        if 'image' in request.data and customer_user_custom_social_media.image != "custom_social_media/undefined.png":
            try:
                os.remove(customer_user_custom_social_media.image.path)
            except Exception as e:
                pass

        if 'type' in request.data and request.data['type'] == 'image':
            if 'imageQR' in request.data and not isinstance(request.data['imageQR'], str):
                try:
                    utilities = customerUserUtilities()
                    customer_user_custom_social_media = utilities.replace_url_in_image_type(request.data,customer_user_custom_social_media)
                except Exception as e:
                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
                
        elif 'type' in request.data and request.data['type'] == 'file':
            if 'file' in request.data and not isinstance(request.data['file'], str):
                try:
                    utilities = customerUserUtilities()
                    customer_user_custom_social_media = utilities.replace_url_in_file_type(request.data,customer_user_custom_social_media)
                except Exception as e:
                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
            else: 
                return Response({"success": False, "msg" : "Se solicito type file pero no se encontro un file"}, status=status.HTTP_400_BAD_REQUEST)

        customer_user_custom_social_media_serializers = CustomerUserCustomSocialMediaserializers(
            instance=customer_user_custom_social_media,
            data=request.data, partial=True)

        customer_user_custom_social_media_serializers.is_valid(raise_exception=True)
        customer_user_custom_social_media_serializers.save()

        return Response({"success": True, "data": customer_user_custom_social_media_serializers.data},
                        status=status.HTTP_200_OK)

    def delete (self, request, pk=None):
        social_media_services = SocialMediaservices()

        utilitiesAdm = UtilitiesAdm()
        custom_social_media = get_object_or_404(CustomerUserCustomSocialMedia, id=pk)
        if not utilitiesAdm.hasPermision(request.user, custom_social_media.customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            social_media_services.delete_custom_social_media(cusm = custom_social_media)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

# metodos para creacion masiva de custom_user_social_media
# estos metodos se usan igual que la clase anterior pero se pasa una coleccion de ids
class CustomerUserCustomSocialMediaByAllUserViewSet(APIView):
    def post(self, request):

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, request.user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            ids = json.loads(request.data.get("ids", []))
            customer_user_list = CustomerUser.objects.filter(id__in=ids)

        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        
        #responses = []
        
        with transaction.atomic():
            for user in customer_user_list:
                data_copy = request.data.copy()
                data_copy["customer_user"] = user.id
                
                if 'type' not in data_copy:
                    data_copy["type"] = "socialMedia"
                                
                serializers = CustomerUserCustomSocialMediaserializers(data=data_copy)

                if serializers.is_valid():
                    utilities = customerUserUtilities()
                    dto = utilities.buid_dto_from_validated_data(serializers)
                    social_media_services = SocialMediaservices()

                    try:
                        response = social_media_services.create_custom_social_media(dto)
                        if 'type' in request.data and request.data['type'] == 'image':
                            if 'imageQR' in request.data and not isinstance(request.data['imageQR'], str):
                                try:
                                    response = utilities.replace_url_in_image_type(data_copy,response)
                                    response.save()
                                except Exception as e:
                                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

                        #responses.append(response)
                    except Exception as e:
                        return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        # if not responses:
        #     return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        
        #customer_custom_social_media_serializers = CustomerUserCustomSocialMediaserializers(responses, many=True)
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
                "contact": "icons8-contact-96.png",
                "store": "icons8-store-96.png",
                "mainLink": "icons8-estrellas-64.png",
                "file": "icons8-carpeta-96.png",

            }
        if isinstance(customer_custom_social_media.data, list):
            # Si es una colección de objetos
            data = []
            for ccsms in customer_custom_social_media.data:
                if ccsms["type"] in type_mapping and ccsms["image"] == "/media/custom_social_media/undefined.png" :
                    ccsms["image"] = f"/media/custom_social_media/{type_mapping[ccsms['type']]}"
                data.append(ccsms)
            return data
        else:
            # Si es un solo objeto
            ccsms = customer_custom_social_media.data
            if ccsms["type"] in type_mapping and ccsms["image"] == "/media/custom_social_media/undefined.png":
                ccsms["image"] = f"/media/custom_social_media/{type_mapping[ccsms['type']]}"
            return ccsms
        
    def buid_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
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
            if not customer_user_custom_social_media.url.endswith("custom_social_media/undefined.png") and not self.is_safe_url(customer_user_custom_social_media.url):
                os.remove(os.path.normpath(os.path.join(settings.MEDIA_ROOT, customer_user_custom_social_media.url.replace(settings.MEDIA_URL, ''))))
        except Exception as e:
            pass
        imagen = data['imageQR']
        nombre_imagen = imagen.name.replace(" ", "")
        ruta_imagen = default_storage.save('custom_social_media/' + nombre_imagen, imagen)
        new_url = settings.MEDIA_URL + ruta_imagen
        customer_user_custom_social_media.url = new_url
        return customer_user_custom_social_media
    
    
    def replace_url_in_file_type(self, data, cucsm):
        try:
            # Validación de tipos de URL no seguros
            if not self.is_safe_url(cucsm.url):
                self.delete_invalid_file(cucsm.url)
        except Exception as e:
            pass
        
        file = data['file']
        
        # Validación de tipo de archivo permitido y tamaño máximo
        if not self.is_valid_file_type(file):
            raise ValidationError("Tipo de archivo no permitido.")
        if not self.is_valid_file_size(cucsm.customer_user, file.size, cucsm.id ):
            raise ValidationError("Memoria de usuario llena")
        
        nombre_file = file.name.replace(" ", "")
        ruta_file = default_storage.save('files/' + nombre_file, file)
        new_url = settings.MEDIA_URL + ruta_file
        cucsm.url = new_url
        return cucsm
            
    def is_safe_url(self, url):
        return url.startswith(("http://", "https://", "tel:", "www", "mailto:"))

    def delete_invalid_file(self, url):
        try:
            if url.startswith(settings.MEDIA_URL):
                file_path = url.replace(settings.MEDIA_URL, "")
                os.remove(os.path.normpath(os.path.join(settings.MEDIA_ROOT, file_path)))
        except Exception as e:
            pass

    def is_valid_file_type(self, file):
        allowed_extensions = ["pdf", "docx", "pptx", "pptm", "ppt", "doc"]  # Agrega las extensiones permitidas
        return file.name.split(".")[-1].lower() in allowed_extensions

    def is_valid_file_size(self, userPK, sizeFile, idcucsm):
        objs = CustomerUserCustomSocialMedia.objects.filter(type="file",customer_user=userPK ).exclude(id=idcucsm)
        max =  20 * 1024 * 1024  #expresando en MB
        AlmacenamientoUsado = sizeFile
        try:
            for cucsm in objs:
                file_path_relative =  cucsm.url.replace(settings.MEDIA_URL, "")
                file_path_absolute = os.path.normpath(os.path.join(settings.MEDIA_ROOT, file_path_relative))
                if os.path.exists(file_path_absolute):
                    file_size_bytes = os.path.getsize( file_path_absolute)
                    file_size_mb = file_size_bytes #/ (1024 * 1024)  
                    AlmacenamientoUsado += file_size_mb
                else: 
                    social_media_services = SocialMediaservices()
                    social_media_services.delete_custom_social_media(cusm = cucsm)

        except Exception as e:
            return False
        
        return AlmacenamientoUsado <= max


