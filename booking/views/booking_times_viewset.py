from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date

#from booking.models import ConfigurationBooking,ConfigurationBookingDto
from booking.services import ConfBookingService, BookingService

#from administration.UtilitiesAdministration import UtilitiesAdm

from booking.serializer import ConfBookingSerializer, BookingSerializer

#from public.views import CustomUserUtilities


class PublicConfBookingViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, user=None):
        if not user:
            return Response({"succes": False}, status=status.HTTP_400_BAD_REQUEST)
        
        # Apartado para obtener los dias disponibles
        bookingservice = BookingService()
        try: 
            day = request.GET.get('day', date.today().isoformat())
            bookings = bookingservice.get_booking_perday(customer_user=user, specific_date=day)
            booking_serializer = BookingSerializer(bookings, many=True)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)