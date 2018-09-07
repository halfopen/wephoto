from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import *
from .models import *
from .serializers import *


class UploadedImageSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer