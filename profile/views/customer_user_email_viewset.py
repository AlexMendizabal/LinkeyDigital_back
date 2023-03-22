from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from profile.models import CustomerUserEmail, EmailDto
from profile.services import ContactService


class CustomerUserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserEmail
        fields = (
            'customer_user', 'email', 'subject', 'body', 'image','is_active', 'is_visible')
        extra_kwargs = {'email': {'required': True}, 'body': {'required': True}, 'subject': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserEmailViewSet(APIView):
    def get(self, request, pk=None):
        contact_service = ContactService()
        try:
            response = contact_service.get_email(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_email_serializers = CustomerUserEmailSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializer = CustomerUserEmailSerializer(data=request.data)

        if 'image' in request.data:
            try:
                request.data.pop('image')
            except Exception as e:
                pass

        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if 'email' in request.data:
            if request.data.get('email').replace(" ", "") == "":
                CustomerUserEmail.objects.filter(customer_user=request.user.id).delete()
                return Response({"success": True})

        dto = self.buid_dto_from_validated_data(serializer)
        contact_service = ContactService()

        try:
            response = contact_service.create_or_update_email(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_email_serializers = CustomerUserEmailSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return EmailDto(
            customer_user=data["customer_user"],
            email=data["email"],
            subject=data["subject"],
            body=data["body"],
            is_active=True,
            is_visible=data["is_visible"],
        )
