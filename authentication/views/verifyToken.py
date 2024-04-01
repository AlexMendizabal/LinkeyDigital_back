from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from firebase_admin import auth, credentials

from authentication.models import CustomerUser
from authentication.views import CustomerUserSerializer
import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import status
from authentication.exceptions import FirebaseAuthException, InvalidToken, TokenNotFound
from soyyo_api.settings import NAME_FIRE_BASE

cred = credentials.Certificate(os.path.join(
    os.path.dirname(__file__), '../secrets/' + NAME_FIRE_BASE))

class VerifyToken(APIView):
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise TokenNotFound()

        token = auth_header.split(' ').pop()
        try:
            try:
                decoded_token = auth.verify_id_token(id_token = token)
                uid = decoded_token.get('uid')
                user = get_object_or_404(CustomerUser, uid=uid )
                serliazer = CustomerUserSerializer(user, many=False)
            except Exception as e:
                return Response({"data": 2, "mansaje": str(e)}, status=status.HTTP_404_NOT_FOUND)

            email = decoded_token.get('email_verified')
            if email:
                return Response({"data": 0, "user": serliazer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"data": 1, "user": serliazer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": 3}, status=status.HTTP_404_NOT_FOUND)