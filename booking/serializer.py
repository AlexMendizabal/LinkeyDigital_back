from rest_framework import serializers
from booking.models import Booking, ConfigurationBooking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'id', 'customer_user', 'adults', 'kids', 'teen', 'date','created_at', 'nombre', 
            'email', 'phone', 'status_booking', 'code')
    code = serializers.CharField(required=False)


class ConfBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationBooking
        fields = (
            'id', 'customer_user', 'max_personas', 'time_bet_booking', 'holiday', 
            'hora_inicio','hora_fin', 'status_conf', 
            'kids', 'teen')