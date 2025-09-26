

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class VerifyToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"mensaje": "Token/sesión válida", "user_id": request.user.id, "email": request.user.email, "username": request.user.username,})
        else:
            return Response({"mensaje": "Token o sesión inválida"}, status=status.HTTP_401_UNAUTHORIZED)
