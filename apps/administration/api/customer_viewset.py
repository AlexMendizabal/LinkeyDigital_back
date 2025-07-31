from rest_framework import viewsets, serializers
from administration.models import Customer



class Customerserializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializers_class = Customerserializers