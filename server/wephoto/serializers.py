from rest_framework import serializers
from wephoto.models import *


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('id', 'file')

