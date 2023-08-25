
from pay.models import Transaction, DetalleTransaction
from pay.models import Productos

from administration.views import LicenciaSerializer, Utilities
from administration.services import LicenciaService
from authentication.views import CreateUserThread, create_users_in_threads
from contact.services import SendEmail
from contact import GetHtmlForEmail

from decimal import Decimal
from django.utils import timezone

class PayService:
    
    def get_transactions(self, customer_user=None):
        if customer_user:
            transaction = Transaction.objects.filter(customer_user = customer_user).order_by('id')
        else:
            return None
        return transaction
    def create_transaction(self, dto):
        transaction = Transaction.objects.create(
            customer_user=dto.customer_user,
            status=dto.status,
            canal =dto.canal,
            monto =dto.monto,
            moneda =dto.moneda,
            descripcion =dto.descripcion,
            nombreComprador =dto.nombreComprador,
            apellidoComprador=dto.apellidoComprador,
            documentoComprador =dto.documentoComprador,
            modalidad =dto.modalidad,
            extra1 =dto.extra1,
            extra2 =dto.extra2,
            extra3 =dto.extra3,
            direccionComprador =dto.direccionComprador,
            ciudad =dto.ciudad,
            codigoTransaccion=dto.codigoTransaccion,
            urlRespuesta =dto.urlRespuesta,
            id_transaccion =dto.id_transaccion,
        ) 
        return transaction
    
    def create_Detalle_transaction(self, dto):
        transaction = DetalleTransaction.objects.create(
            producto=dto.producto,
            transaction=dto.transaction,
            cantidad=dto.cantidad,
        ) 
        return transaction

    def get_price_by_id_producto(self, detalles):
        try:
            monto = Decimal(0)
            for producto in detalles:
                price = Productos.objects.get(id=producto["producto"])
                price = price.price
                monto += Decimal(price) * int(producto["cantidad"])
        except Exception as e:
            print(e)
            raise Exception("El producto no está disponible") 
        return monto
    
    def validar_id_tracaccion(id, codigo):
        try:
            resp = Transaction.objects.get(id_transaccion = id, codigoTransaccion = codigo)
            if not resp:
                return None
        except Exception as e:
            print(str(e))
            return None
        return resp
    
    def guardar_datos_webHook( estatus, resp):
        try:
            #cambiamos el status
            estatus = int(estatus)
            if estatus == 0:
                status = 2
            else:
                status = 1
                resp.status = status
                resp.save()
                return False

            resp.status = status
            resp.save()
            user = resp.customer_user
            monto = resp.monto
            data = {
                
                "tipo_de_plan": "" ,
                "fecha_inicio" : timezone.now() , 
                "cobro" : monto ,
                "duracion" : 730, 
                "status" : 1
            }
            #crea la licencia del usuario y lo actualiza
            utilities = Utilities()
            response = utilities.createDTO(data)
            user.licencia_id = response
            user.save()

            #logica para buscar la cantiad de usuarios requeridos
            detalleProductos = DetalleTransaction.objects.filter(transaction_id = resp.id)
            #ponemos -1 porque el usuario que compro ya tiene cuenta.
            cantidad = -1
            for detalle in detalleProductos:
                cantidad += int(detalle.cantidad)
            #crea los usuarios restantes en la licencia y ademas les pone la misma licencia
            #creada anteriormente 
            if cantidad > 0 :
                errors, corrects = create_users_in_threads(cantidad, "soyyo", response.id)

            #funcion para mandar correo 
            subject = "¡Confirmación de Pago Exitosa!"
            email = user.email

            if cantidad > 0 :
                body = GetHtmlForEmail(user,monto,corrects)
            else :
                body = GetHtmlForEmail(user,monto)
            SendEmail(subject,email,body)

            # funcion para mandar correo al supervisor 

            subject = "¡Copia de confirmación de Pago Exitosa!"
            email = "contacto@soyyo.digital"
            SendEmail(subject,email,body)
            # funcion para mandar al front

        except Exception as e:
            print(str(e))
            return False
        
        return True