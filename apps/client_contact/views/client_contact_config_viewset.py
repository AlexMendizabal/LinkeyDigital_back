from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.client_contact.models.client_contact_config import Configuration
from apps.client_contact.serializers import ClientContactConfigurationserializers
from rest_framework.generics import get_object_or_404

class ConfigurationAPIView(APIView):
    """
    View to list all configurations or create a new one.
    """
    def get(self, request):
        configurations = Configuration.objects.all()
        serializers = ClientContactConfigurationserializers(configurations, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = ClientContactConfigurationserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, customer_user):
        return get_object_or_404(Configuration, customer_user=customer_user)

    def put(self, request, customer_user):
        configuration = self.get_object(customer_user)
        serializers = ClientContactConfigurationserializers(configuration, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, customer_user):
        configuration = self.get_object(customer_user)
        configuration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   
