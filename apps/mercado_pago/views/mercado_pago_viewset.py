from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from conf_fire_base import MERCADOPAGO_SECRET_KEY, BRASIL_MODE, DOMINIO_NAME
import mercadopago
from django.db import transaction
from apps.pay.utilitiesPay import UtilitiesPay, Transactionserializers, DetalleTransactionserializers
from apps.pay.services.transactionService import Payservices

class MercadoPago(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                #validar datos del formulario 
                data = request.data
                required_fields = [
                    "canal",
                    "moneda",
                    "descripcion",
                    "nombreComprador",
                    "apellidoComprador",
                    "correo",
                    "telefono",
                    "modalidad",
                    "ciudad",
                    "direccionComprador",
                    "detalle"

                ]
                # Verificar si todos los campos requeridos están presentes
                if not all(field in data for field in required_fields):
                    return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

                # calculamos el precio
                transaction_services = Payservices()
                monto_pedido = float(transaction_services.get_price_by_id_producto(data["detalle"]))

                ciudad = data.get("ciudad", "")
                pais = data.get("pais", "Bolivia")
                costo_envio = transaction_services.get_precio_envio(ciudad, pais)

                #obtener el descuento 
                verification_code = data.get("verificationCode", False)
                descuento , cupon = transaction_services.get_discount(monto_pedido,verification_code)
                descuento = int(descuento)
                sdk = mercadopago.SDK(MERCADOPAGO_SECRET_KEY)
                # Obtener datos del formulario de pago
                monto = monto_pedido - descuento + costo_envio
                data["monto"] = str(monto)
                codigoTransaccion = transaction_services.generar_codigo_unico()
                data["codigoTransaccion"] = codigoTransaccion
                data["urlRespuesta"] = f"https://www.{DOMINIO_NAME}/#/payment-completed"

                descripcion = request.data.get("descripcion")

                preference_data = {
                    #"notification_url" :  "http://requestbin.fullcontact.com/1ogudgk1",
                    "external_reference" : codigoTransaccion,                        
                    "back_urls": {
                        "success": "https://www.soyyochile.com/#/payment-completed"
                        #"failure": "https://www.tu-sitio/failure",
                        #"pending": "https://www.tu-sitio/pendings"
                    },
                    "items": [{
                        "title": descripcion,
                        "quantity": 1,
                        "currency_id": "CLP",  # Moneda (en este caso, pesos brasileros)
                        "unit_price": monto
                    }]
                }
                if BRASIL_MODE:
                    preference_data = {
                        #"notification_url" :  "http://requestbin.fullcontact.com/1ogudgk1",
                        "external_reference" : codigoTransaccion,
                        "back_urls": {
                            "success": "https://www.soueu.com.br/#/payment-completed"
                            #"failure": "https://www.tu-sitio/failure",
                            #"pending": "https://www.tu-sitio/pendings"
                        },
                        "items": [{
                            "title": descripcion,
                            "quantity": 1,
                            "currency_id": "BRL",  # Moneda (en este caso, pesos brasileros)
                            "unit_price": monto
                        }]
                    }
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response["response"]

                #Crear registro de transaccion
                if "error" not in preference:
                    #data["id_transaccion"] = preference["id"]
                    data["customer_user"] = request.user.id
                    data["discount_id"] = None if cupon==None else cupon.id
                    data["discount_value"] = descuento
                    
                    serializers = Transactionserializers(data=data)
                    if not serializers.is_valid():
                        return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                    utilities = UtilitiesPay()
                    dto = utilities.buid_dto_from_validated_data_transaction(serializers)

                    response = transaction_services.create_transaction(dto)

                    detalles = data.get("detalle", [])
                    for producto in detalles:
                        producto["transaction"] = response.id
                        detalle_serializers = DetalleTransactionserializers(data=producto)
                        if not detalle_serializers.is_valid():
                            return Response({"status": "error", "msg" : "error al serializar detalle del producto", "data": detalle_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                        detalle_dto = utilities.buid_dto_from_validated_data_detalle(detalle_serializers)
                        responseP = transaction_services.create_Detalle_transaction(detalle_dto)

                    sp = preference
                else :
                    sp = preference
                    return Response({"success": False, "data": sp}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"success": True, "data": sp}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({"success": False, "error":str(e)}, status=status.HTTP_503_services_UNAVAILABLE)
