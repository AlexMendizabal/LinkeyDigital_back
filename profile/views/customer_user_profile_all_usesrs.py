from rest_framework.views import APIView

from rest_framework import serializers
from profile.models import CustomerUserProfile
from authentication.models import CustomerUser
from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService


class CustomerUserAllProfileViewSet(APIView):
    def get(self, request, licencia_id=None):
        if not request.user.is_superuser : 
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        profile_service = ProfileService()
        try:
            response = profile_service.get_all_profiles()
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
    
class CustomerUserIndepProfileViewSet(APIView):
    def get(self, request, pk=None):
        profile_service = ProfileService()
        try:
            response = profile_service.get_all_profiles("independiente")
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
