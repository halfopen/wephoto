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
        queryset = User.objects.order_by('-order_count').all()

        price_min = self.request.query_params.get("price_min", None)
        price_max = self.request.query_params.get("price_max", None)
        tags = self.request.query_params.get("tags", None)

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)

        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)

        if tags is not None:
            print(tags, type(tags))
            itags = [int(i) for i in tags.split("-")]
            exclude_phones = []
            for q in queryset:
                print()
                t = [i[0] for i in q.tags.values_list()]
                print(itags, t)
                if len(list(set(itags).intersection(set(t)))) ==0:
                    exclude_phones.append(q.phone)
            print(exclude_phones)
            for p in exclude_phones:
                queryset = queryset.exclude(phone=p)
        return queryset

