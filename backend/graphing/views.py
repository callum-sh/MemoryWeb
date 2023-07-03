from django.core.files.storage import default_storage
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .models import MyImageModel  # your image model here


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = MyImageModel  # your image model here
        fields = ['url']  # and other fields of the model if any

    def get_image_url(self, obj):
        return obj.image.url  # change this if your image field has a different name


class ImageViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = MyImageModel.objects.all()  # your image model here
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)
