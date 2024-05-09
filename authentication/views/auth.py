from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .customer_user_viewset import CustomerUserSerializer
from authentication.services import AuthServices, FireBaseConf
from firebase_admin import auth
from conf_fire_base import  MODES, REGION_ACTUAL


class AuthenticatedView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    authentication_classes = []

    def post(self, request):      
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        fireBaseConf = FireBaseConf()
        authServices = AuthServices()
        user_firebase = fireBaseConf.loginFireBase(email, password)
        # si no lo encuentra en bob hara la busqueda en otros servidores 
        if not user_firebase: 
            for mod in MODES:
                # que no se haga la consulta al mismo server
                if not mod == REGION_ACTUAL:
                    user_firebase = fireBaseConf.loginFireBase(email, password, mod)
                    # si encuentra el user
                    if user_firebase: 
                        user = authServices.make_register_in_alt_server(f"JWT {user_firebase['idToken']}", mod)
                        if not user: return Response({"Mensaje": "Error al conectar servidores"}, status=status.HTTP_404_NOT_FOUND)
                        return Response({'Token': f"JWT {user_firebase['idToken']}" , 
                         'email' : user["data"]["email"],
                         'username' : user["data"]["username"],
                         'region' : mod
                         })
            
            #return Response({"Mensaje": "Usuario o contraseña incorrectos"}, status=status.HTTP_401_UNAUTHORIZED)
        # caso de que si lo haya encontrado... seguira con su vida normal sacando el user de la db :v    
        user = authServices.getUser(uid=user_firebase["localId"])

        return Response({'Token': f"JWT {user_firebase['idToken']}" , 
                         'email' : user_firebase['email'],
                         'username' : user.username,
                         'region' : "Bob"
                         })


"""
Creacion de cuenta e inicio de sesion con correo electronico y contraseña
"""


class RegisterUser(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):

        user_firebase = auth.get_user(request.user.uid)
        if request.user.email != user_firebase.email:
            request.user.email = user_firebase.email
            request.user.save()
        
        user_serializer = CustomerUserSerializer(request.user, many=False)
        return Response({'message': 'User Registered','data': user_serializer.data })
