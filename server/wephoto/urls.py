from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import *
from wephoto.views import *


router = routers.DefaultRouter()

router.register(r'uploaded_image', UploadedImageSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]