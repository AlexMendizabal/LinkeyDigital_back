# En tu archivo serializers.py

from rest_framework import serializers
from apps.client_contact.models.client_contact_config import Configuration
from apps.client_contact.models.client_contact import Register

class ClientContactConfigurationserializers(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['customer_user', 'message', 'phone_enabled', 'email_enabled', 'comment_enabled']


class Registerserializers(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'customer_user_id', 'name', 'country_code', 'phone', 'email','status', 'comment', 'created_at']

