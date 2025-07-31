from rest_framework.views import APIView
from rest_framework.response import Response
from apps.client_contact.models.client_contact_config import Configuration
from apps.client_contact.serializers import ClientContactConfigurationserializers
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
        serializers = ClientContactConfigurationserializers(configuration)
        return Response(serializers.data)
