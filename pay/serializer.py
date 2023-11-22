from rest_framework import serializers
from pay.models.transaction import Discount
from authentication.models.customer_user import CustomerUser

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Discount
        #fields=('id', 'customer_user', 'verification_code', 'social_media', 'initial_date', 'final_date', 'discount_type', 'discount_rate', 'status')

        fields='__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'