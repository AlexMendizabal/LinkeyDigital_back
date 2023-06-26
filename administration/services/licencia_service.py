from dataclasses import dataclass
from rest_framework.generics import get_object_or_404

from authentication.models import CustomerUser
from administration.models import Licencia


class LicenciaService:
    #retorna la licencia del usuario
    def get_licencia(self, licencia_id=None):
        if licencia_id:
            licencias = get_object_or_404(Licencia, id=licencia_id)
        else :
            licencias = None
        return licencias
    #retorna los usuarios adjuntos a una licencia menos al administrador(esta solicitud es solo para admins)
    def get_Users(self, licencia_id=None, custom_user_admin_id = None, with_admin = False):
        if with_admin and licencia_id and custom_user_admin_id:
            users = CustomerUser.objects.filter(licencia_id=licencia_id)
        elif licencia_id and custom_user_admin_id:
            users = CustomerUser.objects.filter(licencia_id=licencia_id).exclude(id=custom_user_admin_id)
        else :
            users = None
        return users
    #retorna todas las licencias existentes
    def get_licencias_super(self):
        licencias = Licencia.objects.all()
        return licencias
    
    def createLicencia(self, dto , customer_user_admin= None):
        licencia = Licencia.objects.create(
            customer_user_admin=dto.customer_user_admin, tipo_de_plan=dto.tipo_de_plan, fecha_inicio=dto.fecha_inicio, cobro=dto.cobro,
            duracion=dto.duracion, status=dto.status)
        if customer_user_admin is not None:
            print(licencia.id)
            CustomerUser.objects.filter(id=customer_user_admin).update(licencia_id=licencia.id, is_admin=True)
        return licencia
    #actualiza al usuario con la pk de la licencia 
    def connectLicencia(self, pk, custom_user_id):
        user = CustomerUser.objects.filter(id=custom_user_id)
        user.update(licencia_id=pk)
        return user
    # update licencia(para extencion de plazo entre otros)
    # En el servicio
    def updateLicencia(self, pk, type=None, cobro=None, duracion=None, status=None, customer_user_admin=None):

        licencia = Licencia.objects.get(id=pk) # Usar get() en vez de filter()
        if type is not None:
            licencia.tipo_de_plan = type # Usar asignación directa en vez de update()
        if cobro is not None:
            licencia.cobro = cobro
        if duracion is not None:
            licencia.duracion = duracion
        if status is not None:
            licencia.status = status
        if customer_user_admin is not None:
            user_antiguo = CustomerUser.objects.get(id=licencia.customer_user_admin_id)
            user_nuevo = CustomerUser.objects.get(id=customer_user_admin)
            user_antiguo.is_admin = False
            user_nuevo.is_admin = True
            user_antiguo.save()
            user_nuevo.save()
            licencia.customer_user_admin = user_nuevo
        licencia.save() # Guardar los cambios en la base de datos
        return licencia

    