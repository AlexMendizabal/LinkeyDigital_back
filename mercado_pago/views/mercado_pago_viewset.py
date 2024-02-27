from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from soyyo_api.settings import MERCADOPAGO_SECRET_KEY, MERCADOPAGO_PUBLIC_KEY
import mercadopago

class MercadoPago(APIView):
    def post(self, request):
        try:
            sdk = mercadopago.SDK(MERCADOPAGO_SECRET_KEY)
            
            # Obtener datos del formulario de pago
            monto = request.data.get("monto")
            descripcion = request.data.get("descripcion")
            
            # Validar datos
            if not monto or not descripcion:
                return Response({"error": "Datos de pago incompletos"}, status=status.HTTP_400_BAD_REQUEST)

            # Crear preferencia de pago
            preference_data = {
                "items": [{
                    "title": descripcion,
                    "quantity": 1,
                    "currency_id": "BRL",  # Moneda (en este caso, pesos argentinos)
                    "unit_price": float(monto)
                }]
            }
            
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            
            return Response({"success": preference}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
