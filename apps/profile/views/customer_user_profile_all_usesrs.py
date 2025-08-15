from rest_framework.views import APIView
from rest_framework import serializers
from apps.profile.models import CustomerUserProfile
from apps.authentication.models import CustomerUser
from rest_framework.response import Response
from rest_framework import status
from apps.profile.services import Profileservices
from django.core.paginator import Paginator
from rest_framework import status
from apps.administration.views.licencias_viewset import Licenciaserializers
from apps.profile.views.customer_user_profile_viewset import CustomerUserProfileserializers
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class CustomerUserserializersLow(serializers.ModelSerializer):
    licencia_id = Licenciaserializers()
    customeruserprofile = CustomerUserProfileserializers()

    class Meta:
        model = CustomerUser
        fields = (
            'id', 'email', 'phone_number', 'public_id', 'rubro', 'is_editable', 
            'date_joined', 'is_active', 'customeruserprofile', 'username', 
            'is_admin', 'licencia_id', 'is_superuser', 'dependency_id', 
            'is_sponsor', 'is_booking', 'is_sales_manager', 'is_ecommerce'
        )


@method_decorator(csrf_exempt, name='dispatch')
class CustomerUserAllProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Verificar permisos de administrador o superusuario
        if not (hasattr(request.user, 'is_admin') and request.user.is_admin) and not (hasattr(request.user, 'is_superuser') and request.user.is_superuser):
            return Response({"success": False, "error": "Permisos insuficientes"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener parámetros de búsqueda
        username = request.GET.get('username')
        user_id = request.GET.get('id')
        email = request.GET.get('email')
        licencia_id = request.GET.get('licencia_id')
        role = request.GET.get('role')
        include_without_license = request.GET.get('include_without_license') in ('1', 'true', 'True')

        profile_services = Profileservices()

        try:
            # Base: usuarios con licencia
            users = CustomerUser.objects.all()
            # Restringir por ámbito del admin actual si no es superuser
            if not request.user.is_superuser:
                # Empresas de mi licencia o donde soy admin
                users = users.filter(Q(licencia_id=request.user.licencia_id_id) | Q(licencia_id__customer_user_admin_id=request.user.id))
            # Por defecto, requerimos licencia enlazada salvo que se pida incluir sin licencia
            if not include_without_license:
                users = users.filter(licencia_id__isnull=False)

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
                'is_inactive': Q(is_active=False),
                'todos': None  # Añadir soporte para 'todos' = sin filtro adicional
            }

            # Aplicar filtro según el rol especificado
            if role and role in role_mapping and role != 'todos':
                filter_condition = role_mapping[role]
                if role == 'is_inactive':
                    users = users.filter(filter_condition)
                else:
                    filters.append(Q(**{filter_condition: True}))

            # Aplicar todos los filtros acumulativamente usando Q objects
            if filters:
                users = users.filter(*filters)

            # Ordenar usuarios por más recientes primero: por fecha_inicio de licencia si existe, sino por id desc
            users = users.order_by('-licencia_id__fecha_inicio', '-id')

        except Exception as e:
            return Response({"success": False, "error": "Error interno del servidor"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        page_number = request.GET.get('page', 1)
        items_per_page = 100
        paginator = Paginator(users, items_per_page)
        try:
            page = paginator.page(page_number)
        except Exception as e:
            return Response({"success": False, "error": "Página no válida"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializers = CustomerUserserializersLow(page, many=True)

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
