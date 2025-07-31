from rest_framework import generics
from apps.ecommerce.models.button import Button
from apps.ecommerce.serializers import Buttonserializers

class ButtonListByCustomerUserAPIView(generics.ListAPIView):
    serializers_class = Buttonserializers

    permission_classes = []
    authentication_classes = []
    def get_queryset(self):
        customer_user_id = self.kwargs.get('customer_user_id')
        return Button.objects.filter(customer_user_id=customer_user_id)
