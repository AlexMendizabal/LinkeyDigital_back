from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated
from .customer_user_viewset import CustomerUserSerializer


class AuthenticatedView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user_serializer = CustomerUserSerializer(request.user, many=False)
        return Response({'User': user_serializer.data})


"""
Creacion de cuenta e inicio de sesion con correo electronico y contraseña
"""


class RegisterUser(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user_serializer = CustomerUserSerializer(request.user, many=False)
        return Response({'message': 'User Registered','data': user_serializer.data })
