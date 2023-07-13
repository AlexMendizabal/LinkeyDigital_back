from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import threading
from threading import Lock

from authentication.exceptions import FirebaseAuthException, TokenNotFound

class CreateUserThread(threading.Thread):
    def __init__(self, email, password, errors, lock, corrects):
        super(CreateUserThread, self).__init__()
        self.email = email
        self.password = password
        self.errors = errors
        self.lock = lock
        self.corrects = corrects

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
                user = User.objects.create(uid=uid, email=email, username=username)
                with self.lock:
                    self.corrects.append({"email": self.email})
            except Exception as e:
                print(e)
                with self.lock:
                    self.errors.append({"email": self.email, "error": str(e)})
                raise FirebaseAuthException()
        except Exception as e:
            with self.lock:
                self.errors.append({"email": self.email, "error": str(e)})
            raise e


class CreateALotOfUsers(APIView):

    def post(self, request, cant=None):
        if not request.user.is_superuser:
            raise TokenNotFound()
        if not cant:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        if cant > 50:
            cant = 50
        
        User = get_user_model()
        users = User.objects.filter(email__startswith='usuario-', email__endswith='@soyyo.digital')

        numbers = []
        for user in users:
            email = user.email
            match = re.search(r'usuario-(\d+)@', email)
            if match:
                number = int(match.group(1))
                numbers.append(number)

        max_number = max(numbers) if numbers else 0

        threads = []
        errors = []
        corrects = []
        lock = Lock()
        for i in range(1, cant+1):
            email = "usuario-" + str(max_number + i) + "@soyyo.digital"
            password = "123456"
            thread = CreateUserThread(email=email, password=password, errors=errors, lock=lock, corrects=corrects)
            thread.start()
            threads.append(thread)

        # Esperar a que todos los hilos terminen su ejecución
        for thread in threads:
            thread.join()

        if errors:
            return Response({"success": True, "errors": errors, "corrects": corrects}, status=status.HTTP_200_OK)

        return Response({"success": True, "corrects" : corrects}, status=status.HTTP_200_OK)
