from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booking.services import BookingService
from booking.serializer import PublicAllBookingSerializer
from datetime import datetime


class PublicBusyViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, user=None):
        if not user:
            return Response({"succes": False}, status=status.HTTP_400_BAD_REQUEST)

        booking_service = BookingService()
        try:
            date_time_str = request.GET.get('date', datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            response = booking_service.get_booking_perday(customer_user=user, specific_date=date_time_str)
        except Exception as e:
            return Response({"succes": False, "message": "Error al procesar la fecha"}, status=status.HTTP_404_NOT_FOUND)
        if response is None:
            return Response({"success": False, "message": "Fecha inválida"}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(response, list):  # Verifica si es una lista
            many = True
        else:
            many = False
            
        booking_serializer = PublicAllBookingSerializer(response, many=many)
        return Response({"success": True, "data": booking_serializer.data}, status=status.HTTP_200_OK)

