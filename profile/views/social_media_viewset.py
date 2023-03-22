from rest_framework import serializers, status
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from profile.models import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ('id', 'title', 'url_base', 'image')


class SocialmediaViewSet(APIView):

    def get(self, request, pk=None, format=None):
        if pk:
            socialmedia = get_object_or_404(SocialMedia, id=pk)
            socialmedia_serializers = SocialMediaSerializer(socialmedia)
            return Response(socialmedia_serializers.data, status=status.HTTP_200_OK)
        else:
            socialmedia_list = SocialMedia.objects.all()
            socialmedia_serializers = SocialMediaSerializer(socialmedia_list, many=True)
            return Response(socialmedia_serializers.data, status=status.HTTP_200_OK)
