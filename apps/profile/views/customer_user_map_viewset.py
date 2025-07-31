from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from apps.profile.models import CustomerUserMap, MapDto
from apps.profile.services import Contactservices


class CustomerUserMapserializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserMap
        fields = (
           'customer_user', 'longitude', 'latitude', 'image', 'is_active', 'is_visible')
        extra_kwargs = {'longitude': {'required': True}, 'latitude': {'required': True},
                        'is_visible': {'required': True}}


class CustomerUserMapViewSet(APIView):
    def get(self, request, pk=None):
        contact_services = Contactservices()
        try:
            response = contact_services.get_map(pk, request.user.id)
        except Exception as e:
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

        customer_map_serializers = CustomerUserMapserializers(response, many=False)
        return Response({"success": True, "data": customer_map_serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer_user"] = request.user.id
        serializers = CustomerUserMapserializers(data=request.data)

        if not serializers.is_valid():
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

        if 'image' in request.data:
            try:
                request.data.pop('image')
            except Exception as e:
                pass

        dto = self.buid_dto_from_validated_data(serializers)
        contact_services = Contactservices()

        try:
            response = contact_services.create_or_update_map(dto)
        except Exception as e:
            return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        customer_map_serializers = CustomerUserMapserializers(response, many=False)
        return Response({"success": True, "data": customer_map_serializers.data}, status=status.HTTP_200_OK)


    def buid_dto_from_validated_data(self, serializers):
        data = serializers.validated_data
        return MapDto(
            customer_user=data["customer_user"],
            longitude=data["longitude"],
            latitude=data["latitude"],
            is_active=True,
            is_visible=data["is_visible"],
        )
