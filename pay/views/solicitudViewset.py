from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pay.services import PayService, ScrumPay

from pay.models.transaction import Discount

from pay.utilitiesPay import UtilitiesPay, TransactionSerializer, DetalleTransactionSerializer

from django.db import transaction
from django.shortcuts import get_object_or_404

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
                transaction_service = PayService()

                monto_pedido = float(transaction_service.get_price_by_id_producto(data["detalle"]))

                ciudad = data.get("ciudad", "")
                costo_envio = transaction_service.get_precio_envio(ciudad)

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

                data["monto"] = str(monto_pedido - descuento + costo_envio)
                data["codigoTransaccion"] = transaction_service.generar_codigo_unico()
                data["urlRespuesta"] = "https://www.soyyo.digital/#/payment-completed"

                solicitud_pago = scrumPay.solicitudPago(data)
                
                if "success" not in solicitud_pago:
                    data["id_transaccion"] = solicitud_pago["id_transaccion"]
                    data["customer_user"] = request.user.id
                    data["discount_id"] = None if cupon==None else cupon.id
                    data["discount_value"] = round( descuento, 2)
                    
                    serializer = TransactionSerializer(data=data)
                    if not serializer.is_valid():
                        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    utilities = UtilitiesPay()
                    dto = utilities.buid_dto_from_validated_data_transaction(serializer)

                    response = transaction_service.create_transaction(dto)

                    detalles = data.get("detalle", [])
                    for producto in detalles:
                        producto["transaction"] = response.id
                        detalle_serializer = DetalleTransactionSerializer(data=producto)
                        if not detalle_serializer.is_valid():
                            return Response({"status": "error", "data": detalle_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                        detalle_dto = utilities.buid_dto_from_validated_data_detalle(detalle_serializer)
                        responseP = transaction_service.create_Detalle_transaction(detalle_dto)

                else:
                    return Response({"success": False, "error": solicitud_pago.get("error")}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

                sp = {
                    "error": solicitud_pago.get("error"),
                    "solicitud_pago": solicitud_pago.get("url"),
                    "id": response.id
                }
                return Response({"success": True, "data": sp}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error":str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


