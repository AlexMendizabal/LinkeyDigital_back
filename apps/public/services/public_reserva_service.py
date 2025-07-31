from rest_framework.generics import get_object_or_404

from apps.profile.models import CustomerUserReserva

class Reservaservices:
    def create_or_update_reserva(self, dto):
        customer_user_reserva_media, created = CustomerUserReserva.objects.update_or_create(
            custome_user_social_media=dto.custome_user_social_media, date=dto.date
        )     
        customer_user_reserva_media.adults = dto.adults
        customer_user_reserva_media.kids = dto.kids
        customer_user_reserva_media.date = dto.date
        customer_user_reserva_media.Nombre = dto.Nombre
        customer_user_reserva_media.Email = dto.Email
        customer_user_reserva_media.phone = dto.phone
        
        customer_user_reserva_media.save()
        return customer_user_reserva_media
    