from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from booking.models import ConfigurationBooking
from booking.serializer import ConfBookingSerializer

class ConfBookingListView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = ConfBookingSerializer

    def get_queryset(self):
        customer_user_id = self.kwargs.get('customer_user_id', None)
        if customer_user_id:
            return ConfigurationBooking.objects.filter(customer_user=customer_user_id)
        return ConfigurationBooking.objects.none()

class ConfBookingCreateView(generics.CreateAPIView):
    serializer_class = ConfBookingSerializer

    def perform_create(self, serializer):
        customer_user_id = self.kwargs.get('customer_user_id', None)
        if customer_user_id:
            serializer.save(customer_user_id=customer_user_id)

class ConfBookingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ConfigurationBooking.objects.all()
    serializer_class = ConfBookingSerializer

class ConfBookingDeleteView(generics.DestroyAPIView):
    queryset = ConfigurationBooking.objects.all()
    serializer_class = ConfBookingSerializer

class ConfBookingRetrieveView(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = ConfigurationBooking.objects.all()
    serializer_class = ConfBookingSerializer
    lookup_field = 'pk'  # Campo utilizado para buscar la configuración de reserva por su ID

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)