from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.profile.models import DesignProfile


class DesignProfileserializers(serializers.ModelSerializer):
    class Meta:
        model = DesignProfile
        fields = ('id','code')


class DesignProfileViewSet(APIView):

    def get(self, request, pk=None, format=None):
        if pk:
            design_profile = get_object_or_404(DesignProfile, id=pk)
            design_profile_serializers = DesignProfileserializers(design_profile)
            return Response(design_profile_serializers.data, status=status.HTTP_200_OK)
        else:
            design_profile_list = DesignProfile.objects.all()
            design_profile_serializers = DesignProfileserializers(design_profile_list, many=True)
            return Response(design_profile_serializers.data, status=status.HTTP_200_OK)

