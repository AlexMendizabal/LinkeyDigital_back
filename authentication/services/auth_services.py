from rest_framework.generics import get_object_or_404
import os
from profile.models import CustomerUserCustomSocialMedia
from authentication.models import CustomerUser
from conf_fire_base import bob_conf, cl_conf, br_conf, pg_conf, REGION_ACTUAL, \
                        bob_server, cl_server, br_server, pg_server
import pyrebase
import requests

class FireBaseConf: 
    # este constructor inicia los componentes basicos para pyrebase, no para el sdk admin
    def __init__(self):
        self.config = {}
        self.config["bob"] = {
        "apiKey": "AIzaSyDbkLm-AW1Ai6Qd8IoCG59_BtMPoO3NxfE",
        "authDomain": "soyyo-auth.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "storageBucket": "soyyo-auth.appspot.com",
        "serviceAccount": os.path.join(
            os.path.dirname(__file__), '../secrets/' + bob_conf)
        }
        self.config["cl"] = {
        "apiKey": "AIzaSyBNsUKCZ59ec93C2UCEKdpt3GzsrRqIfiA",
        "authDomain": "soyyochile-auth.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "storageBucket": "soyyochile-auth.appspot.com",
        "serviceAccount": os.path.join(
            os.path.dirname(__file__), '../secrets/' + cl_conf)
        }
        self.config["br"] = {
        "apiKey": "AIzaSyBc9_kqRbPTO6Vypx3IV-l7k5bzWkkfhYE",
        "authDomain": "soueudigital-auth.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "storageBucket": "soueudigital-auth.appspot.com",
        "serviceAccount": os.path.join(
            os.path.dirname(__file__), '../secrets/' + br_conf)
        }
        self.config["pg"] = {
        "apiKey": "AIzaSyBL_ZshO-9H5armvM47SzfRy684gHrW0Dg",
        "authDomain": "epadigital-auth-1ccf2.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "storageBucket": "epadigital-auth.appspot.com",
        "serviceAccount": os.path.join(
            os.path.dirname(__file__), '../secrets/' + pg_conf)
        }

        self.firebase_apps = {}
        for key, config in self.config.items():
            self.firebase_apps[key] = pyrebase.initialize_app(config)

    # metodos con el id public pyrebase
    def loginFireBase(self, email, password, region = REGION_ACTUAL):
        if region not in self.firebase_apps:
            return None  
        try:
            auth = self.firebase_apps[region].auth()
            user = auth.sign_in_with_email_and_password(email, password)
            return user
        except Exception as e:
            return None



class AuthServices:
    from firebase_admin import auth
    from authentication.authentication import app

    def restartUser(self, user_id):
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
    
        # metodos con el sdk
    def changeEmailFireBase(self, uid, new_email, region = REGION_ACTUAL):
        # Parte para cambiar correo a traves de firebase
        updated_user = self.auth.update_user(uid, email=new_email, app=self.app)
        return True
    
    def make_register_in_alt_server(self, token, server ): 
        headers = {
            "Authorization" : token
        }
        if server == "bob": url = bob_server
        elif server == "cl": url = cl_server
        elif server == "br": url = br_server
        elif server == "pg": url = pg_server

        response = requests.post(f"{url}auth/register", headers=headers)
        if response.status_code == 200:
            return response.json()
        
        return None

    

