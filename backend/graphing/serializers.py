from rest_framework import serializers

class PhotoSerializer(serializers.Serializer):

    id = serializers.CharField()
    productUrl = serializers.CharField()
    baseUrl = serializers.CharField()
    mimeType = serializers.CharField()
    mediaMetadata = serializers.DictField()
    filename = serializers.CharField()
