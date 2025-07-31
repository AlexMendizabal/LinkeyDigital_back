from rest_framework import viewsets, generics,status
from apps.pay.serializers import Discountserializers, Userserializers
from apps.pay.models import Discount
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

class DiscountView(viewsets.ModelViewSet):
    serializers_class=Discountserializers
    queryset=Discount.objects.all()

    
    
class GetUserByDiscountView(generics.GenericAPIView):
    serializers_class = Userserializers

    def get(self, request, discount_id):
        try:
            discount = Discount.objects.get(id=discount_id)
            user_info = Userserializers(discount.customer_user).data
            return Response(user_info, status=status.HTTP_200_OK)
        except Discount.DoesNotExist:
            return Response({"error": "Descuento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class UserDiscountsView(generics.GenericAPIView):
    serializers_class = Discountserializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_superuser:
            userID = self.request.GET.get("userID", False) or self.request.user.id
            return Discount.objects.filter(customer_user__id=userID)
        return Discount.objects.filter(customer_user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = self.get_serializers(queryset, many=True)
        return Response(serializers.data)
    
class GetDiscountByVerificationCodeView(APIView):
    serializers_class = Discountserializers  # Use your Discount serializers here
    permission_classes = []
    authentication_classes = []

    def get(self, request, verification_code):
        try:
            discount = Discount.objects.get(verification_code=verification_code)
            discount_info = Discountserializers(discount).data
            return Response(discount_info, status=status.HTTP_200_OK)
        except Discount.DoesNotExist:
            return Response({"error": "Descuento no encontrado"}, status=status.HTTP_404_NOT_FOUND)