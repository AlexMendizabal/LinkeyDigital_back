# En tu archivo views.py
from rest_framework import generics
from apps.pay.models import Productos
from apps.pay.serializers import Productsserializers

class ProductosListCreateView(generics.ListCreateAPIView):
    queryset = Productos.objects.all()
    serializers_class = Productsserializers
    
class ProductosRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Productos.objects.all()
    serializers_class = Productsserializers

class ProductosListView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []

    queryset = Productos.objects.all()
    serializers_class = Productsserializers

