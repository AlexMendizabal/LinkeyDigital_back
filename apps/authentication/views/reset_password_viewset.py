from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class ResetPasswordView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password")

        # --- MODO 1: email → generar link de reset ---
        if email:
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                # No revelar si existe
                return Response({"mensaje": "Si el correo existe, se enviará un enlace"}, status=status.HTTP_200_OK)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/restore-password?uid={uid}&token={token}"


            subject = "Reestablecimiento de contraseña en Linkey.digital"
                       
            message = (
                f"Saludos {user.username},\n\n"
                f"Se confirmó su correo para su cuenta en nuestra plataforma.\n"
                f"Por favor, haga clic en el siguiente enlace para establecer su contraseña:\n\n"
                f"{reset_link}\n\nGracias."
            )

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({"mensaje": "Correo de recuperación enviado"}, status=status.HTTP_200_OK)

        # --- MODO 2: uid + token + password → reset real ---
        if not uidb64 or not token:
            return Response({"mensaje": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"mensaje": "Enlace inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"mensaje": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password:
            return Response({"mensaje": "Token válido"}, status=status.HTTP_200_OK)

        user.set_password(new_password)
        user.save()

        return Response({"mensaje": "Contraseña restablecida correctamente"}, status=status.HTTP_200_OK)

class ValidateResetTokenView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")

        if not uidb64 or not token:
            return Response({"valid": False, "mensaje": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"valid": False, "mensaje": "Enlace inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            return Response({
                "valid": True,
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"valid": False, "mensaje": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

