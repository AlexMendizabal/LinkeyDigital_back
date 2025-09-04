from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.models.customer_user import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class AuthenticatedView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        print(f"🔍 Intentando login con: {email} / {password}")

        try:
            user = User.objects.get(email=email)
            print(f"✅ Usuario encontrado en DB: {user.email}, activo={user.is_active}")
        except User.DoesNotExist:
            print("❌ No existe un usuario con ese email en la DB")
            return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=email, password=password)
        print("Resultado de authenticate():", user)

        if user is None:
            return Response({"mensaje": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "mensaje": "Login exitoso",
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

"""
Creacion de cuenta e inicio de sesion con correo electronico y contraseña
"""


class RegisterUser(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"mensaje": "Email y contraseña requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomerUser.objects.filter(email=email).exists():
            return Response({"mensaje": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomerUser.objects.create_user(email=email, password=password)

        refresh = RefreshToken.for_user(user)
        return Response({
            "mensaje": "Usuario registrado",
            "user_id": user.id,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)