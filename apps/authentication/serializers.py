from rest_framework import serializers
from apps.authentication.models import CustomerUser

class CustomerUserserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'
