from rest_framework.views import APIView

from rest_framework import serializers
from profile.models import CustomerUserProfile
from authentication.models import CustomerUser
from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService

from django.core.paginator import Paginator
from rest_framework import status

class CustomerUserAllProfileViewSet(APIView):
    def get(self, request):
        type = request.GET.get('type', None)

        if not request.user.is_superuser : 
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile_service = ProfileService()
        try:
            response = profile_service.get_all_profiles(type)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
         # Paginación
        page_number = request.GET.get('page', 1)  # Obtener el número de página de la consulta GET
        items_per_page = 10  # Número de perfiles a mostrar por página
        paginator = Paginator(response, items_per_page)

        try:
            profiles = paginator.page(page_number)
        except Exception as e:
            print(e)
            profiles = paginator.page(paginator.num_pages)  # Mostrar la última página si está fuera de rango
       
        return Response({"success": True,  "data": profiles.object_list}, status=status.HTTP_200_OK)
    
