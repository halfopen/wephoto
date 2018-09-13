from rest_framework import viewsets, mixins
from rest_framework.pagination import *
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import *


class ReviewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('tag',)


class TagSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UploadedImageSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer


class OrderSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserSet(viewsets.ModelViewSet):
    # queryset = Photographer.objects.all()
    serializer_class = UserSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('gender', 'pay_way')

    def get_queryset(self):
        queryset = User.objects.all()

        price_min = self.request.query_params.get("price_min", None)
        price_max = self.request.query_params.get("price_max", None)

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)

        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

