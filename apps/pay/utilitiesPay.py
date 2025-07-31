from .models import Transaction, TransactionDto, DetalleTransaction, DetalleTransactionDto, Discount
from rest_framework import viewsets, serializers

class Transactionserializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'customer_user',  'status', 'date',
            'canal', 'monto', 'moneda', 'descripcion', 'nombreComprador',
            'apellidoComprador', 'documentoComprador', 'modalidad',
            'extra1','extra2','extra3', 'direccionComprador',
            'ciudad','codigoTransaccion', 'urlRespuesta',
            'discount_value', 'discount_id',
            'id_transaccion','correo', 'telefono')
        extra_kwargs = {'customer_user': {'required': True}, 
                         'monto' :{'required': True} }
        
class TransactionserializersForGet(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id', 'status')
        
class TransactionserializersForAll(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')
        
class DetalleTransactionserializersForAll(serializers.ModelSerializer):
    class Meta:
        model = DetalleTransaction
        fields = ('__all__')

class DetalleTransactionserializers(serializers.ModelSerializer):
    class Meta:
        model = DetalleTransaction
        fields = ('id','producto',  'transaction', 'cantidad' )
        
class UtilitiesPay():
    def buid_dto_from_validated_data_transaction(self, serializers):
        data = serializers.validated_data
        return TransactionDto(
            customer_user=data["customer_user"],
            status=data.get("status", 1),
            canal =data["canal"],
            monto =data["monto"],
            moneda =data["moneda"],
            descripcion =data.get("descripcion", None),
            nombreComprador =data["nombreComprador"],
            apellidoComprador=data["apellidoComprador"],
            documentoComprador =data.get("documentoComprador", None),
            modalidad =data["modalidad"],
            extra1 =data.get("extra1", None),
            extra2 =data.get("extra2", None),
            extra3 =data.get("extra3", None),
            direccionComprador =data["direccionComprador"],
            ciudad =data.get("ciudad", None),
            codigoTransaccion=data["codigoTransaccion"],
            urlRespuesta =data["urlRespuesta"],
            id_transaccion  =data.get("id_transaccion", None),
            correo =data["correo"],
            telefono =data.get("telefono", None),
            discount_id=data.get("discount_id", None),
            discount_value = data.get("discount_value", None),
        )
    
    def buid_dto_from_validated_data_detalle(self, serializers):
        data = serializers.validated_data
        return DetalleTransaction(
            producto=data["producto"],
            transaction =data["transaction"],
            cantidad =data["cantidad"]
        )
    
    def apply_discount(request,id_transaccion, verification_code):
        transaccion = Transaction.objects.get(id=id_transaccion)
        discount = Discount.objects.get(verification_code)

        transaccion.discount=discount
        transaccion.save()

        