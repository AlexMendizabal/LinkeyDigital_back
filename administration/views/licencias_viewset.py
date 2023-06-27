from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from administration.models import Licencia
from administration.services import LicenciaService

from authentication.views import CustomerUserSerializer

from django.utils import timezone
import datetime

class LicenciaSerializer(serializers.ModelSerializer):
    fecha_fin = serializers.CharField (default="No definida")
    class Meta:
        model = Licencia
        fields = (
            'id', 'customer_user_admin', 'tipo_de_plan', 'fecha_fin', 'fecha_inicio', 'cobro', 'duracion','status')
        extra_kwargs = {'cobro': {'required': True}, 
                        'duracion': {'required': True}}
        read_only_fields = ('fecha_fin',)
        
# apartado para usuarios genericos  
class LicenciaViewSet(APIView):
    #retorna la licencia a la que el usuario pertenece
    def get(self, request):
        if request.user.licencia_id is None:
            return Response({"succes": False, "message": "El usuario no tiene licencia_id"}, status=status.HTTP_404_NOT_FOUND)
        licencia_service = LicenciaService()
        try:
            response = licencia_service.get_licencia(request.user.licencia_id_id)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        licenciaSerializers = LicenciaSerializer(response, many=False)

        #####   proceso para agregar fecha fin al objeto 
        fecha_inicio = datetime.datetime.strptime(licenciaSerializers.data['fecha_inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
        fecha_fin = fecha_inicio + datetime.timedelta (days=licenciaSerializers.data['duracion'])
        fecha_fin_str = fecha_fin.strftime ("%Y-%m-%dT%H:%M:%S.%fZ")
        licenciaSerializers.data['fecha_fin'] = fecha_fin_str

        # Crear un nuevo diccionario con los datos del serializador
        data = licenciaSerializers.data.copy ()
        # Agregar el campo fecha_fin al diccionario
        data ['fecha_fin'] = fecha_fin_str
        return Response({"success": True, "data": data }, status=status.HTTP_200_OK)
    

#apartado para usuarios administradores 
class LicenciaAdminViewSet(APIView):
    #retorna los usuarios adjuntados a la licencia del admin
    def get(self, request):
        if request.user.licencia_id is None:
            return Response({"success": False, "message": "El usuario no tiene licencia"}, status=status.HTTP_404_NOT_FOUND)
        if not (request.user.is_admin):
            return Response({"success": False, "message": "Acceso negado"}, status=status.HTTP_404_NOT_FOUND)
        licencia_service = LicenciaService()
        try:
            response = licencia_service.get_Users(request.user.licencia_id_id,request.user.id )
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        licenciaSerializers = CustomerUserSerializer(response, many=True)
        return Response({"success": True, "data": licenciaSerializers.data  }, status=status.HTTP_200_OK)
  
# apartado para los super usuarios
class LicenciaSuperViewSet(APIView):
    def get(self, request, pk=None):
        if request.user.is_superuser == 0:
            return Response({"succes": False, "message": "El usuario no tiene acceso"}, status=status.HTTP_404_NOT_FOUND)
        licencia_service = LicenciaService()
        try:
            response = licencia_service.get_licencias_super()
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        licenciaSerializers = LicenciaSerializer(response, many=True)


        data = []
        for licencia in licenciaSerializers.data:
            # Calcular el valor de fecha_fin y agregarlo al diccionario
            fecha_inicio = datetime.datetime.strptime (licencia ['fecha_inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
            fecha_fin = fecha_inicio + datetime.timedelta (days=licencia ['duracion'])
            fecha_fin_str = fecha_fin.strftime ("%Y-%m-%dT%H:%M:%S.%fZ")
            licencia ['fecha_fin'] = fecha_fin_str
            # Añadir el diccionario modificado a la lista
            data.append (licencia)

        return Response({"success": True, "data": licenciaSerializers.data}, status=status.HTTP_200_OK)
    
    #metodo para crear licencias
    def post(self, request, pk=None):
        #validacion de los campos 
        if request.user.is_superuser == False :
            return Response({"succes": False, "message": "Acceso denegado"}, status=status.HTTP_400_BAD_REQUEST)
        if 'duracion' not in request.data :
            return Response({"succes": False, "message": "el campo duracion es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        if 'status' not in request.data :
            return Response({"succes": False, "message": "el campo de status es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'fecha_inicio' not in request.data :
            request.data["fecha_inicio"] = timezone.now()

        serializer = LicenciaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        dto = self.buid_dto_from_validated_data(serializer)
        licenciaService = LicenciaService()

        # Obtener el valor de customer_user_admin del request.data
        customer_user_admin = request.data.get('customer_user_admin', None) # Puedes cambiar None por otro valor por defecto
   
        try:
            response = licenciaService.createLicencia(dto,customer_user_admin)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        licencia_serializers = LicenciaSerializer(response, many=False)
        return Response({"success": True, "data": licencia_serializers.data},
                        status=status.HTTP_200_OK)
    
    def patch(self, request, pk=None):
        if request.user.is_superuser == False :
            return Response({"succes": False, "message": "Acceso denegado"}, status=status.HTTP_400_BAD_REQUEST)
        licencia_service = LicenciaService()
 
        type = request.data.get('tipo_de_plan', None)
        cobro = request.data.get('cobro', None)
        duracion = request.data.get('duracion', None)
        estado = request.data.get('status', None)
        customer_user_admin = request.data.get('customer_user_admin', None)

        try:
            licencia = licencia_service.updateLicencia(pk=pk, type=type, cobro=cobro, duracion=duracion, status=estado, customer_user_admin=customer_user_admin)
            licenciaSerializers = LicenciaSerializer(licencia, many=False)

            #####   proceso para agregar fecha fin al objeto 
            fecha_inicio = datetime.datetime.strptime(licenciaSerializers.data['fecha_inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
            fecha_fin = fecha_inicio + datetime.timedelta (days=licenciaSerializers.data['duracion'])
            fecha_fin_str = fecha_fin.strftime ("%Y-%m-%dT%H:%M:%S.%fZ")
            licenciaSerializers.data['fecha_fin'] = fecha_fin_str

            # Crear un nuevo diccionario con los datos del serializador
            data = licenciaSerializers.data.copy ()
            # Agregar el campo fecha_fin al diccionario
            data ['fecha_fin'] = fecha_fin_str
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    
    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return Licencia(
            customer_user_admin=data.get("customer_user_admin", None), # Si no hay customer_user_admin, se usa None
            tipo_de_plan=data["tipo_de_plan"],
            fecha_inicio=data.get("fecha_inicio", None),
            cobro=data["cobro"],
            duracion=data["duracion"],
            status=data["status"],
        )
    
#apartado para conectar usuarios con las licencias 
class LicenciaCoonectViewSet(APIView):
    #actualiza a el campo "licencia_id" de la clase customer usere para conectar estas dos entidades
    def patch(self, request, pk=None):
        ids = []
        licencia_service = LicenciaService()
        for reg in request.data:
            try :
                usr=licencia_service.connectLicencia(pk,reg["id"] )
            except Exception as e:
                return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_200_OK)

