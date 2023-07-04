from rest_framework import serializers

class PhotoSerializer(serializers.Serializer):
    # Define the fields in your photo data
    # Adjust the fields according to the structure of your photo data dictionary
    id = serializers.CharField()
    productUrl = serializers.CharField()
    baseUrl = serializers.CharField()
    mimeType = serializers.CharField()
    mediaMetadata = serializers.DictField()
    filename = serializers.CharField()
