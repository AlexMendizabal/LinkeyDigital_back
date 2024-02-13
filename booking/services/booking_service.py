from datetime import datetime, date
from rest_framework.generics import get_object_or_404
from ..models import Booking

class BookingService:
    
    def get_booking_today(self, pk=None, customer_user=None, all = False):
        today = date.today()
        if not all:
            bookings = Booking.objects.filter(date__gte=datetime.combine(today, datetime.min.time())).order_by('date')
        else: 
            bookings = Booking.objects.filter().order_by('date')
        if pk:
            bookings = bookings.filter(pk=pk)
        if customer_user:
            bookings = bookings.filter(customer_user=customer_user)
        return bookings
    
    def get_booking_percode(self, code):
        booking = get_object_or_404(Booking, code=code)
        return booking
    
    def get_booking_perday(self, pk=None, customer_user=None, specific_date=None, specific_hour=False):
        try:
            date_obj = datetime.strptime(specific_date, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
        
        if specific_hour:
            sh = date_obj.time()
            bookings = Booking.objects.filter(date__date=date_obj.date(), date__time=sh).order_by('date')
        else:
            bookings = Booking.objects.filter(date__date=date_obj.date()).order_by('date')

        if pk:
            bookings = bookings.filter(pk=pk)
        if customer_user:
            bookings = bookings.filter(customer_user=customer_user)
        return list(bookings)

    
    def get_bookings_count(self, customer_user, status=0):
        count = Booking.objects.filter(customer_user=customer_user, status_booking = status).count()
        return count
    
    def create_booking(self, dto):
        booking = Booking.objects.create(
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
    