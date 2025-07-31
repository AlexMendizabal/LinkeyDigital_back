from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.mercado_pago.services.mercado_pago import MercadoPagoservices
from apps.pay.services.transactionService import Payservices
import mercadopago


class MercadoPagoWebhook(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        notification_type = request.data.get('type')
        mercadoPagoservices = MercadoPagoservices()
        payservices = Payservices()
        if notification_type:
            if notification_type == 'payment':
                payment_id = request.data.get('data')
                payment_id = payment_id["id"]
                payment = mercadoPagoservices.get_payment(payment_id)
                
                resp = payservices.validar_id_tracaccion(id = None, codigo = payment["external_reference"])
                resp.id_transaccion = payment_id
                resp.save()
                if not resp:
                    return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

                
                estado = 0 
                if not payment["status"] == "approved":
                    estado = 1

                response = payservices.guardar_datos_webHook(estado, resp)

                return Response({"success": True}, status=status.HTTP_200_OK)
            elif notification_type == 'plan':
                plan_id = request.data.get('data[id]')
                #plan = mercadopago.plan.get(plan_id)
                # Aquí puedes realizar acciones con la información del plan
                return Response({'message': 'Plan notification received'}, status=status.HTTP_200_OK)
            elif notification_type == 'subscription':
                subscription_id = request.data.get('data[id]')
                #subscription = mercadopago.subscription.get(subscription_id)
                # Aquí puedes realizar acciones con la información de la suscripción
                return Response({'message': 'Subscription notification received'}, status=status.HTTP_200_OK)
            elif notification_type == 'invoice':
                invoice_id = request.data.get('data[id]')
                #invoice = mercadopago.invoice.get(invoice_id)
                # Aquí puedes realizar acciones con la información de la factura
                return Response({'message': 'Invoice notification received'}, status=status.HTTP_200_OK)
            elif notification_type == 'point_integration_wh':
                # En este caso, simplemente recibimos la notificación sin hacer nada específico
                return Response({'message': 'Point Integration notification received'}, status=status.HTTP_200_OK)
        
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
    

