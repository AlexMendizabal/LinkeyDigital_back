
from pay.models import Transaction, DetalleTransaction, Discount, DetalleTransaction
from pay.models import Productos

from administration.views import Utilities
from authentication.views import create_users_in_threads
from contact.services import SendEmail
from contact import GetHtmlForEmail
from django.shortcuts import get_object_or_404

from decimal import Decimal
from django.utils import timezone
import string
import secrets

from conf_fire_base import REGION_ACTUAL

class PayService:
    
    def get_transactions(self, customer_user=None):
        if customer_user:
            transaction = Transaction.objects.filter(customer_user = customer_user).order_by('id')
        else:
            return None
        return transaction
    def get_detalle_transaccion(self, id_transaccion=None):
        if id_transaccion:
            transaction = DetalleTransaction.objects.filter(transaction = id_transaccion).order_by('id')
        else:
            return None
        return transaction
    
    def create_transaction(self, dto):
        transaction = Transaction.objects.create(
            customer_user=dto.customer_user,
            discount_id=dto.discount_id,
            discount_value=dto.discount_value,
            status=dto.status,
            canal =dto.canal,
            monto =dto.monto,
            moneda =dto.moneda,
            telefono =dto.telefono,
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
    
    #WAITING: Poner costo_envio en algun documento de conf, para no tener que estarlo buscando
    def get_precio_envio(self, ciudad, pais="Bolivia"):
        costo_envio = 0
        if pais == "Bolivia" or pais == "bolivia":
            if ciudad != "Santa Cruz":
                costo_envio = 40
        return costo_envio

    def generar_codigo_unico(self):
        caracteres = string.ascii_letters + string.digits  # Usar letras y dígitos
        longitud = 10
        codigo_unico = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        return codigo_unico
    
    def get_discount(self, monto_pedido, verification_code=False):
        descuento = 0
        cupon = None
        if verification_code:
            try:
                cupon = get_object_or_404(Discount, verification_code=verification_code)
                discount_rate = float(cupon.discount_rate)
                if(cupon.discount_type == "percentage"):
                    descuento = monto_pedido* discount_rate / 100

                if(cupon.discount_type == "price"):
                    descuento = discount_rate

                if not cupon.es_valido():
                    descuento = 0

            except Exception:
                descuento = 0 

            descuento = round( descuento, 2)
        return descuento , cupon

    def get_price_by_id_producto(self, detalles):
        try:
            monto = Decimal(0)
            for producto in detalles:
                price = Productos.objects.get(id=producto["producto"])
                price = price.price
                monto += Decimal(price) * int(producto["cantidad"])
        except Exception as e:
            raise Exception("El producto no está disponible") 
        return monto
    
    def validar_id_tracaccion(self, id, codigo):
        try:
            #resp = Transaction.objects.get(id_transaccion = id, codigoTransaccion = codigo)
            resp = Transaction.objects.get(codigoTransaccion = codigo)
            if not resp:
                return None
        except Exception as e:
            return None
        return resp
    
    def guardar_datos_webHook(self, estatus, resp):
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
            monto = round(resp.monto, 2)
            licencia = {
                
                "tipo_de_plan": "" ,
                "fecha_inicio" : timezone.now() , 
                "cobro" : monto ,
                "duracion" : 730, 
                "status" : 1
            }

            # booleano para ver si hay tarjetas en la compra o no
            new_user_bool = False
            #logica para buscar la cantiad de usuarios requeridos
            detalleProductos = DetalleTransaction.objects.filter(transaction_id = resp.id)
            #ponemos -1 porque el usuario que compro ya tiene cuenta.
            cantidad = -1
            # accesorio
            for detalle in detalleProductos:
                if detalle.producto.type == "tarjeta": 
                    cantidad += int(detalle.cantidad)
                    new_user_bool = True

            if new_user_bool:
                #crea la licencia del usuario y lo actualiza
                utilities = Utilities()
                response = utilities.create_licencia_DTO(licencia)
                user.licencia_id_id = response
                user.save()
                #crea los usuarios restantes en la licencia y ademas les pone la misma licencia
                #creada anteriormente 
                correo_inicio = user.username
                if cantidad > 0 :
                    errors, corrects = create_users_in_threads(cantidad, correo_inicio, response.id)

                if REGION_ACTUAL == "br":
                    #funcion para mandar correo 
                    subject = "Confirmação de Pagamento Bem-Sucedida!"
                    email = user.email

                    # # funcion para mandar correo al supervisor 
                    subject_s = "Cópia de confirmação de Pagamento Bem-Sucedido!"
                    email_s = "contacto@linkey.digital"
                elif REGION_ACTUAL == "bob":
                    #funcion para mandar correo 
                    subject = "¡Confirmación de Pago Exitosa!"
                    email = user.email

                    # # funcion para mandar correo al supervisor 
                    subject_s = "¡Copia de confirmación de Pago Exitosa!"
                    email_s = "contacto@linkey.digital"
                
                if cantidad > 0 :
                    body = GetHtmlForEmail(user,monto,corrects,REGION_ACTUAL)
                else :
                    body = GetHtmlForEmail(user,monto, region= REGION_ACTUAL)
                # SendEmail(subject,email,body)
                # SendEmail(subject_s,email_s,body)

        except Exception as e:
            return False
        
        return True