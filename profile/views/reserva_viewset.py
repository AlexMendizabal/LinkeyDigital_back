from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from authentication.models import CustomerUser
from profile.models import CustomerUserReserva, ReservaDto
from profile.services import ReservaService


class CustomerReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUserReserva
        fields = (
            'id', 'custome_user_social_media', 'adults', 'kids', 'date', 'created_at','Nombre','Email','phone')
        extra_kwargs = {'date': {'required': True}, 'Nombre': {'required': True},
                        'phone': {'required': True}}


class CustomerUserReservaViewSet(APIView):

    def get(self, request, pk=None, social=None):
        reserva_service = ReservaService()
        try:
            response = reserva_service.get_reserva(pk, social)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        if(pk):
            reserva_serializer = CustomerReservaSerializer(response, many=False)
        else:
            reserva_serializer = CustomerReservaSerializer(response, many=True)
        return Response({"success": True, "data": reserva_serializer.data}, status=status.HTTP_200_OK)

