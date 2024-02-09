from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from booking.services import BookingService
from booking.serializer import BookingSerializer_public


class PUblicSearchBookingViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, codigo=None):
        if not codigo:
            return Response({"succes": False}, status=status.HTTP_400_BAD_REQUEST)
        
        # Apartado para obtener los dias disponibles
        bookingservice = BookingService()
        try: 
            bookings = bookingservice.get_booking_percode(code=codigo)
            booking_serializer = BookingSerializer_public(bookings, many=False)
            return Response({"success": True, "data": booking_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
