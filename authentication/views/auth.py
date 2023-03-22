from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth
from django.contrib.auth import get_user_model


class AuthenticatedView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'User': request.user.email})


"""
Creacion de cuenta e inicio de sesion con correo electronico y contraseña
"""


class RegisterUser(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': 'User Registered'})
