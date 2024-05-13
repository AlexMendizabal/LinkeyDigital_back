from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pay.utilitiesPay import TransactionSerializerForAll
from pay.models import Transaction
from pay.serializer import AllTransactionSerializer
class AllTransactionsView(APIView):
    def get(self, request):
        try:
            status_param = request.query_params.get('status')
            if status_param is not None:
                # Filtrar las transacciones por estado
                transactions = Transaction.objects.filter(status=status_param)
            else:
                # Obtener todas las transacciones si no se proporciona el parámetro de estado
                transactions = Transaction.objects.all()
            # Serializar los datos de las transacciones personalizando los campos
            transaction_serializer = AllTransactionSerializer(transactions, many=True)
            # Devolver la respuesta con los datos serializados
            return Response({"success": True, "data": transaction_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # En caso de error, devolver una respuesta de error
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)