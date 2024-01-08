import os

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from profile.models import CustomerUserCustomSocialMedia, CustomSocialMediaDto
from profile.services import SocialMediaService

from authentication.models import CustomerUser
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import transaction
import json
from administration.UtilitiesAdministration import UtilitiesAdm

from django.core.exceptions import ValidationError

class customer_user_custom_order_viewset(APIView):

# {
# 1:123,
# 2:124,
# 3:125,
# }

    def put(self, request):
        ids = request.data.get('ids', {})
        cusm_service = SocialMediaService()

        if not ids or ids == {}:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        print(ids)
        for key, value in ids.items():
            res = cusm_service.update_order_social_media(value, key)

        return Response({"success": True}, status=status.HTTP_200_OK)
            
            


            



