import json
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail, EmailMessage

import threading


class EmailContent:
    def __init__(self, json):
        self.name = json["name"]
        self.phone = json["phone"]
        self.department = json["department"]
        self.email = json["email"]
        self.plan = json["plan"]
        self.numberCards = json["numberCards"]

class UserSendMailViewSet(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request, pk=None, format=None):

        try:
            json_response = json.loads(request.body)
            emailContent = EmailContent(json_response)

            ip = _get_client_ip(request)

            EmailThread(content=emailContent, ip=ip).start()
            return Response({"succes": True, "message": "enviado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"succes": False, "message": "error al enviar el correo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailThread(threading.Thread):
    def __init__(self, content:EmailContent, ip):
        self.subject = "Solicitud de Soy Yo"
        self.recipient_list = [ content.email ]
        self.sender = "contacto@soyyo.digital"
        self.body = f"Se lleno una solicitud con la siguiente información:\nNombre: {content.name}\nDepartamento: {content.department}\nEmail: {content.email}\nTeléfono: {content.phone}\nPlan seleccionado: {content.plan}\nNúmero de tarjetas: {content.numberCards}\nIP de solicitud: {ip}"
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.body,
            self.sender,
            ["ventas@soyyo.digital"],
            fail_silently=False,
        )
        print("Correo enviado exitosamente")



def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip