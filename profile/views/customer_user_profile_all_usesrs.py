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
        # Obtener parámetros de búsqueda
        username = request.GET.get('username')
        user_id = request.GET.get('id')
        email = request.GET.get('email')
        licencia_id = request.GET.get('licencia_id')
        role = request.GET.get('role')


        if not request.user.is_superuser:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        profile_service = ProfileService()

        try:
            users = profile_service.get_all_users_v2(type=None)  # Ajusta según tu lógica de obtención de usuarios

            # Lista de filtros a aplicar
            filters = []

            if username:
                filters.append(Q(username__icontains=username))
            if user_id:
                filters.append(Q(id=user_id))
            if email:
                filters.append(Q(email__icontains=email))
            if licencia_id:
                filters.append(Q(licencia_id=licencia_id))


                # Mapeo de roles a campos de modelo
            role_mapping = {
                'is_admin': 'is_admin',
                'is_superuser': 'is_superuser',
                'is_booking': 'is_booking',
                'is_ecommerce': 'is_ecommerce',
                'is_sales_manager': 'is_sales_manager',
                'is_sponsor': 'is_sponsor',
                'is_active': 'is_active',
                'is_inactive': Q(is_active=False)
            }

            # Aplicar filtro según el rol especificado
            if role and role in role_mapping:
                filter_condition = role_mapping[role]
                if filter_condition == 'is_inactive':
                    users = users.filter(filter_condition)
                else:
                    filters.append(Q(**{filter_condition: True}))

            # Aplicar todos los filtros acumulativamente usando Q objects
            if filters:
                users = users.filter(*filters)

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
