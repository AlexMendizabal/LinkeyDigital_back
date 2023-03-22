from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from profile.models import CustomerUserWhatsapp, WhatsappDto
from profile.services import ContactService


class CustomerUserWhatsappSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserWhatsapp
        fields = (
            'customer_user', 'phone_number', 'message', 'image', 'is_active', 'is_visible')
        extra_kwargs = {'phone_number': {'required': True}, 'message': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserWhatsappViewSet(APIView):
    def get(self, request, pk=None):
        contact_service = ContactService()
        try:
            response = contact_service.get_whatsapp(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_whatsapp_serializers = CustomerUserWhatsappSerializer(response, many=False)
        return Response({"success": True, "data": customer_whatsapp_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializer = CustomerUserWhatsappSerializer(data=request.data)

        if 'image' in request.data:
            try:
                request.data.pop('image')
            except Exception as e:
                pass

        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if 'phone_number' in request.data:
            if request.data.get('phone_number').replace(" ", "") == "":
                CustomerUserWhatsapp.objects.filter(customer_user=request.user.id).delete()
                return Response({"success": True})

        dto = self.buid_dto_from_validated_data(serializer)
        contact_service = ContactService()

        try:
            response = contact_service.create_or_update_whatsapp(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_whatsapp_serializers = CustomerUserWhatsappSerializer(response, many=False)
        return Response({"success": True, "data": customer_whatsapp_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return WhatsappDto(
            customer_user=data["customer_user"],
            phone_number=data["phone_number"],
            message=data["message"],
            is_active=True,
            is_visible=data["is_visible"],
        )
