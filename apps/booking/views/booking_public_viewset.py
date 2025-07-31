from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from apps.booking.models import  BookingDto
from apps.booking.services import Bookingservices, ConfBookingservices
from apps.booking.serializers import Bookingserializers
from datetime import datetime

class PublicBookingViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, user_id=None):

# Validaciones del codigo:
        # # validacion de la fecha y hora
        # now = datetime.now()
        # date_time_str = request.data.get('date')
        # # Validar que la fecha y hora no sean None
        # if date_time_str is None:
        #     return Response({"status": "error", "message": "La fecha y hora de la reserva son obligatorias"}, status=status.HTTP_400_BAD_REQUEST)
        # # Validar que la fecha y hora no sean antiguas
        # try:
        #     date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        # except ValueError:
        #     return Response({"status": "error", "message": "Formato de fecha y hora no válido"}, status=status.HTTP_400_BAD_REQUEST)
        # if date_time < now:
        #     return Response({"status": "error", "message": "La fecha y hora de la reserva no pueden ser anteriores a la fecha y hora actual"}, status=status.HTTP_400_BAD_REQUEST)
        
        # validacion de reserva no repetida 
        # booking_services = Bookingservices()
        # cu = request.data.get('customer_user')
        # booking = booking_services.get_booking_perday(customer_user=cu, specific_date=date_time_str, specific_hour=True)
        # if booking:
        #     conf_booking_services = ConfBookingservices()
        #     conf_booking = conf_booking_services.get_conf_booking(customer_user=cu)
        #     max_reservas = conf_booking.max_reservas
        #     if len(booking) >= max_reservas:
        #         return Response({"status": "error", "message": "Parece que ya no hay espacio para reservas"}, status=status.HTTP_409_CONFLICT)


        booking_serializers = Bookingserializers(data=request.data)

        if not booking_serializers.is_valid():
            return Response({"status": "error", "data": booking_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(booking_serializers)
        booking_services = Bookingservices()

        try:
            response = booking_services.create_booking(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_email_serializers = Bookingserializers(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
        return BookingDto(
            adults=data.get("adults", 1),
            kids=data.get("kids", 0),
            teen=data.get("teen", 0),
            date=data["date"],
            nombre=data["nombre"],
            email=data["email"],
            phone=data["phone"],
            customer_user=data["customer_user"],
            description=data.get("description", ""),
            booking_configuration=data.get("booking_configuration"),
        )

