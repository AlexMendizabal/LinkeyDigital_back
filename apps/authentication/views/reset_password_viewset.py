from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

class ResetPasswordView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password", None)

        if not uidb64 or not token:
            return Response({"mensaje": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decodificar UID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"mensaje": "Enlace inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar validez del token
        if not default_token_generator.check_token(user, token):
            return Response({"mensaje": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

        # Si no se mandó password → solo validar token
        if not new_password:
            return Response({"mensaje": "Token válido"}, status=status.HTTP_200_OK)

        # Si hay password → cambiarla
        user.password = make_password(new_password)
        user.save()

        return Response({"mensaje": "Contraseña restablecida correctamente"}, status=status.HTTP_200_OK)
