from rest_framework import serializers
from wephoto.models import *


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('id', 'file', 'tag')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'content', 'count')


class UserSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)

    password = serializers.CharField(write_only=True)  # 不可查看

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'password', 'gender', "avatar", "qq", "wechat", "money", "in_order_money",
                  "is_reviewed", "tags", "desc", "home_img", "pay_way", "price", "visit", "album")


class ReviewSerializer(serializers.ModelSerializer):
    # photographer = PhotographerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'photographer', 'id_card_1', 'id_card_2', 'device_1', 'device_2', 'device_3', 'is_reviewed', 'comment')


class OrderSerializer(serializers.ModelSerializer):
    # photographer = PhotographerSerializer(read_only=True)
    # model_user = CommonUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'photographer', 'model_user', 'type', 'price', 'place', 'place_type', 'year', 'month', 'day')