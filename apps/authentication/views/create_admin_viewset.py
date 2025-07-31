from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class CreateAdmin(APIView):
    permission_classes = []

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        correo = request.data.get("correo")
        esEmpresa = request.data.get("esEmpresa")
        rubro = "empresa" if esEmpresa else "independiente"
        User = get_user_model()
        if User.objects.filter(email=correo).exists():
            return Response({"mensaje": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=correo,
            username=correo.split('@')[0],
            password=make_password(correo),
            rubro=rubro,
            is_staff=True,
            is_superuser=True
        )
        return Response({"mensaje": "Admin creado exitosamente", "user_id": user.id}, status=status.HTTP_201_CREATED)
        # El siguiente bloque estaba mal indentado, lo ajustamos:
        # Si necesitas lógica de licencia, descomenta y ajusta:
        # serializers = Licenciaserializers(data=request.data)
        # if not serializers.is_valid():
        #     return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        # serializers.data["customer_user_admin"] = user
        # dto = utilitiesLicencia.buid_dto_from_validated_data(serializers)
        # licenciaservices = Licenciaservices()    
        # licencia = licenciaservices.createLicencia(dto,user.id, is_admin)
        # user = User.objects.get(id=user.id)
        # licencia_serializers = Licenciaserializers(licencia, many=False)
        # user_serializers = CustomerUserserializers(user, many=False)
        # return Response({"success": True, "Licencia": licencia_serializers.data, "Usuario": user_serializers.data}, status=status.HTTP_200_OK)
        
        return Response({"success": True, "Licencia": licencia_serializers.data, "Usuario": user_serializers.data}, 
                        status=status.HTTP_200_OK)
        
        

        

        
