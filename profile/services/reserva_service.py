from rest_framework.generics import get_object_or_404

from profile.models import CustomerUserReserva

class ReservaService:
    
    def get_reserva(self, pk=None, custome_user_social_media=None):
        if pk and custome_user_social_media:
            customer_user_reserva_media = get_object_or_404(CustomerUserReserva, pk=pk, custome_user_social_media=custome_user_social_media)
        elif custome_user_social_media:
            customer_user_reserva_media = CustomerUserReserva.objects.all().filter(custome_user_social_media=custome_user_social_media)
        else:
            customer_user_reserva_media = CustomerUserReserva.objects.all()
        return customer_user_reserva_media