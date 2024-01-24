from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from booking.models import Booking, BookingDto
from booking.services import BookingService

from administration.UtilitiesAdministration import UtilitiesAdm

from booking.serializer import BookingSerializer

class PublicBookingViewset(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, user_id=None):

        booking_serializer = BookingSerializer(data=request.data)

        if not booking_serializer.is_valid():
            return Response({"status": "error", "data": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        dto = self.buid_dto_from_validated_data(booking_serializer)
        booking_service = BookingService()

        try:
            response = booking_service.create_booking(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        customer_email_serializers = BookingSerializer(response, many=False)
        return Response({"success": True, "data": customer_email_serializers.data}, status=status.HTTP_200_OK)

    def buid_dto_from_validated_data(self, serializer):
        data = serializer.validated_data
        return BookingDto(
            adults=data.get("adults", 1),
            kids=data.get("kids", 0),
            teen=data.get("teen", 0),
            date=data["date"],
            nombre=data["nombre"],
            email=data["email"],
            phone=data["phone"],
            customer_user=data["customer_user"],
        )

