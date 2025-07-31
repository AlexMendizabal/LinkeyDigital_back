from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from apps.profile.models import CustomerUserPhone, PhoneDto
from apps.profile.services import Contactservices


class CustomerUserPhoneserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserPhone
        fields = (
            'customer_user', 'phone', 'image', 'is_active', 'is_visible')
        extra_kwargs = {'phone': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserPhoneViewSet(APIView):
    def get(self, request, pk=None):
        contact_services = Contactservices()
        try:
            response = contact_services.get_phone(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_phone_serializers = CustomerUserPhoneserializers(response, many=False)
        return Response({"success": True, "data": customer_phone_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializers = CustomerUserPhoneserializers(data=request.data)

        if 'image' in request.data:
            try:
                request.data.pop('image')
            except Exception as e:
                pass

        if not serializers.is_valid():
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

        if 'phone' in request.data:
            if request.data.get('phone').replace(" ", "") == "":
                CustomerUserPhone.objects.filter(customer_user=request.user.id).delete()
                return Response({"success": True})

        dto = self.buid_dto_from_validated_data(serializers)
        contact_services = Contactservices()

        try:
            response = contact_services.create_or_update_phone(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_phone_serializers = CustomerUserPhoneserializers(response, many=False)
        return Response({"success": True, "data": customer_phone_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
        return PhoneDto(
            customer_user=data["customer_user"],
            phone=data["phone"],
            is_active=True,
            is_visible=data["is_visible"],
        )
