from rest_framework.views import APIView
from rest_framework.response import Response
from client_contact.models.client_contact_config import Configuration
from client_contact.serializers import ClientContactConfigurationSerializer
from django.http import Http404

class ConfigurationDetail(APIView):
    """
    View to retrieve a configuration by customer_user.
    """
    permission_classes = []
    authentication_classes = []
    def get_object(self, customer_user):
        try:
            return Configuration.objects.get(customer_user=customer_user)
        except Configuration.DoesNotExist:
            raise Http404

    def get(self, request, customer_user):
        configuration = self.get_object(customer_user)
        serializer = ClientContactConfigurationSerializer(configuration)
        return Response(serializer.data)
