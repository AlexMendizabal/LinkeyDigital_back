from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from authentication.views import CustomerUserSerializer
from authentication.models import CustomerUser
from administration.services import BlockersService

#apartado para bloquear usuarios --> unicamente para adm y super
class BlockersUsersViewSet(APIView):

    def put(self, request, pk=None):
            
        serviceBlock = BlockersService()
        try:
            if (request.user.is_superuser) :
                response = serviceBlock.blockUser(pk)
            elif (request.user.is_admin) :
                response = serviceBlock.blockUser(pk,request.user.licencia_id_id )
                if response is None:
                    return Response({"success": False, "error": "No tienes permisos de administrador."},
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"success": False, "error": "No tienes permisos de administrador."},
                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        responseSerializer = CustomerUserSerializer(response, many=False)
        return Response({"success": True, "data": responseSerializer.data},
                        status=status.HTTP_200_OK)
class EditableUsersViewSet(APIView):

    def put(self, request, pk=None):
            
        serviceBlock = BlockersService()
        try:
            if (request.user.is_superuser) :
                response = serviceBlock.blockEditUser(pk)
            elif (request.user.is_admin) :
                response = serviceBlock.blockEditUser(pk,request.user.licencia_id_id )
                if response is None:
                    return Response({"success": False, "error": "No tienes permisos de administrador."},
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"success": False, "error": "No tienes permisos de administrador."},
                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        responseSerializer = CustomerUserSerializer(response, many=False)
        return Response({"success": True, "data": responseSerializer.data},
                        status=status.HTTP_200_OK)