from rest_framework import generics
from apps.client_contact.models.client_contact import Register
from apps.client_contact.serializers import Registerserializers

class RegisterListCreateAPIView(generics.ListCreateAPIView):
    """
    View to list all registers or create a new one.
    """
    serializers_class = Registerserializers

    def get_queryset(self):
        # Obtener el ID del usuario cliente de los parámetros de la URL
        customer_user_id = self.kwargs['customer_user_id']
        # Filtrar los registros por el usuario cliente específico
        return Register.objects.filter(customer_user_id=customer_user_id)

class RegisterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a register by its id.
    """
    queryset = Register.objects.all()
    serializers_class = Registerserializers
