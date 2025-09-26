# apps/authentication/views/verify_email.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.authentication.utils.email import send_confirmation_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class UpdatetemporalEmailView(APIView):
    permission_classes = []  # Ajusta según tus necesidades

    def post(self, request):
        linkey_email = request.data.get("linkey_email")
        new_email = request.data.get("new_email")

        if not linkey_email or not new_email:
            return Response(
                {"error": "Debe enviar linkey_email y new_email"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el correo temporal tenga el dominio correcto
        if not linkey_email.endswith("@linkey.digital"):
            return Response(
                {"error": "El correo proporcionado no es un correo temporal válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el correo temporal existe
        try:
            user = User.objects.get(email=linkey_email)
        except User.DoesNotExist:
            return Response(
                {"error": "No se encontró usuario con ese correo temporal"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verificar que el new_email no esté registrado
        if User.objects.filter(email=new_email).exists():
            return Response(
                {"error": "El nuevo correo ya está registrado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generar token seguro para identificar al usuario
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construir enlace seguro incluyendo el nuevo correo como query param
        reset_link = (
            f"http://localhost:3000/restore-password?"
            f"uid={uid}&token={token}&new_email={new_email}"
        )

        # Enviar correo con username y enlace
        subject = "Activa tu cuenta Linkey"
        message = (
            f"Saludos {user.username},\n\n"
            f"Se confirmó su correo {new_email} para su cuenta en nuestra plataforma.\n"
            f"Por favor, haga clic en el siguiente enlace para establecer su contraseña:\n\n"
            f"{reset_link}\n\nGracias."
        )

        try:
            send_confirmation_email(new_email, subject, message)
        except Exception as e:
            return Response(
                {"error": f"No se pudo enviar correo: {str(e)}"},
                status=500
            )

        # ⚠️ No actualizar el email todavía
        # Se actualizará solo cuando el usuario establezca su contraseña

        return Response(
            {"mensaje": "Correo enviado correctamente. Usa el enlace para establecer contraseña.", "user_id": user.id},
            status=status.HTTP_200_OK
        )
