from rest_framework import generics
from ecommerce.models.button import Button
from ecommerce.serializers import ButtonSerializer

class ButtonListByCustomerUserAPIView(generics.ListAPIView):
    serializer_class = ButtonSerializer

    permission_classes = []
    authentication_classes = []
    def get_queryset(self):
        customer_user_id = self.kwargs.get('customer_user_id')
        return Button.objects.filter(customer_user_id=customer_user_id)
