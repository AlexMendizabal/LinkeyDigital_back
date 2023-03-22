from rest_framework import viewsets, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomerUser
from rest_framework import status


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'


class CustomerUserViewSet(APIView):
    def get(self, request):
        if request.user.is_superuser == 1:
            customer_user_list = CustomerUser.objects.all()
            customer_user_serializers = CustomerUserSerializer(customer_user_list, many=True)
            return Response(customer_user_serializers.data, status=status.HTTP_200_OK)
        customer_user = get_object_or_404(CustomerUser, id=request.user.id)
        customer_user_serializer = CustomerUserSerializer(customer_user)
        return Response(customer_user_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser == 0:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomerUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        customer_user = get_object_or_404(CustomerUser, id=request.user.id)
        customer_user_serializers = CustomerUserSerializer(instance=customer_user, data=request.data, partial=True)
        customer_user_serializers.is_valid(raise_exception=True)
        customer_user_serializers.save()
        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        #userProfile = get_object_or_404(CustomerUser, id=request.user.id)
        #userProfile.delete()
        #return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)



