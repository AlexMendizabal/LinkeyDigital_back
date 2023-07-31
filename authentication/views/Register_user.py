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
                print(self.licencia_id)
                user = User.objects.create(uid=uid, email=email, username=username, licencia_id_id = self.licencia_id)
                with self.lock:
                    self.corrects.append({"email": self.email})
            except Exception as e:
                print(e)
                auth.delete_user(user.uid)
                with self.lock:
                    self.errors.append({"email": self.email, "error": str(e)})
                raise FirebaseAuthException()
        except Exception as e:
            with self.lock:
                self.errors.append({"email": self.email, "error": str(e)})
            raise e


class CreateALotOfUsers(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            raise TokenNotFound()
        # cantidad de usuarios a crear (solo admite 50)
        cant = request.data.get("cant", None)
        # nombre con el que iniciar el correo 
        correo = request.data.get("correo", None)
        # licencia a la que agregar el usuario
        licencia_id = request.data.get("licencia", None)
        # se puede tambien mandar el user id del que se quiere extraer la licencia para no buscar la licencia en el front 
        user_id = request.data.get("user_id", None)

        if not cant:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        if not licencia_id and not user_id:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        cant = int(cant)
        if cant > 50:
            cant = 50

        if not licencia_id and user_id:
            # busca por id, si no lo encuentra lo busca por username
            try:
                user = CustomerUser.objects.get(id=user_id)
            except Exception as e:
                user = get_object_or_404(CustomerUser, username=user_id)
                    
            licencia_id = user.licencia_id
        if not correo:
            correo = "usuario"
        
        licencia_id = int(licencia_id)
        
        User = get_user_model()
        users = User.objects.filter(email__startswith=correo, email__endswith='@soyyo.digital')

        numbers = []
        for user in users:
            email = user.email
            regex_pattern = re.escape(correo) + r'-(\d+)@'
            match = re.search(regex_pattern, email)
            if match:
                number = int(match.group(1))
                numbers.append(number)

        max_number = max(numbers) if numbers else 0

        threads = []
        errors = []
        corrects = []
        lock = Lock()
        for i in range(1, cant+1):
            email = str(correo) + "-" + str(max_number + i) + "@soyyo.digital"
            password = "soyyo.digital"
            thread = CreateUserThread(email=email, password=password, errors=errors, lock=lock, corrects=corrects, licencia_id=licencia_id)
            thread.start()
            threads.append(thread)

        # Esperar a que todos los hilos terminen su ejecución
        for thread in threads:
            thread.join()

        if errors:
            return Response({"success": True, "errors": errors, "corrects": corrects}, status=status.HTTP_200_OK)

        return Response({"success": True, "corrects" : corrects}, status=status.HTTP_200_OK)
