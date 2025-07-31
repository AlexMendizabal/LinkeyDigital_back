from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.pay.services.transactionService import Payservices
from apps.pay.services.scrumPay import ScrumPay

from apps.pay.models.transaction import Discount

from apps.pay.utilitiesPay import UtilitiesPay, Transactionserializers, DetalleTransactionserializers

from django.db import transaction
from django.shortcuts import get_object_or_404

from conf_fire_base import DOMINIO_NAME

class SolicitudViewSet(APIView):

    

    def post(self, request):
        
        data = request.data
        # Lista de campos requeridos
        required_fields = [
            "canal",
            "moneda",
            "descripcion",
            "nombreComprador",
            "apellidoComprador",
            "correo",
            "telefono",
            "modalidad",
            "direccionComprador",
            "ciudad",
            "detalle"

        ]
        # Verificar si todos los campos requeridos están presentes
        if not all(field in data for field in required_fields):
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                scrumPay = ScrumPay()
                transaction_services = Payservices()

                monto_pedido = float(transaction_services.get_price_by_id_producto(data["detalle"]))

                ciudad = data.get("ciudad", "")
                costo_envio = transaction_services.get_precio_envio(ciudad)

                descuento = 0
                verification_code = data.get("verificationCode", False)
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

                data["monto"] = str(round(monto_pedido - descuento + costo_envio, 2))
                data["codigoTransaccion"] = transaction_services.generar_codigo_unico()
                data["urlRespuesta"] = f"https://www.{DOMINIO_NAME}/#/payment-completed"

                solicitud_pago = scrumPay.solicitudPago(data)
                
                if "success" not in solicitud_pago:
                    data["id_transaccion"] = solicitud_pago["id_transaccion"]
                    data["customer_user"] = request.user.id
                    data["discount_id"] = None if cupon==None else cupon.id
                    data["discount_value"] = round( descuento, 2)
                    
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
                            return Response({"status": "error", "data": detalle_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                        detalle_dto = utilities.buid_dto_from_validated_data_detalle(detalle_serializers)
                        responseP = transaction_services.create_Detalle_transaction(detalle_dto)

                else:
                    return Response({"success": False, "error": solicitud_pago.get("error")}, status=status.HTTP_503_services_UNAVAILABLE)

                sp = {
                    "error": solicitud_pago.get("error"),
                    "solicitud_pago": solicitud_pago.get("url"),
                    "id": response.id
                }
                return Response({"success": True, "data": sp}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error":str(e)}, status=status.HTTP_503_services_UNAVAILABLE)


