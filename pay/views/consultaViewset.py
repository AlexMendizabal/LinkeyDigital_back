from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from administration.UtilitiesAdministration import UtilitiesAdm
from rest_framework.generics import get_object_or_404

from pay.models import Transaction, TransactionDto
from pay.services import ReservaService, ScrumPay

from pay.utilitiesPay import UtilitiesPay, TransactionSerializerForGet

class ConsultaViewSet(APIView):
    def get(self, request):

        utilitiesAdm = UtilitiesAdm()

        user_id = request.GET.get('user_id', request.user.id)
        user_id = int(user_id)
        if not utilitiesAdm.hasPermision(request.user, user_id ):
            print(request.user, user_id )
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.GET.get('user_id', request.user.id)

        transaction_service = ReservaService()
        try:
            response = transaction_service.get_transactions(user_id)
        except Exception as e:
            print(str(e))
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        transaction_serializer = TransactionSerializerForGet(response, many=True)
        return Response({"success": True, "data": transaction_serializer.data}, status=status.HTTP_200_OK)


        
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
                if solicitud_pago["estatus"] == "0":
                    transaction.status = 2
                    transaction.save()
                transaction_serializer = TransactionSerializerForGet(transaction, many=False)
                return Response({"success": True, "data": transaction_serializer.data, "respuesta" : solicitud_pago  }, status=status.HTTP_200_OK)
            else:
                return Response(solicitud_pago, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(e)
            return {"success": False, "error": str(e)}

    

