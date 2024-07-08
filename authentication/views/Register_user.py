from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import threading
from threading import Lock
from authentication.models import CustomerUser
from rest_framework.generics import get_object_or_404
from conf_fire_base import DOMINIO_NAME

from authentication.exceptions import FirebaseAuthException, TokenNotFound

class CreateUserThread(threading.Thread):
    def __init__(self, email, password, errors, lock, corrects, licencia_id):
        super(CreateUserThread, self).__init__()
        self.email = email
        self.password = password
        self.errors = errors
        self.lock = lock
        self.corrects = corrects
        self.licencia_id = licencia_id

    def run(self):
        try:
            user = auth.create_user(
                email=self.email,
                password=self.password
            )
            try:
                uid = user.uid
                email = user.email
                username = email.split('@')[0]
                User = get_user_model()
                user = User.objects.create(uid=uid, email=email, username=username, licencia_id_id=self.licencia_id)
                with self.lock:
                    self.corrects.append({"email": self.email})
            except Exception as e:
                auth.delete_user(user.uid)
                with self.lock:
                    self.errors.append({"email": self.email, "error": str(e)})
                raise FirebaseAuthException()
        except Exception as e:
            with self.lock:
                self.errors.append({"email": self.email, "error": str(e)})
            raise e

def create_users_in_threads(cant, correo, licencia_id, user_id=None):
    if not licencia_id and user_id:
        try:
            user = CustomerUser.objects.get(id=user_id)
        except Exception as e:
            user = get_object_or_404(CustomerUser, username=user_id)
        licencia_id = user.licencia_id

    if not correo:
        correo = "Test-julio"

    User = get_user_model()
    users = User.objects.filter(email__startswith=correo, email__endswith=f'@{DOMINIO_NAME}')

    numbers = [int(re.search(re.escape(correo) + r'-(\d+)@', user.email).group(1)) for user in users if re.search(re.escape(correo) + r'-(\d+)@', user.email)]

    max_number = max(numbers) if numbers else 0
    threads = []
    errors = []
    corrects = []
    lock = Lock()

    for i in range(1, cant + 1):
        email = f"{correo}-{max_number + i}@{DOMINIO_NAME}"
        password = DOMINIO_NAME
        thread = CreateUserThread(email=email, password=password, errors=errors, lock=lock, corrects=corrects, licencia_id=licencia_id)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return errors, corrects

class CreateALotOfUsers(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            raise TokenNotFound()

        cant = int(request.data.get("cant", 0))
        correo = request.data.get("correo", None)
        licencia_id = int(request.data.get("licencia", 0))
        user_id = request.data.get("user_id", None)

        if not cant or (not licencia_id and not user_id):
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        if cant > 50:
            cant = 50

        errors, corrects = create_users_in_threads(cant, correo, licencia_id, user_id)

        if errors:
            return Response({"success": True, "errors": errors, "corrects": corrects}, status=status.HTTP_200_OK)

        return Response({"success": True, "corrects": corrects}, status=status.HTTP_200_OK)
