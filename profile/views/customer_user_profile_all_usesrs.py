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
from django.db.models import Q

class CustomerUserSerializerLow(serializers.ModelSerializer):
    licencia_id = LicenciaSerializer()
    customeruserprofile = CustomerUserProfileSerializer()

    class Meta:
        model = CustomerUser
        fields = (
            'id', 'email', 'phone_number', 'public_id', 'rubro', 'is_editable', 
            'date_joined', 'is_active', 'customeruserprofile', 'username', 
            'is_admin', 'licencia_id', 'is_superuser', 'dependency_id', 
            'is_sponsor', 'is_booking', 'is_sales_manager', 'is_ecommerce'
        )


class CustomerUserAllProfileViewSet(APIView):
    def get(self, request):
        search_value = request.GET.get('search_value', '')

        if not request.user.is_superuser:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        profile_service = ProfileService()

        try:
            users = profile_service.get_all_users_v2(type=None)  # Ajusta según tu lógica de obtención de usuarios

            # Filtrar usuarios según los tres campos simultáneamente usando Q objects
            users = users.filter(
                Q(username__icontains=search_value) |
                Q(id__icontains=search_value) |
                Q(email__icontains=search_value)
            )

            # Obtener otros filtros de parámetros GET
            is_active = request.GET.get('is_active')
            is_admin = request.GET.get('is_admin')
            is_superuser = request.GET.get('is_superuser')
            is_sponsor = request.GET.get('is_sponsor')
            is_booking = request.GET.get('is_booking')
            is_sales_manager = request.GET.get('is_sales_manager')
            is_ecommerce = request.GET.get('is_ecommerce')

            # Nuevo filtro para is_active=False
            is_inactive = request.GET.get('is_inactive')

            # Aplicar filtros adicionales si están presentes
            if is_active is not None:
                users = users.filter(is_active=is_active.lower() == 'true')
            if is_inactive is not None:
                users = users.filter(is_active=False)
            if is_admin is not None:
                users = users.filter(is_admin=is_admin.lower() == 'true')
            if is_superuser is not None:
                users = users.filter(is_superuser=is_superuser.lower() == 'true')
            if is_sponsor is not None:
                users = users.filter(is_sponsor=is_sponsor.lower() == 'true')
            if is_booking is not None:
                users = users.filter(is_booking=is_booking.lower() == 'true')
            if is_sales_manager is not None:
                users = users.filter(is_sales_manager=is_sales_manager.lower() == 'true')
            if is_ecommerce is not None:
                users = users.filter(is_ecommerce=is_ecommerce.lower() == 'true')

            # Ordenar usuarios por fecha de unión
            users = sorted(users, key=lambda user: user.date_joined, reverse=True)

        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Paginación como lo tienes implementado actualmente
        page_number = request.GET.get('page', 1)
        items_per_page = 100
        paginator = Paginator(users, items_per_page)
        try:
            page = paginator.page(page_number)
        except Exception as e:
            print(e)
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                    "is_booking": user["is_booking"],
                    "is_sales_manager": user["is_sales_manager"],
                    "is_ecommerce": user["is_ecommerce"],
                    "dependency_id": user["dependency_id"],
                }
            }
            data.append(new_object)

        return Response({"success": True, "data": data, "pages": paginator.num_pages}, status=status.HTTP_200_OK)