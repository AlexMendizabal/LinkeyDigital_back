from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.booking.models import ConfigurationBooking
from apps.booking.serializers import ConfBookingserializers

class ConfBookingListView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializers_class = ConfBookingserializers

    def get_queryset(self):
        customer_user_id = self.kwargs.get('customer_user_id', None)
        if customer_user_id:
            return ConfigurationBooking.objects.filter(customer_user=customer_user_id)
        return ConfigurationBooking.objects.none()

class ConfBookingCreateView(generics.CreateAPIView):
    serializers_class = ConfBookingserializers

    def perform_create(self, serializers):
        customer_user_id = self.kwargs.get('customer_user_id', None)
        if customer_user_id:
            serializers.save(customer_user_id=customer_user_id)

class ConfBookingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ConfigurationBooking.objects.all()
    serializers_class = ConfBookingserializers

class ConfBookingDeleteView(generics.DestroyAPIView):
    queryset = ConfigurationBooking.objects.all()
    serializers_class = ConfBookingserializers

class ConfBookingRetrieveView(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = ConfigurationBooking.objects.all()
    serializers_class = ConfBookingserializers
    lookup_field = 'pk'  # Campo utilizado para buscar la configuración de reserva por su ID

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializers(instance)
        return Response(serializers.data)