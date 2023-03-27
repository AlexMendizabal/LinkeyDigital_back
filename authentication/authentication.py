import os
from time import sleep

import firebase_admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from firebase_admin import auth, credentials
from rest_framework.authentication import BaseAuthentication

from soyyo_api import settings
from .exceptions import FirebaseAuthException, InvalidToken, TokenNotFound, EmailNotVerified

cred = credentials.Certificate(os.path.join(
    os.path.dirname(__file__), 'secrets/firebaseconfig.json'))

app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    Acceso a datos solo si se inicio sesion en firebase
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise TokenNotFound()

        token = auth_header.split(' ').pop()

        #sleep(3)
        try:
            decoded_token = auth.verify_id_token(id_token = token)
        except Exception as e:
            raise InvalidToken()
        try:
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            username = email.split('@')[0]
            user = auth.get_user(uid, app)
        except Exception as e:
            raise FirebaseAuthException()

        User = get_user_model()

        try:
            objUser = User.objects.filter(uid=user.uid)
            if objUser and not user.email_verified:
                raise EmailNotVerified()
        except Exception as e:
            raise EmailNotVerified()
        try:
            user_exists = User.objects.filter(uid=uid).count() > 0
            if user_exists:
                user = User.objects.filter(uid=uid)[0]
                
            elif User.objects.filter(username=username).count() > 0:
                
                username = username+user.uid[0:4]
            else:
                user, created = User.objects.create(uid=uid, email=email, username=username)
        except Exception as e:
            print('this is problem', e)
            return None
        return user, None
