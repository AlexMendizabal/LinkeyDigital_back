from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from apps.authentication.services.auth_services import Authservicess
class AuthenticationSpecialViewset(APIView):

    def delete(self, request):
        # Metodo para borrar datos internos del user ( no borra al user xd )
        if not request.user.is_superuser:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            authservicess = Authservicess()
            user_id = request.GET.get('user_id', None)
            authservicess.restartUser(user_id)
            authservicess.deleteUser(user_id)
        except:
            return Response({'msg': 'error al borrar social_media'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "True"}, status=status.HTTP_200_OK)