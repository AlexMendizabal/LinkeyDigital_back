from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.authentication.models import CustomerUser
from apps.public.services import PublicContactservices


class PublicCustomerUserPhoneViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, public_id):
        char_public_id = public_id.replace('-', "")
        customer_user = get_object_or_404(CustomerUser, public_id=char_public_id)

        customer_user_public_contact_services = PublicContactservices()

        try:
            customer_user_public_contact_services.visit_phone(customer_user.pk)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True}, status=status.HTTP_200_OK)
