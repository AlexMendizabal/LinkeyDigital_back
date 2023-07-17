from rest_framework.generics import get_object_or_404
from django.db.models import Max

from profile.models import CustomerUserProfile
from authentication.models import CustomerUser
from rest_framework import serializers

from administration.models import Licencia
from administration.views import LicenciaSerializer, Utilities

#WAITING: poner los serializadores en sus archivos o lugares respectivos

class CustomerUserProfileSerializerLow(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserProfile
        fields = (
            'id','public_name', 
            'image')

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = (
            'id','email', 'rubro', 'is_editable', 'is_active', 'username', 'is_admin')

class ProfileService:
    def cantobjs(self):
        cantUsers = CustomerUser.objects.filter().count()
        cantLicencia = Licencia.objects.filter(status=1).count()
        cantLicenciaV = Licencia.objects.filter(status=2).count()
        cantLicenciaB = Licencia.objects.filter(status=3).count()

        
        return {"Usuarios": cantUsers, "Licencias vigentes": cantLicencia, "Licencias vencidas": cantLicenciaV, "Licencias bloqueadas": cantLicenciaB}
    def create_profile(self, dto):
        customer_user_profile, created = CustomerUserProfile.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_profile.public_id = dto.public_id
        customer_user_profile.career = dto.career
        customer_user_profile.public_name = dto.public_name
        customer_user_profile.description = dto.description
        customer_user_profile.save()
        return customer_user_profile
    
    def get_all_profile_licencia(self, licencia_id, id_admin = None):
        if not id_admin:
            customer_users = CustomerUser.objects.filter(licencia_id_id=licencia_id)
        else :
            customer_users = CustomerUser.objects.filter(licencia_id_id=licencia_id).exclude(id=id_admin)
        customer_user_profile = []
        
        for customer_user in customer_users:
            customer_user_id = customer_user.id
            profile = CustomerUserProfile.objects.get(customer_user_id=customer_user_id)
            #Sereliazamos el objeto pa que regrese bien
            customer_profile_serializers = CustomerUserProfileSerializerLow(profile, many=False)
            user_serializers = CustomerUserSerializer(customer_user, many=False)
            customer_user_profile.append({"profile": customer_profile_serializers.data, "customer_user": user_serializers.data })
        
        return customer_user_profile
    
    def get_all_profiles(self, rubro=None):
        # Obtener los customer_user_id más recientes
        latest_ids = Licencia.objects.values('customer_user_admin').annotate(max_id=Max('id'))
        # Obtener las licencias correspondientes a los customer_user_id más recientes
        licencias = Licencia.objects.filter(id__in=latest_ids.values('max_id'))
        response = []

        for licencia in licencias:
            custom_user = licencia.customer_user_admin
            if (rubro == "independiente" and custom_user.rubro == "independiente") or \
                    (rubro != "independiente" and custom_user.rubro != "independiente"):
                profile_user = CustomerUserProfile.objects.get(customer_user_id=custom_user.id)

                licencia_serializ = LicenciaSerializer(licencia, many=False)
                utilities = Utilities()
                data = licencia_serializ.data.copy ()
                data ['fecha_fin'] = utilities.calcular_fecha_fin(licencia_serializ.data['fecha_inicio'], licencia_serializ.data['duracion'])
                custom_user_serializ = CustomerUserSerializer(custom_user, many=False)

                profile_user_serializ = CustomerUserProfileSerializerLow(profile_user, many=False)

                response.append({"licencia": data, "custom_user": custom_user_serializ.data,
                                "profile": profile_user_serializ.data})

        return response

    
    def get_profile(self, pk=None, customer_user=None):
        if pk :
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user_id=pk)
        elif customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)
        else:
            customer_user_profile = CustomerUserProfile.objects.all()
        return customer_user_profile
    
    def get_users_by_licencia(self, licencia_id=None):

        if licencia_id:
            customer_users = CustomerUser.objects.filter(licencia_id_id = licencia_id)
        else:
            customer_users = None
        return customer_users
