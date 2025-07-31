from rest_framework import serializers
from apps.pay.models.transaction import Discount, Productos, Transaction
from apps.authentication.models.customer_user import CustomerUser

class Discountserializers(serializers.ModelSerializer):
    class Meta:
        model=Discount
        fields='__all__'
        
class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class Productsserializers(serializers.ModelSerializer):
    class Meta:
        model=Productos
        fields='__all__'

class AllTransactionserializers(serializers.ModelSerializer):
    # Agregar campos para el cliente y el vendedor
    customer_user_email = serializers.SerializerMethodField()
    customer_user_phone_number = serializers.SerializerMethodField()
    vendedor = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'id_transaccion',
            'date',
            'status',
            'canal',
            'monto',
            'moneda',
            'descripcion',
            'nombreComprador',
            'apellidoComprador',
            'documentoComprador',
            'modalidad',
            'direccionComprador',
            'ciudad',
            'codigoTransaccion',
            'correo',
            'telefono',
            'customer_user_email',
            'customer_user_phone_number',
            'discount_value',
            'vendedor',
        ]

    def get_customer_user_email(self, obj):
        # Obtener el correo electrónico del cliente
        if obj.customer_user_id:
            customer_user = CustomerUser.objects.get(id=obj.customer_user_id)
            return customer_user.email
        return None

    def get_customer_user_phone_number(self, obj):
        # Obtener el número de teléfono del cliente
        if obj.customer_user_id:
            customer_user = CustomerUser.objects.get(id=obj.customer_user_id)
            return customer_user.phone_number
        return None

    def get_vendedor(self, obj):
        # Obtener el nombre del cliente asociado al vendedor
        if obj.discount_id_id:
            discount = Discount.objects.get(id=obj.discount_id_id)
            return discount.customer_user.username
        return None