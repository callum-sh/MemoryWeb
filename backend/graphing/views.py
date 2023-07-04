from django.core.files.storage import default_storage
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .models import MyImageModel  # your image model here

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PhotoSerializer

from .utils import get_all_photos, service_account_login
from django.conf import settings



class PhotoView(APIView):
    def get(self, request):
        # Call the get_all_photos function to obtain the list of photos
        creds = service_account_login()
        photos = get_all_photos(creds)  # Make sure to pass the appropriate creds object

        # Serialize the list of photos
        serializer = PhotoSerializer(photos, many=True)

        # Return the serialized photos as the API response
        return Response(serializer.data, status=status.HTTP_200_OK)


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
