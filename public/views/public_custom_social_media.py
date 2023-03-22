from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import CustomerUser
from public.services import PublicSocialMediaService


class PublicCustomerUserCustomSocialMediaViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, public_id):
        try:
            customer_user_custom_social_media_id = request.data["customer_user_custom_social_media_id"]
        except Exception as e:
            return Response(
                {"status": "error", "data": {"customer_user_custom_social_media_id": ["This field is required"]}},
                status=status.HTTP_400_BAD_REQUEST)

        char_public_id = public_id.replace('-', "")
        customer_user = get_object_or_404(CustomerUser, public_id=char_public_id)
        customer_user_public_custom_social_media_service = PublicSocialMediaService()
        try:
            customer_user_public_custom_social_media_service.visit_custom_social_media(customer_user_custom_social_media_id,
                                                                    customer_user.pk)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"success": True}, status=status.HTTP_200_OK)
