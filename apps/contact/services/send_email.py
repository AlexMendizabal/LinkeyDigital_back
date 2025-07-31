import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives  
from conf_fire_base import REGION_ACTUAL

import threading

class EmailThread(threading.Thread):
    def __init__(self, subject , email, body ):
        self.subject = subject
        self.email = email
        if REGION_ACTUAL == "br":
            self.sender = "contato@soueu.com.br"
        else: 
            self.sender = "ignacio@linkey.digital"
        self.body = body
        threading.Thread.__init__(self)

    def run(self):
        try:
            msg = EmailMultiAlternatives(
                self.subject,
                self.body,
                self.sender,
                [self.email]
            )
            msg.attach_alternative(self.body, "text/html")
            msg.send()
        except Exception as e:
            print(e)
            print("Error al enviar el correo")



def SendEmail(subject, email, body ):
        try:
            EmailThread(body=body, email= email, subject=subject).start()
            return True
        except Exception as e:
            return False



