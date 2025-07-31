from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from apps.administration.UtilitiesAdministration import UtilitiesAdm
from rest_framework.generics import get_object_or_404

from apps.pay.models import Transaction, TransactionDto
from apps.pay.services.transactionService import Payservices
from apps.pay.services.scrumPay import ScrumPay

from apps.pay.utilitiesPay import UtilitiesPay, TransactionserializersForGet, TransactionserializersForAll \
    ,DetalleTransactionserializersForAll

class ConsultaViewSet(APIView):

    def convert_detalles_to_serializers(self,detalle,trans):
        transaction_services = Payservices()
        detalle = transaction_services.get_detalle_transaccion(trans["id"])
        detalle_serializers = DetalleTransactionserializersForAll(detalle, many=True)
        trans["Detalle"] = detalle_serializers.data
        return trans

    def get(self, request):

        utilitiesAdm = UtilitiesAdm()

        user_id = request.GET.get('user_id', request.user.id)
        user_id = int(user_id)
        if not utilitiesAdm.hasPermision(request.user, user_id ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.GET.get('user_id', request.user.id)

        transaction_services = Payservices()
        try:
            response = transaction_services.get_transactions(user_id)
            transaction_serializers = TransactionserializersForAll(response, many=True)
            
            data = []
            if isinstance(transaction_serializers.data, list):
                # Si es una colección de objetos
                for trans in transaction_serializers.data:
                    data.append(self.convert_detalles_to_serializers(trans["id"],trans))
            else:
                    trans = transaction_serializers.data
                    data.append(self.convert_detalles_to_serializers(trans["id"],trans))
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


        
class ConsultaExtendViewSet(APIView):
    def get(self, request, pk=None):
        if not pk:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction = get_object_or_404(Transaction, id=pk)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, transaction.customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        try:

            scrumPay = ScrumPay()
            solicitud_pago = scrumPay.consultaDePago(transaction.id_transaccion)
            
            if not "success" in solicitud_pago:
                if solicitud_pago["estatus"] == "0" and transaction.status == 1:
                    transaction.status = 2
                    transaction.save()
                transaction_serializers = TransactionserializersForGet(transaction, many=False)
                return Response({"success": True, "data": transaction_serializers.data, "respuesta" : {"estatus":solicitud_pago["estatus"], "error": solicitud_pago["error"]}  }, status=status.HTTP_200_OK)
            else:
                return Response(solicitud_pago, status=status.HTTP_503_services_UNAVAILABLE)
        except Exception as e:
            return {"success": False, "error": str(e)}
    # maybe deberia verificar que este pagado primero idk
    def put(self, request, pk=None):
        estatus = 3

        if not pk or not estatus: 
            return Response({"success": False, "error" : "falta pk"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_superuser: 
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        try: 
            transaction = get_object_or_404(Transaction, id=pk)
            transaction.status = estatus
            transaction.save()
            transaction_serializers = TransactionserializersForGet(transaction, many=False)
        except Exception as e:
            return {"success": False, "error": str(e)}
        return Response({"success": True, "data": transaction_serializers.data }, status=status.HTTP_200_OK)
        

        
        
        

