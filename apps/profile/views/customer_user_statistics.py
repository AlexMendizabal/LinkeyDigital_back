from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from apps.profile.models import CustomerUserProfile, CustomerUserCustomSocialMedia
from apps.profile.services import Profileservices,  SocialMediaservices
from apps.profile.views import customerUserUtilities
from apps.authentication.models import CustomerUser
from apps.authentication.views import CustomerUserserializers
from apps.administration.UtilitiesAdministration import UtilitiesAdm

class CustomerUserProfileStatisticsserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = ('id', 'counter', 'image', 'public_name','customer_user_id')

class CustomerUserCustomSocialMediaStatisticsserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserCustomSocialMedia
        fields = ('title', 'counter', 'image', 'type', 'url', 'created_at','update_at')

class CustomerUserStatisticsserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('username', 'rubro')


class CustomerUserStatistics(APIView):

    def get(self, request):

        user_id = request.GET.get('user_id', request.user)

        if user_id == request.user.id:
            user = request.user
        else:
            try:
                user = CustomerUser.objects.get(id=user_id)
            except Exception as e:
                return Response({"success": False, 'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, user):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        utilities = Utilities()
        profile_services = Profileservices()
        social_media_services = SocialMediaservices()

        customer_profile_serializers = utilities.get_profile(profile_services, None, user_id)
        customer_custom_social_media_serializers = utilities.get_custom_social_media(social_media_services, None,
                                                                                      user_id)

        customer_custom_social_media_serializers_formated = customer_custom_social_media_serializers if customer_custom_social_media_serializers else None

        # Obtener el ID del CustomerUserProfile
        customer_profile_id = customer_profile_serializers.id

        # Agregar id y customer_user_id al diccionario de datos devuelto
        data = {
            "id": customer_profile_id,
            "customer_user_id": user_id,
            "profile": customer_profile_serializers.counter,
            "custom_social_list": customer_custom_social_media_serializers_formated,
        }

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


class StaticsForAdminViewSet(APIView):
    def get(self, request):
        

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

        licencia_id = user.licencia_id

        utilities = Utilities()
        profile_services = Profileservices()
        social_media_services = SocialMediaservices()

        customer_profile = utilities.get_profile_and_social_medias_by_licencia(profile_services=profile_services,
                                                                               licencia_id=licencia_id,
                                                                               contact_services = social_media_services
                                                                               )
        if not customer_profile:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": customer_profile}, status=status.HTTP_200_OK)
    
class StaticsForSuperViewSet(APIView):
    def get(self, request):
        if not request.user.is_superuser:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile_services = Profileservices()
            data = profile_services.cantobjs()
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    
class Utilities():
    def get_profile(self, profile_services, pk, customer_user):
        try:
            response = profile_services.get_profile(pk, customer_user)
        except Exception as e:
            return Response(None)
        return response 

    def get_profile_and_social_medias_by_licencia(self, profile_services, contact_services, licencia_id):
        try:
            response = profile_services.get_users_by_licencia(licencia_id)
            if not response:
                return None
            profiles = []
            for usr in response:
                obj = profile_services.get_profile(customer_user=usr.id)
                obj = CustomerUserProfileStatisticsserializers(obj, many=False)
                custom = contact_services.get_custom_social_media(customer_user=usr.id)
                custom = CustomerUserCustomSocialMediaStatisticsserializers(custom,many=True)

                utilitiesC = customerUserUtilities()
                custom = utilitiesC.put_image_with_type(custom)

                user = CustomerUserStatisticsserializers(usr, many=False)
                profiles.append({   **user.data, **obj.data, "statistics": {"custom_social_list": custom}})
            return profiles

        except Exception as e:
            return Response(None)



    def get_custom_social_media(self, contact_services, pk, customer_user):
        try:
            response = contact_services.get_custom_social_media(pk, customer_user)
            metodos = customerUserUtilities()
        except Exception as e:
            return Response(None)
        customer_custom_social_media_serializers = CustomerUserCustomSocialMediaStatisticsserializers(response,
                                                                                                     many=True)
        data = metodos.put_image_with_type(customer_custom_social_media_serializers)
        return data
