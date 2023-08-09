from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from firebase_admin import auth, credentials

from authentication.models import CustomerUser
import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import status

cred = credentials.Certificate(os.path.join(
    os.path.dirname(__file__), '../secrets/firebaseconfig.json'))


class VerifyEmailViewSet(APIView):
    def get(self, request, customer_id=None):

        try:
            if not request.user.is_superuser:
                return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
            if not customer_id:
                user = request.user
            else:
                user = get_object_or_404(CustomerUser, id=customer_id)

            userFire = auth.get_user(user.uid)
            if userFire.email_verified:
                return Response({"verificado": True}, status=status.HTTP_200_OK)
            else:
                return Response({"verificado": False}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        