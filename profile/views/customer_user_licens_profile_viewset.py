from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService

class CustomerUserLicensProfileViewSet(APIView):
    def get(self, request, licencia_id=None):

        if not request.user.is_admin and not request.user.is_superuser: 
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        if licencia_id and not request.user.is_superuser:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.licencia_id and not licencia_id:
            return Response({"success": False, "mensaje": "No llego ninguna licencia"},  status=status.HTTP_400_BAD_REQUEST)
        admin_id = None
        if not licencia_id:
            licencia_id = request.user.licencia_id
            admin_id = request.user.id

        profile_service = ProfileService()
        try:
            response = profile_service.get_all_profile_licencia(licencia_id, admin_id)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True, "data": response}, status=status.HTTP_200_OK)
    
