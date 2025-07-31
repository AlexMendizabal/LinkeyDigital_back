from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.booking.services import ConfBookingservices

#from administration.UtilitiesAdministration import UtilitiesAdm

from apps.booking.serializers import ConfBookingserializers
from apps.public.views import CustomUserUtilities

#from public.views import CustomUserUtilities


class PublicConfBookingViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, user=None):
        if not user:
            return Response({"succes": False}, status=status.HTTP_400_BAD_REQUEST)
        # Apartado para obtener la conf 
        booking_services = ConfBookingservices()
        #utilities = CustomUserUtilities()
        try:
            response = booking_services.get_conf_booking(customer_user=user)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        if not response:
            response = booking_services.create_or_update_conf_booking(cu=user)
        if user:
            conf_booking_serializers = ConfBookingserializers(response, many=False)
        else:
            conf_booking_serializers = ConfBookingserializers(response, many=True)
        return Response({"success": True, "data": conf_booking_serializers.data }, status=status.HTTP_200_OK)



