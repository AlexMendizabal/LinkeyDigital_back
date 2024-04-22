from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from client_contact.models.client_contact_config import Configuration
from client_contact.serializers import ClientContactConfigurationSerializer

class ConfigurationAPIView(APIView):
    """
    View to list all configurations or create a new one.
    """
    def get(self, request):
        configurations = Configuration.objects.all()
        serializer = ClientContactConfigurationSerializer(configurations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientContactConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, customer_user):
        try:
            return Configuration.objects.get(customer_user=customer_user)
        except Configuration.DoesNotExist:
            raise Http404

    def put(self, request, customer_user):
        configuration = self.get_object(customer_user)
        serializer = ClientContactConfigurationSerializer(configuration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_user):
        configuration = self.get_object(customer_user)
        configuration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
