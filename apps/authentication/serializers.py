from rest_framework import serializers
from apps.authentication.models import CustomerUser

class CustomerUserserializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = CustomerUser
        fields = ['id', 'pk', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'is_superuser', 'is_admin', 'is_sales_manager', 'is_booking', 'is_ecommerce']
