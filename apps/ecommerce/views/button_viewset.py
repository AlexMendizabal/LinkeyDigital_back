from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.ecommerce.models.button import Button
from apps.ecommerce.serializers import Buttonserializers

class ButtonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Button.objects.all()
    serializers_class = Buttonserializers

    def post(self, request, *args, **kwargs):
        # Obtener los datos de la solicitud
        data = request.data
        customer_user_id = data.get('customer_user')

        # Verificar si ya existe un botón para este cliente
        existing_button = Button.objects.filter(customer_user=customer_user_id).first()

        if existing_button:
            # Si ya existe un botón, actualizarlo en lugar de crear uno nuevo
            serializers = self.get_serializers(existing_button, data=data, partial=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            # Si no existe un botón, crear uno nuevo
            serializers = self.get_serializers(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)


class ButtonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Button.objects.all()
    serializers_class = Buttonserializers
