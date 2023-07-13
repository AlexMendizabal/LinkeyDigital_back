from django.contrib.auth import get_user_model
from administration.models import Licencia
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.exceptions import FirebaseAuthException, TokenNotFound
from administration.views import Utilities, LicenciaSerializer
from administration.services import LicenciaService
from ..views import CustomerUserSerializer

class CreateAdmin(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            raise TokenNotFound()
        
        correo = request.data.get("correo", None)
        rubro = request.data.get("esEmpresa", None)
        # tipo_de_plan = request.data.get("tipo_de_plan", None)
        # cobro = request.data.get("cobro", None)
        # duracion = request.data.get("duracion", None)
        # fecha_inicio = request.data.get("fecha_inicio", None)
        # estado = request.data.get("status", None)

        if not correo  or rubro is None: #or not tipo_de_plan or not cobro or not duracion or not fecha_inicio or not estado
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        
        rubro = "empresa" if rubro else "independiente"


        username = correo.split('@')[0]
        User = get_user_model()
        try:
            user = auth.create_user(
                email=correo,
                password=username
            )
            uid = user.uid            
        except Exception as e:
            return Response({"success": "Firebase Auth Exception", "error" : str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:
            user = User.objects.create(uid=uid, email=correo, username=username, rubro=rubro)
            
            try:
                utilitiesLicencia = Utilities()
                request.data["customer_user_admin"] = user.id
                serializer = LicenciaSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                serializer.data["customer_user_admin"] = user
                dto = utilitiesLicencia.buid_dto_from_validated_data(serializer)
                licenciaService = LicenciaService()    
                licencia = licenciaService.createLicencia(dto,user.id)

                user = User.objects.get(id=user.id)
            except Exception as e:
                auth.delete_user(user.uid)
                User.objects.filter(uid=uid).delete()
                return Response({"success": False, "error al crear licencia" : str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            licencia_serializers = LicenciaSerializer(licencia, many=False)
            user_serializers = CustomerUserSerializer(user, many=False)
                
        except Exception as e:
            auth.delete_user(user.uid)
            User.objects.filter(uid=uid).delete()
            return Response({"status": "error al crear usuario", "error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": True, "Licencia": licencia_serializers.data, "Usuario": user_serializers.data}, 
                        status=status.HTTP_200_OK)
        
        

        

        
