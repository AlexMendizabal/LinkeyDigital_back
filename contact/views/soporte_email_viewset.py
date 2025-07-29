import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail
from conf_fire_base import REGION_ACTUAL

import threading


class EmailContent:
    def __init__(self, json):
        self.numberCards = json["numberCards"]


class OrderNewCardsViewSet(APIView):

    def post(self, request, pk=None, format=None):
        try:
            json_response = json.loads(request.body)
            emailContent = EmailContent(json_response)

            ip = _get_client_ip(request)

            EmailThread(content=emailContent, ip=ip, user = request.user).start()
            return Response({"succes": True, "message": "enviado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"succes": False, "message": "error al enviar el correo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailThread(threading.Thread):
    def __init__(self, content: EmailContent, ip, user ):
        self.subject = "Solicitud para nuevas cartas de: " + user.username
        self.recipient_list = [user.email]
        if REGION_ACTUAL == "br":
            self.sender = "contato@soueu.com.br"
        else: 
            self.sender = "contacto@linkey.digital"
        self.body = f"Se lleno una solicitud con la siguiente información:\nNombre: {user.username}\nEmail: {user.email}\nTeléfono: {user.phone_number}\nUser_id: {user.id}\nPublic_id: {user.public_id}\nIP de solicitud: {ip} \nEste usuario esta solicitando la cantidad de tarjetas: {content.numberCards}"
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject,
                self.body,
                self.sender,
                ["ignacio@linkey.digital"],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"succes": False, "message": "error al enviar el correo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
