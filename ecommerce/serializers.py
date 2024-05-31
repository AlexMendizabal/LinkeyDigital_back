from rest_framework import serializers
from ecommerce.models.button import Button

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ['id', 'customer_user', 'button_title', 'url', 'enabled']
