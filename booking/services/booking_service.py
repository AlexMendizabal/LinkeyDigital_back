from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from ..models import Booking, BookingDto


class BookingService:

    def get_booking(self, pk=None, customer_user=None):
        if pk and customer_user:
            booking = get_object_or_404(Booking, pk=pk, customer_user=customer_user)
        elif pk:
            booking = get_object_or_404(Booking, pk=pk)
        else: 
            booking = Booking.objects.all()
        return booking
    
    def create_or_update_booking(self, dto):
        booking, created = Booking.objects.update_or_create(
            customer_user=dto.customer_user,
        adults = dto.adults,
        kids = dto.kids,
        nombre = dto.nombre,
        date = dto.date,
        teen = dto.teen,
        email = dto.email,
        phone = dto.phone)
        #booking.save()
        return booking
    