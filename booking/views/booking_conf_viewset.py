from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from booking.models import ConfigurationBooking,ConfigurationBookingDto
from booking.services import ConfBookingService

from administration.UtilitiesAdministration import UtilitiesAdm

class ConfBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationBooking
        fields = (
            'id', 'customer_user', 'max_personas', 'time_bet_booking', 'holiday', 
            'hora_inicio','hora_fin', 'status_conf', 
            'kids', 'teen')

class ConfBookingViewset(APIView):
    def get(self, request, user_id=None):
        booking_service = ConfBookingService()
        try:
            if not user_id:
                user_id = request.user.id
            response = booking_service.get_conf_booking(customer_user=user_id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        if not response:
            response = booking_service.create_default_conf_booking(cu=user_id)
        if user_id:
            booking_serializer = ConfBookingSerializer(response, many=False)
        else:
            booking_serializer = ConfBookingSerializer(response, many=True)
        return Response({"success": True, "data": booking_serializer.data}, status=status.HTTP_200_OK)

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
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_email_serializers = ConfBookingSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return ConfigurationBookingDto(
            customer_user=data["customer_user"],
            max_personas=data.get("max_personas", 0),
            time_bet_booking=data.get("time_bet_booking", 60),
            holiday=data.get("holiday", []),
            hora_inicio=data.get("hora_inicio", "08:00:00"),
            hora_fin=data.get("hora_inicio", "20:00:00"),
            status_conf=data.get("status_conf", 0),
            kids=data.get("kids", False),
            teen=data.get("teen", False),
        )


