from rest_framework import routers
from django.urls import path, include

from contact.views import UserSendMailViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('send-email', UserSendMailViewSet.as_view()),

]
