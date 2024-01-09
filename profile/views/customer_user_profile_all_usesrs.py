from rest_framework.views import APIView

from rest_framework import serializers
from profile.models import CustomerUserProfile
from authentication.models import CustomerUser
from rest_framework.response import Response
from rest_framework import status

from profile.services import ProfileService

from django.core.paginator import Paginator
from rest_framework import status

from administration.views import LicenciaSerializer
from profile.views import CustomerUserProfileSerializer

class CustomerUserSerializerLow(serializers.ModelSerializer):
    licencia_id = LicenciaSerializer()
    customeruserprofile = CustomerUserProfileSerializer()
    class Meta:
        model = CustomerUser
        fields = (
            'id','email', 'phone_number','public_id', 'rubro', 'is_editable', 'date_joined', 'is_active', 'customeruserprofile', 'username', 'is_admin', 'licencia_id', 'is_superuser','dependency_id','is_sponsor')


class CustomerUserAllProfileViewSet(APIView):
    def get(self, request):
        type = request.GET.get('type', None)

        if not request.user.is_superuser : 
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile_service = ProfileService()

        try:
            #response = profile_service.get_all_profiles(type)

            users = profile_service.get_all_users_v2(type=type)

        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
         # Paginación
        page_number = request.GET.get('page', 1)  # Obtener el número de página de la consulta GET
        items_per_page = 2000  # Número de perfiles a mostrar por página
        paginator = Paginator(users, items_per_page)
        try:
            page = paginator.page(page_number)
        except Exception as e:
            print(e)
        user_serializers = CustomerUserSerializerLow(page, many=True)

        data = []
        for user in user_serializers.data:
            new_object = {
                "licencia": user["licencia_id"],
                "profile": user["customeruserprofile"],
                "custom_user": {
                    "id": user["id"],
                    "rubro": user["rubro"],
                    "is_admin": user["is_admin"],
                    "username": user["username"],
                    "email": user["email"],
                    "is_editable": user["is_editable"],
                    "date_joined": user["date_joined"],
                    "phone_number": user["phone_number"],
                    "is_superuser": user["is_superuser"],
                    "public_id": user["public_id"],
                    "is_sponsor": user["is_sponsor"],
                    "dependency_id": user["dependency_id"],
                }
            }
            data.append(new_object)
        return Response({"success": True,  "data": data, "pages": paginator.num_pages}, status=status.HTTP_200_OK)
    
