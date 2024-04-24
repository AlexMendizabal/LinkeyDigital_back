from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from client_contact.models.client_contact import Register
from client_contact.serializers import RegisterSerializer

class RegisterCreateAPIView(APIView):
    """
    View to create a new register.
    """
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
