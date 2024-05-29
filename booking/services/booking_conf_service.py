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

    def create_or_update_conf_booking(self, dto=None, cu=None):
        if not cu is None:
            customer_user =  get_object_or_404(CustomerUser, pk=cu)
            booking_conf, created = ConfigurationBooking.objects.update_or_create(
            customer_user=customer_user)
            return booking_conf
        update_fields = {}
        if dto.max_personas is not None:
            update_fields['max_personas'] = dto.max_personas
        if dto.max_reservas is not None:
            update_fields['max_reservas'] = dto.max_reservas
        if dto.time_bet_booking is not None:
            update_fields['time_bet_booking'] = dto.time_bet_booking
        if dto.holiday is not None:
            update_fields['holiday'] = dto.holiday
        if dto.hora_inicio is not None:
            update_fields['hora_inicio'] = dto.hora_inicio
        if dto.hora_fin is not None:
            update_fields['hora_fin'] = dto.hora_fin
        if dto.hora_inicio_tarde is not None:
            update_fields['hora_inicio_tarde'] = dto.hora_inicio_tarde
        if dto.hora_fin_tarde is not None:
            update_fields['hora_fin_tarde'] = dto.hora_fin_tarde
        if dto.hora_inicio_noche is not None:
            update_fields['hora_inicio_noche'] = dto.hora_inicio_noche
        if dto.hora_fin_noche is not None:
            update_fields['hora_fin_noche'] = dto.hora_fin_noche
        if dto.status_conf is not None:
            update_fields['status_conf'] = dto.status_conf
        if dto.kids is not None:
            update_fields['kids'] = dto.kids
        if dto.teen is not None:
            update_fields['teen'] = dto.teen
        if dto.btn is not None:
            update_fields['btn'] = dto.btn
        if dto.phone is not None:
            update_fields['phone'] = dto.phone
        if dto.email is not None:
            update_fields['email'] = dto.email
        if dto.description is not None:
            update_fields['description'] = dto.description
        if dto.title is not None:
            update_fields['title'] = dto.title

        booking_conf, created = ConfigurationBooking.objects.update_or_create(
            customer_user=dto.customer_user,
            defaults=update_fields
        )
        return booking_conf

    