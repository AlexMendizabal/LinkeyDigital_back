from authentication.models import CustomerUser

class UtilitiesAdm():
    def is_from_same_license(self, usr, usr2):
        try:
            #preguntamos si es numerico, si lo es sifnifica que se obtuvo el id.. porlo que traeremos el user
            # pero si no lo es significa que ya es tipo user...
            if isinstance(usr2, int):
                usr2 = CustomerUser.objects.get(id = usr2)
            if isinstance(usr, int):
                usr = CustomerUser.objects.get(id = usr)

            if usr.licencia_id_id ==  usr2.licencia_id_id:
                return True
            
            return False
        except Exception as e:
            return False
    
    def hasPermision(self, user_que_solicita, user_al_que_le_aplica_los_cambios= None):
        if not user_que_solicita.is_superuser:
            if not user_que_solicita.is_admin:
                #preguntamos si es numerico, si lo es sifnifica que se obtuvo el id.. porlo que traeremos el user
                # pero si no lo es significa que ya es tipo user...
                if isinstance(user_al_que_le_aplica_los_cambios, int):
                    user_al_que_le_aplica_los_cambios = CustomerUser.objects.get(id = user_al_que_le_aplica_los_cambios)

                if user_que_solicita.id != user_al_que_le_aplica_los_cambios.id:
                    return False

            if not self.is_from_same_license(user_que_solicita, user_al_que_le_aplica_los_cambios):
                    return False

        return True