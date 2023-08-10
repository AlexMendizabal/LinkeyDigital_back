from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from firebase_admin import auth, credentials

from authentication.models import CustomerUser
import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import status
from authentication.exceptions import FirebaseAuthException, InvalidToken, TokenNotFound

cred = credentials.Certificate(os.path.join(
    os.path.dirname(__file__), '../secrets/firebaseconfig.json'))


class VerifyEmailViewSet(APIView):
    def get(self, request):

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise TokenNotFound()

        token = auth_header.split(' ').pop()

        #sleep(3)
        try:
            try:
                decoded_token = auth.verify_id_token(id_token = token)
            except Exception as e:
                return Response({"data": 2}, status=status.HTTP_404_NOT_FOUND)

            email = decoded_token.get('email_verified')
            if email:
                return Response({"data": 0}, status=status.HTTP_200_OK)
            else:
                return Response({"data": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": 3}, status=status.HTTP_404_NOT_FOUND)
    

#     export const TOKEN_RESULT = {
#   VALID: 0,
#   NEED_VERIFICATION: 1,
#   INVALID: 2,
#   ERROR: 3, /* Error en lado del cliente, por conexión por ejm */
# };