from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import *
from wephoto.views import *


router = routers.DefaultRouter()

router.register(r'uploaded_image', UploadedImageSet)
router.register(r'user', UserSet)
router.register(r'tag', TagSet)
router.register(r'review', ReviewSet)
router.register(r'order', OrderSet)
router.register(r'moment', MomentSet)

router.register(r'moment_comment', MomentCommentSet)
router.register(r'thumbup', ThumbUpSet)
router.register(r'app_config', AppConfigSet)
router.register(r'payment', PaymentSet)
router.register(r'withdraw', WithdrawSet)
router.register(r'accusement', AccusementSet)

router.register(r'moment_detail', MomentDetailSet, base_name='moment_detail')
router.register(r'user_detail', UserDetailSet, base_name='user_detail')
router.register(r'order_detail', OrderDetailSet, base_name='order_detail')

urlpatterns = [
    url(r'^', include(router.urls)),
]