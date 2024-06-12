from django.http import JsonResponse
from django.views import View
from authentication.models.customer_user import CustomerUser

class ListSponsorUsersView(View):
    def get(self, request):
        # Filtra los usuarios que sean sponsors
        sponsor_users = CustomerUser.objects.filter(is_sponsor=True)

        # Serializa los datos de los usuarios
        sponsor_user_data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # Agrega más campos según sea necesario
            }
            for user in sponsor_users
        ]

        # Devuelve los datos serializados como respuesta JSON
        return JsonResponse({'sponsor_users': sponsor_user_data})
