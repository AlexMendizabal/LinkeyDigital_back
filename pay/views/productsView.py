# En tu archivo views.py
from rest_framework import generics
from pay.models import Productos
from pay.serializer import ProductsSerializer

class ProductosListCreateView(generics.ListCreateAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductsSerializer

class ProductosRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductsSerializer
