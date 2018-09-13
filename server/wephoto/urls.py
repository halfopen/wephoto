from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import *
from wephoto.views import *


router = routers.DefaultRouter()

router.register(r'uploaded_image', UploadedImageSet)
router.register(r'user', UserSet, base_name='user')
router.register(r'tag', TagSet)
router.register(r'review', ReviewSet)
router.register(r'order', OrderSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]