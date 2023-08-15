from rest_framework.generics import get_object_or_404

from pay.models import Transaction, DetalleTransaction

class ReservaService:
    
    def get_transactions(self, customer_user=None):
        if customer_user:
            transaction = Transaction.objects.filter(customer_user = customer_user).order_by('id')
        else:
            return None
        return transaction
    def create_transaction(self, dto):
        transaction = Transaction.objects.create(
            customer_user=dto.customer_user,
            status=dto.status,
            canal =dto.canal,
            monto =dto.monto,
            moneda =dto.moneda,
            descripcion =dto.descripcion,
            nombreComprador =dto.nombreComprador,
            apellidoComprador=dto.apellidoComprador,
            documentoComprador =dto.documentoComprador,
            modalidad =dto.modalidad,
            extra1 =dto.extra1,
            extra2 =dto.extra2,
            extra3 =dto.extra3,
            direccionComprador =dto.direccionComprador,
            ciudad =dto.ciudad,
            codigoTransaccion=dto.codigoTransaccion,
            urlRespuesta =dto.urlRespuesta,
            id_transaccion =dto.id_transaccion,
        ) 
        return transaction
    
    def create_Detalle_transaction(self, dto):
        transaction = DetalleTransaction.objects.create(
            producto=dto.producto,
            transaction=dto.transaction,
            cantidad=dto.cantidad,
        ) 
        return transaction
