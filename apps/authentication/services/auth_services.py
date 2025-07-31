
# Limpieza: Firebase y Pyrebase removidos. Estructura base para futura autenticación (Allauth/Django)




# Limpieza: Firebase removido. Métodos de usuario base para futura autenticación (Allauth/Django)
class Authservicess:
    def restartUser(self, user_id):
        # Eliminar redes sociales asociadas a un usuario
        CustomerUserCustomSocialMedia.objects.filter(customer_user=user_id).delete()
        return True

    def deleteUser(self, user_id):
        user = get_object_or_404(CustomerUser, id=user_id)
        user.is_active = False
        user.save()
        return True

    def getUser(self, user_id=None, uid=None):
        if user_id:
            user = get_object_or_404(CustomerUser, id=user_id)
        elif uid:
            user = get_object_or_404(CustomerUser, uid=uid)
        return user

    def getUsers(self, is_active=None, licencia_id=None, sin_licencia=None):
        filters = {}
        if is_active is not None:
            filters['is_active'] = is_active
        if licencia_id is not None:
            filters['licencia_id'] = licencia_id
        elif sin_licencia is not None:
            filters['licencia_id__isnull'] = bool(sin_licencia)
        user = CustomerUser.objects.filter(**filters).order_by("id")
        return user

    

