from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status

from apps.profile.models import ViewProfile
from apps.profile.services import Viewsservicess


class ViewProfileserializers(serializers.ModelSerializer):
    class Meta:
        model = ViewProfile
        fields = (
            'id', 'custom_user', 'timestamp', 'counter')


class ViewsViewSet(APIView):
    def get(self, request, profile=None, month=None, year=None):
        try:
            if not month or not year or not profile:
                return Response({"succes": False, "data" : "Faltan datos"}, status=status.HTTP_404_NOT_FOUND)
            view_services = Viewsservicess()
            try:
                response = view_services.get_views(profile, month,year)
            except Exception as e:
                print(e)
                return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)

            viewsSerealized = ViewProfileserializers(response, many=True)
            return Response({"success": True, "data": viewsSerealized.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"succes": False}, status=status.HTTP_404_NOT_FOUND)