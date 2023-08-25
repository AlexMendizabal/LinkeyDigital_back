from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pay.services import PayService, ScrumPay

from pay.utilitiesPay import UtilitiesPay, TransactionSerializer, DetalleTransactionSerializer

from decimal import Decimal

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
            "urlRespuesta",
            "detalle"

        ]
        # Verificar si todos los campos requeridos están presentes
        if not all(field in data for field in required_fields):
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            
            from django.db import transaction

            with transaction.atomic():
                    scrumPay = ScrumPay()
                    transaction_service = PayService()
                    data["monto"] = str(transaction_service.get_price_by_id_producto(data["detalle"]))
                    data["codigoTransaccion"] = scrumPay.generar_codigo_unico()
                    solicitud_pago = scrumPay.solicitudPago(data)
                    
                    if "success" not in solicitud_pago:
                        data["id_transaccion"] = solicitud_pago["id_transaccion"]
                        data["customer_user"] = request.user.id
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
            print(e)
            return Response({"success": False, "error":str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


