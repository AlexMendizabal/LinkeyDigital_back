from rest_framework import serializers
from apps.booking.models import Booking, ConfigurationBooking

class Bookingserializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('__all__')
    code = serializers.CharField(required=False)

class Bookingserializers_public(serializers.ModelSerializer):
    class Meta:
        model = Booking 
        fields = ('id','date','code','status_booking',)
        
class PublicAllBookingserializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'date','status_booking')


class ConfBookingserializers(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationBooking
        fields = ('__all__')