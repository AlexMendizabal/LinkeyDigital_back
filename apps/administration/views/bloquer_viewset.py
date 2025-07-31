from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from apps.administration.views.licencias_viewset import CustomerUserserializers
from apps.authentication.models import CustomerUser
from apps.administration.services.blocker_service import Blockersservices

#apartado para bloquear usuarios --> unicamente para adm y super
class BlockersUsersViewSet(APIView):

    def put(self, request, pk=None):
            
        servicesBlock = Blockersservices()
        try:
            if (request.user.is_superuser) :
                response = servicesBlock.blockUser(pk)
            elif (request.user.is_admin) :
                response = servicesBlock.blockUser(pk,request.user.licencia_id_id )
                if response is None:
                    return Response({"success": False, "error": "No tienes permisos de administrador."},
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"success": False, "error": "No tienes permisos de administrador."},
                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        responseserializers = CustomerUserserializers(response, many=False)
        return Response({"success": True, "data": responseserializers.data},
                        status=status.HTTP_200_OK)
class EditableUsersViewSet(APIView):

    def put(self, request, pk=None):
            
        servicesBlock = Blockersservices()
        value = request.data.get("canEdit", False)
        try:
            if (request.user.is_superuser) :
                response = servicesBlock.blockEditUser(value, pk)
            elif (request.user.is_admin) :
                response = servicesBlock.blockEditUser(value, pk,request.user.licencia_id_id )
                if response is None:
                    return Response({"success": False, "error": "No tienes permisos de administrador."},
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"success": False, "error": "No tienes permisos de administrador."},
                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        responseserializers = CustomerUserserializers(response, many=False)
        return Response({"success": True, "data": responseserializers.data},
                        status=status.HTTP_200_OK)