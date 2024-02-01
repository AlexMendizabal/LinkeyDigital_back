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
        # bookingservice = BookingService()
        # try: 
        #     day = request.GET.get('day', date.today().isoformat())
        #     bookings = bookingservice.get_booking_perday(customer_user=user, specific_date=day)
        #     booking_serializer = BookingSerializer(bookings, many=True)
        # except Exception as e:
        #     return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        # Apartado para obtener la conf 
        booking_service = ConfBookingService()
        #utilities = CustomUserUtilities()
        try:
            # customer_user = utilities.getUsers(user)
            # user_id = customer_user.id
            response = booking_service.get_conf_booking(customer_user=user)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        if not response:
            response = booking_service.create_or_update_conf_booking(cu=user)
        if user:
            conf_booking_serializer = ConfBookingSerializer(response, many=False)
        else:
            conf_booking_serializer = ConfBookingSerializer(response, many=True)
            #"booking" : booking_serializer.data
        return Response({"success": True, "data": {"configuration" :conf_booking_serializer.data, } }, status=status.HTTP_200_OK)



