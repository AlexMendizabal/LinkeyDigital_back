from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.client_contact.models.client_contact_config import Configuration
from apps.client_contact.serializers import ClientContactConfigurationserializers
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets

class MultipleConfigurationViewSet(viewsets.ViewSet):
    serializers_class = ClientContactConfigurationserializers

    def list(self, request):
        customer_user_ids = request.data.get('customer_users', [])
        existing_configurations = Configuration.objects.filter(customer_user_id__in=customer_user_ids)
        configurations_data = []
        
        for customer_user_id in customer_user_ids:
            has_configuration = any(config.customer_user_id == customer_user_id for config in existing_configurations)
            configurations_data.append({
                'customer_user_id': customer_user_id,
                'has_configuration': has_configuration
            })

        return Response(configurations_data)

    def create(self, request):
        customer_users = request.data.get('customer_users', [])
        configurations = request.data.get('configurations', {})
        serialized_configurations = []

        for customer_user_id in customer_users:
            existing_config = Configuration.objects.filter(customer_user_id=customer_user_id).first()
            
            if existing_config:
                # Si la configuración existe, actualiza los valores
                serializers = self.serializers_class(existing_config, data=configurations, partial=True)
            else:
                # Si la configuración no existe, crea una nueva configuración
                config_data = {'customer_user': customer_user_id, **configurations}
                serializers = self.serializers_class(data=config_data)
            
            if serializers.is_valid():
                serializers.save()
                serialized_configurations.append(serializers.data)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_configurations, status=status.HTTP_201_CREATED)
