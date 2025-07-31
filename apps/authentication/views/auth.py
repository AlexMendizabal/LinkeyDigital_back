
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class AuthenticatedView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"mensaje": "Login exitoso", "user_id": user.id})
        else:
            return Response({"mensaje": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUser(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return Response({"mensaje": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=email,
            username=email.split('@')[0],
            password=make_password(password)
        )
        return Response({"mensaje": "Usuario registrado exitosamente", "user_id": user.id}, status=status.HTTP_201_CREATED)
