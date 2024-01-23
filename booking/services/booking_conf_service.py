from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from ..models import ConfigurationBooking, ConfigurationBookingDto
from authentication.models import CustomerUser


class ConfBookingService:

    def get_conf_booking(self, pk=None, customer_user=None):
        if pk and customer_user:
            booking = ConfigurationBooking.objects.filter(pk=pk, customer_user=customer_user).first()
        elif pk:
            booking = ConfigurationBooking.objects.filter(pk=pk).first()
        elif customer_user:
            booking = ConfigurationBooking.objects.filter(customer_user=customer_user).first()
        else: 
            booking = None
        return booking

    def create_default_conf_booking(self, cu):
        customer_user =  get_object_or_404(CustomerUser, pk=cu)

        booking_conf, created = ConfigurationBooking.objects.update_or_create(
            customer_user=customer_user,
            max_personas = 10,
            time_bet_booking = 0,
            holiday = "[]",
            hora_inicio = "07:00:00",
            hora_fin = "20:00:00",
            status_conf =0 ,
            kids = False,
            teen = False)
        return booking_conf
    
    def create_or_update_conf_booking(self, dto):
        booking_conf, created = ConfigurationBooking.objects.update_or_create(
            customer_user=dto.customer_user,
        max_personas = dto.max_personas,
        time_bet_booking = dto.time_bet_booking,
        holiday = dto.holiday,
        hora_inicio = dto.hora_inicio,
        hora_fin = dto.hora_fin,
        status_conf = dto.status_conf,
        kids = dto.kids,
        teen = dto.teen)
        return booking_conf

    