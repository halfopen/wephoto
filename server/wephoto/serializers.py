from rest_framework import serializers
from wephoto.models import *


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)

    password = serializers.CharField(write_only=True)  # 不可查看
    # token = serializers.CharField(read_only=True)  # 不可查看
    is_reviewed = serializers.IntegerField(read_only=True) # 没有权限修改
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('token', )


class UserDetailSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(write_only=True)  # 不可查看
    # password = serializers.CharField(write_only=True)  # 不可查看
    is_reviewed = serializers.IntegerField(read_only=True) # 没有权限修改

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('token', 'password')
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    # photographer = PhotographerSerializer(read_only=True)

    is_reviewed = serializers.IntegerField(read_only=True)
    comment = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # photographer = PhotographerSerializer(read_only=True)
    # model_user = CommonUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class MomentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moment
        fields = '__all__'


class MomentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moment
        fields = '__all__'
        depth = 1


class MomentCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MomentComment
        fields = '__all__'

