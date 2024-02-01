from rest_framework import serializers
from booking.models import Booking, ConfigurationBooking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('__all__')
    code = serializers.CharField(required=False)


class ConfBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationBooking
        fields = ('__all__')