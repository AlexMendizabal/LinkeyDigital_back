from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from booking.models import ConfigurationBooking,ConfigurationBookingDto
from booking.services import ConfBookingService

from administration.UtilitiesAdministration import UtilitiesAdm

from booking.serializer import ConfBookingSerializer

class ConfBookingViewset(APIView):

    def post(self, request, user_id=None):
        # utilitiesAdm = UtilitiesAdm()
        # if not utilitiesAdm.hasPermision(request.user, user_id):
        #     return Response({"status": "error"}, status=status.HTTP_401_UNAUTHORIZED)
        booking_serializer = ConfBookingSerializer(data=request.data)

        if not booking_serializer.is_valid():
            return Response({"status": "error", "data": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(booking_serializer)
        booking_service = ConfBookingService()

        try:
            response = booking_service.create_or_update_conf_booking(dto)
        except Exception as e:
            return Response({"success": False, "error" : e}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_email_serializers = ConfBookingSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return ConfigurationBookingDto(
            customer_user=data["customer_user"],
            max_personas=data.get("max_personas", None),
            time_bet_booking=data.get("time_bet_booking", None),
            holiday=data.get("holiday", None),

            hora_inicio=data.get("hora_inicio", None),
            hora_fin=data.get("hora_fin", None),
            
            hora_inicio_tarde=data.get("hora_inicio_tarde", None),
            hora_fin_tarde=data.get("hora_fin_tarde", None),
            
            hora_inicio_noche=data.get("hora_inicio_noche", None),
            hora_fin_noche=data.get("hora_fin_noche", None),

            status_conf=data.get("status_conf", None),
            kids=data.get("kids", None),
            teen=data.get("teen", None),
        )


