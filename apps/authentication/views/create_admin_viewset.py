from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from apps.administration.views.licencias_viewset import Licenciaserializers, Utilities
from apps.administration.services import Licenciaservices

class CreateAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("DEBUG user:", request.user)
        print("DEBUG is_authenticated:", request.user.is_authenticated)
        print("DEBUG is_staff:", request.user.is_staff)
        print("DEBUG is_superuser:", request.user.is_superuser)

        if not request.user.is_superuser:
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        username = request.data.get("username")
        correo = request.data.get("correo")
        esEmpresa = request.data.get("esEmpresa", True)
        tipo_de_plan = request.data.get("tipo_de_plan")
        duracion = request.data.get("duracion")
        cobro = request.data.get("cobro")
        status_plan = request.data.get("status")
        fecha_inicio = request.data.get("fecha_inicio") or timezone.now()

        if not correo:
            return Response({"mensaje": "El email es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        # Validar datos mínimos de licencia
        missing = [k for k, v in {"tipo_de_plan": tipo_de_plan, "duracion": duracion, "cobro": cobro, "status": status_plan}.items() if v in (None, "")] 
        if missing:
            return Response({"mensaje": f"Faltan campos de licencia: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        rubro = "empresa" if esEmpresa else "independiente"
        User = get_user_model()
        if User.objects.filter(email=correo).exists():
            return Response({"mensaje": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        # 🔹 Definir username dinámicamente
        final_username = username if username else correo.split('@')[0]
        # Crear usuario empresa admin
        user = User.objects.create(
            email=correo,
            username=final_username,
            password=make_password(request.data.get("password")) if request.data.get("password") else None,
            rubro=rubro,
            # imagino que is_staff es para registrar consultores del sistema,
            # por defecto que sea false, más adelante se lo puede habilitar
            is_staff=False,
            is_superuser=False,
            is_admin=esEmpresa, 
        )
        # Crear y enlazar licencia
        payload = {
            'customer_user_admin': user.id,
            'tipo_de_plan': tipo_de_plan,
            'fecha_inicio': fecha_inicio,
            'cobro': cobro,
            'duracion': duracion,
            'status': status_plan,
        }
        serializer = Licenciaserializers(data=payload)
        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        utilities = Utilities()
        dto = utilities.buid_dto_from_validated_data(serializer)
        licenciaservices = Licenciaservices()
        licencia = licenciaservices.createLicencia(dto, customer_user_admin=user.id, admin=esEmpresa)
        # Respuesta
        licencia_data = Licenciaserializers(licencia).data
        licencia_data = licencia_data.copy()
        licencia_data['fecha_fin'] = utilities.calcular_fecha_fin(licencia_data['fecha_inicio'], licencia_data['duracion'])
        return Response({
            "mensaje": "Admin creado exitosamente",
            "user_id": user.id,
            "licencia_id": licencia.id,
            "licencia": licencia_data
        }, status=status.HTTP_201_CREATED)






