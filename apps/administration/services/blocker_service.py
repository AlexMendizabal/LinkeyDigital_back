from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from apps.authentication.models import CustomerUser
from apps.administration.models import Licencia

class Blockersservices:
#README: metodo para bloquear usuarios... osea que no puedan entrar a sus perfiles
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
#README: metodo para bloquear usuarios... osea que no puedan editar sus perfiles
    def blockEditUser(self, value, pk=None, licencia_id=None):
        # si no llega licencia_id y solo pk
        if licencia_id is None and pk:
            user = get_object_or_404(CustomerUser, id=pk)
            user.is_editable = value
            user.save()
            return user
        # esta pregunta de redundancia sirve para filtrar que 
        # los administradores solo eliminen personas de su licencia
        elif pk and licencia_id:
            user = get_object_or_404(CustomerUser, id=pk, licencia_id_id = licencia_id)
            user.is_editable = value
            user.save()
            return user
        return None