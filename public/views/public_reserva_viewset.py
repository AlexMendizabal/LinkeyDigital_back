from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from authentication.models import CustomerUser
from profile.models import CustomerUserCustomSocialMedia
from profile.models import CustomerUserReserva, ReservaDto
from public.services import ReservaService


class CustomerReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUserReserva
        fields = (
            'id', 'custome_user_social_media', 'adults', 'kids', 'date', 'created_at','Nombre','Email','phone')
        extra_kwargs = {'date': {'required': True}, 'Nombre': {'required': True},
                        'phone': {'required': True}}


class CustomerUserReservaViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, public_id):
        char_public_id = public_id.replace('-', "")
        custome_user_social_media = get_object_or_404(CustomerUserCustomSocialMedia, id=request.data["custome_user_social_media"])
        request.data["custome_user_social_media"] = custome_user_social_media.id
        serializer = CustomerReservaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(serializer)
        reserva_service = ReservaService()

        try:
            response = reserva_service.create_or_update_reserva(dto)
        except Exception as e:
            print(e)
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        reserva_serializer = CustomerReservaSerializer(response, many=False)
        return Response({"success": True, "data": reserva_serializer.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return ReservaDto(
            date=data["date"],
            adults=data["adults"],
            kids=data["kids"],
            Nombre=data["Nombre"],
            Email=data["Email"],
            phone=data["phone"],
            custome_user_social_media=data["custome_user_social_media"]
        )
