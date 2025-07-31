from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.client_contact.models.client_contact import Register
from apps.client_contact.serializers import Registerserializers

class RegisterCreateAPIView(APIView):
    """
    View to create a new register.
    """
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        serializers = Registerserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
