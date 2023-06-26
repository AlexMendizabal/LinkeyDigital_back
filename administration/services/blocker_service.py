from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from authentication.models import CustomerUser
from administration.models import Licencia

class BlockersService:
# este metodo es para bloquear usuarios
    def blockUser(self, pk=None, licencia_id=None):
        # si no llega licencia_id y solo pk
        if licencia_id is None and pk:
            user = get_object_or_404(CustomerUser, id=pk)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            return user
        # esta pregunta de redundancia sirve para filtrar que 
        # los administradores solo eliminen personas de su licencia
        elif pk and licencia_id:
            user = get_object_or_404(CustomerUser, id=pk, licencia_id_id = licencia_id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            return user
        return None
