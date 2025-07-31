from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from apps.booking.models import Booking, BookingDto
from apps.booking.services import Bookingservices

from apps.administration.UtilitiesAdministration import UtilitiesAdm
from apps.booking.serializers import Bookingserializers

class BookingViewset(APIView):
    def get(self, request, pk=None):

        if not pk:
            pk = request.user.id
        
        all = request.GET.get('all', False)

        #TODO: Implementar seguridad del metodo a aplicar 
        #TODO: Implementar paginacion para hacer mas eficiente

        # utilitiesAdm = UtilitiesAdm()
        # if not utilitiesAdm.hasPermision(request.user, user_id):
        #     return Response({"status": "error"}, status=status.HTTP_401_UNAUTHORIZED)
        # booking_serializers = Bookingserializers(data=request.data)
        # user_id = request.GET.get('user_id', request.user.id)

        booking_services = Bookingservices()
        try:
            response = booking_services.get_booking_today(customer_user=pk, all=all)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)
        booking_serializers = Bookingserializers(response, many=True)
        return Response({"success": True, "data": booking_serializers.data}, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        # utilitiesAdm = UtilitiesAdm()
        # if not utilitiesAdm.hasPermision(request.user, user_id):
        #     return Response({"status": "error"}, status=status.HTTP_401_UNAUTHORIZED)
        # booking_serializers = Bookingserializers(data=request.data)

        try:
            booking = get_object_or_404(Booking, id=pk)
            customer_user_serializers = Bookingserializers(instance=booking, data=request.data, partial=True)
            customer_user_serializers.is_valid(raise_exception=True)
            customer_user_serializers.save()
            
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        
        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)


