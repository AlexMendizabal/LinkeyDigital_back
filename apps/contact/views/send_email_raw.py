
import json
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail, EmailMessage

import threading

class SendEmailRawViewSet(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request, pk=None, format=None):

        try:
            emailTypes = [
                {"to": "soporte@linkey.digital", "title": "Solicitud de soporte"},
                {"to": "soporte@linkey.digital", "title": "Extensión de licencia"},
                {"to": "ignacio@linkey.digital", "title": "Solicitud de Soy Yo"},
            ]

            emailFormat = emailTypes[ request.data['type'] ]
            data = request.data['data']

            EmailThread(emailFormat=emailFormat, content=data).start()
            return Response({"success": True, "message": "Enviado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": "Error al enviar el correo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailThread(threading.Thread):
    def __init__(self, emailFormat, content):
        self.subject = emailFormat["title"]
        self.sendTo = emailFormat["to"]
        self.sender = "contacto@linkey.digital"
        self.body = '\n'.join( [ f"{key} : {value}" for key,value in content.items() ] )
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.body,
            self.sender,
            [ self.sendTo ],
            fail_silently=False,
        )