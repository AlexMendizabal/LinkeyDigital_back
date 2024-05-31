from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


from administration.models import Licencia
from administration.services import LicenciaService

#from authentication.views import CustomerUserSerializer
from authentication.models import CustomerUser
from profile.models import CustomerUserProfile
from administration.UtilitiesAdministration import UtilitiesAdm


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

class CustomerUserProfileSerializerLow(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = (
            'id','public_name', 'customer_user',
            'image')
        
class CustomerUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomerUser
        fields = ('id','email','is_editable','rubro', 'username', 'public_id', 'profile', 'phone_number', 'is_sponsor','is_booking','is_sales_manager','is_ecommerce')
        read_only_fields = ('profile',)
    def get_profile(self, user):
        profile = CustomerUserProfile.objects.get(customer_user=user)
        profile_serializer = CustomerUserProfileSerializerLow(profile)
        return profile_serializer.data
        

        
# apartado para usuarios genericos  
class LicenciaViewSet(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id', request.user.id)

        if user_id == request.user.id:
            user = request.user
        else:
            try:
                user = CustomerUser.objects.get(id = user_id)
            except Exception as e:
                return Response({"success": False, 'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.licencia_id is None:
            return Response({"success": False, "message": "El usuario no tiene licencia_id"}, status=status.HTTP_404_NOT_FOUND)
        licencia_service = LicenciaService()
        try:
            response = licencia_service.get_licencia(user.licencia_id_id)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        licenciaSerializers = LicenciaSerializer(response, many=False)

        #####   proceso para agregar fecha fin al objeto 
        utilities = Utilities()
        fecha_fin_str = utilities.calcular_fecha_fin(licenciaSerializers.data['fecha_inicio'], licenciaSerializers.data['duracion'])
        data = licenciaSerializers.data.copy ()
        data['fecha_fin'] = fecha_fin_str
        return Response({"success": True, "data": data }, status=status.HTTP_200_OK)
    

#apartado para usuarios administradores 
class LicenciaAdminViewSet(APIView):
    def get(self, request, pk=None):
        licencia_service = LicenciaService()
        #Si se manda Pk es porque la peticion es de un superAdmin
        try:
            user = get_object_or_404(CustomerUser, id=pk) if pk is not None else request.user
            utilitiesAdm = UtilitiesAdm()
            if not utilitiesAdm.hasPermision(request.user, user ):
                return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
            response = licencia_service.get_Users(user.licencia_id_id,request.user.id, with_admin=True if pk is None else True )
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        UserSerializers = CustomerUserSerializer(response, many=True)
        return Response({"success": True, "data": UserSerializers.data  }, status=status.HTTP_200_OK)
  
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
            utilities = Utilities()
            licencia ['fecha_fin'] = utilities.calcular_fecha_fin(licencia ['fecha_inicio'], licencia ['duracion'])
            # Añadir el diccionario modificado a la lista
            data.append (licencia)

        return Response({"success": True, "data": licenciaSerializers.data}, status=status.HTTP_200_OK)
    
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
        utilities = Utilities()
        dto = utilities.buid_dto_from_validated_data(serializer)
        licenciaService = LicenciaService()

        # Obtener el valor de customer_user_admin del request.data
        customer_user_admin = request.data.get('customer_user_admin', None) 
   
        try:
            response = licenciaService.createLicencia(dto,customer_user_admin)
        except Exception as e:
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
            utilities = Utilities() 
            # Crear un nuevo diccionario con los datos del serializador
            data = licenciaSerializers.data.copy ()
            # Agregar el campo fecha_fin al diccionario
            data ['fecha_fin'] = utilities.calcular_fecha_fin(licenciaSerializers.data['fecha_inicio'], licenciaSerializers.data['duracion'])
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    

    def delete(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({"succes": False, "message": "Acceso denegado"}, status=status.HTTP_400_BAD_REQUEST)
        licencia_service = LicenciaService()

        try:
            licencia_service.delete_licencia(licencia_id=pk)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_200_OK)

class LicenciaCoonectViewSet(APIView):
    def patch(self, request, pk=None):
        ids = []
        licencia_service = LicenciaService()
        for reg in request.data:
            try :
                usr=licencia_service.connectLicencia(pk,reg["id"] )
            except Exception as e:
                return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_200_OK)
    
from dateutil.parser import parse
from datetime import timedelta

#WAITING: Unificar las clases de utilities en un archivo global para todos los modulo, 
# DELETEME: borrar esta parte
class Utilities():
    def calcular_fecha_fin(self, fecha_inicio, duracion):
        fecha_inicio = parse(fecha_inicio) # Detecta el formato y convierte la cadena a objeto
        fecha_fin = fecha_inicio + timedelta(days=duracion) # Suma la duración en días al objeto
        fecha_fin_str = fecha_fin.strftime("%Y-%m-%dT%H:%M:%SZ") # Convierte el objeto a cadena con el formato deseado
        return fecha_fin_str # Devuelve la cadena
    
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
    
    def create_licencia_DTO(self, data):
        serializer = LicenciaSerializer(data=data)
        if not serializer.is_valid():
            return False
        utilities = Utilities()
        dto = utilities.buid_dto_from_validated_data(serializer)
        licenciaService = LicenciaService()

        response = licenciaService.createLicencia(dto)
        return response


