import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers
from apps.profile.models import CustomerUserProfile, ProfileDto
from rest_framework.response import Response
from rest_framework import status

from apps.profile.services import Profileservices
from apps.administration.UtilitiesAdministration import UtilitiesAdm


class CustomerUserProfileserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = (
            'customer_user', 'career', 'public_name', 'description', 'color', 'background',
            'image')


class CustomerUserProfileViewSet(APIView):
    def get(self, request, pk=None):
        profile_services = Profileservices()
        try:
            response = profile_services.get_profile(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileserializers(response, many=False)
        return Response({"success": True, "data": customer_profile_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id

        try:
            instance = CustomerUserProfile.objects.get(customer_user=request.user.id)
        except Exception as e:
            instance = None

        serializers = CustomerUserProfileserializers(instance, data=request.data)
        if not serializers.is_valid():
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

        utilities = UtilitiesProfile()
        dto = utilities.buid_dto_from_validated_data(serializers)
        profile_services = Profileservices()

        try:
            response = profile_services.create_profile(dto)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_email_serializers = CustomerUserProfileserializers(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)
    
    def put(self, request):

        user_id = request.GET.get('user_id', request.user.id)
        customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=user_id)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, customer_user_profile.customer_user ):
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

        customer_user_profile_serializers = CustomerUserProfileserializers(
            instance=customer_user_profile,
            data=request.data, partial=True)

        customer_user_profile_serializers.is_valid(raise_exception=True)
        customer_user_profile_serializers.save()

        return Response({"success": True, "data": customer_user_profile_serializers.data}, status=status.HTTP_200_OK)
    

class CustomerUserProfileForAdmViewSet(APIView):
    def get(self, request, customer_user=None):
        profile_services = Profileservices()
        try:
            response = profile_services.get_profile(customer_user)

            utilitiesAdm = UtilitiesAdm()
            if not utilitiesAdm.hasPermision(request.user, customer_user ):
                return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_profile_serializers = CustomerUserProfileserializers(response, many=False)
        return Response({"success": True, "data": customer_profile_serializers.data}, status=status.HTTP_200_OK)

    def put(self, request, customer_user=None):
        customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, customer_user_profile.customer_user_id ):
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

        customer_user_profile_serializers = CustomerUserProfileserializers(
            instance=customer_user_profile,
            data=request.data, partial=True)

        customer_user_profile_serializers.is_valid(raise_exception=True)
        customer_user_profile_serializers.save()

        return Response({"success": True, "data": customer_user_profile_serializers.data}, status=status.HTTP_200_OK)

    
    
class UtilitiesProfile ():
    def buid_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
        return ProfileDto(
            customer_user=data["customer_user"],
            public_id=data["public_id"],
            career=data["career"],
            public_name=data["public_name"],
            description=data["description"],
        )
