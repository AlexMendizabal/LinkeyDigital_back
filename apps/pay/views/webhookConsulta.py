from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from apps.pay.services.transactionService import Payservices

class webhook(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):

        data = request.data
        required_fields = [
            "id_transaccion",
            "fop",
            "numeroTarjeta",
            "FechaExpiracion",
            "codigoAutorizacion",
            "codigoTransaccion",
            "estatus"
        ]
        if not all(field in data for field in required_fields):
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        #Logica para valir datos 

        servicess = Payservices()
        resp = servicess.validar_id_tracaccion(id = data["id_transaccion"], codigo = data["codigoTransaccion"])
        if not resp:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        #Logica para guardar datos

        response = servicess.guardar_datos_webHook(data["estatus"], resp)
        if response is None:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        #response: id_transaccion y fecha actual
        return Response({"id_transaccion": data["id_transaccion"],"fechaConfirmacion": datetime.now() }, status=status.HTTP_200_OK)


