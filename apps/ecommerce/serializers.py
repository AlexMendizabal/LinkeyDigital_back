from rest_framework import serializers
from apps.ecommerce.models.button import Button

class Buttonserializers(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ['id', 'customer_user', 'button_title', 'url', 'color', 'enabled']
