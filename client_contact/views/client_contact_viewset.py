from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from client_contact.models.client_contact import Register
from client_contact.serializers import RegisterSerializer

class RegisterDetail(APIView):
    permission_classes = []
    authentication_classes = []
    def get_object(self, register_id):
        try:
            return Register.objects.get(pk=register_id)
        except Register.DoesNotExist:
            return None

    def get(self, request, register_id=None):
        # Si se proporciona un register_id, se devuelve el detalle de ese registro específico
        if register_id:
            register = self.get_object(register_id)
            if register is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = RegisterSerializer(register)
            return Response(serializer.data)
        else:
            # Si no se proporciona register_id, se obtienen todos los registros del usuario especificado
            customer_user_id = request.query_params.get('customer_user_id', None)
            if customer_user_id is None:
                return Response({"error": "Se debe proporcionar customer_user_id"}, status=status.HTTP_400_BAD_REQUEST)
            registers = Register.objects.filter(customer_user_id=customer_user_id)
            serializer = RegisterSerializer(registers, many=True)
            return Response(serializer.data)

    def put(self, request, register_id):
        register = self.get_object(register_id)
        if register is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterSerializer(register, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, register_id):
        register = self.get_object(register_id)
        if register is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        register.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateRegister(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
