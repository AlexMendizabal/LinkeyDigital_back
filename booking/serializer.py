from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'id', 'customer_user', 'adults', 'kids', 'teen', 'date','created_at', 'nombre', 
            'email', 'phone', 'status_booking', 'code')
    code = serializers.CharField(required=False)