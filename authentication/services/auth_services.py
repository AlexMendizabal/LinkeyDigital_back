from rest_framework.generics import get_object_or_404

from profile.models import CustomerUserCustomSocialMedia
from authentication.models import CustomerUser

from firebase_admin import auth 
from authentication.authentication import app



class AuthServices:

    def restartUser(self, user_id):
        CustomerUserCustomSocialMedia.objects.filter(customer_user=user_id).delete()
        return True
    
    def deleteUser(self, user_id):
        user = get_object_or_404(CustomerUser, id=user_id)
        user.is_active = False
        user.save()
        return True
    
    def changeEmailFireBase(self, uid, new_email):
        # Parte para cambiar correo a traves de firebase
        updated_user = auth.update_user(uid, email=new_email, app=app)
        return True
