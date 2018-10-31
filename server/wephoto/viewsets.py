# coding: utf-8

from rest_framework import viewsets, mixins
from rest_framework.pagination import *
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import *
from rest_framework import status
from django.http import Http404

class ReviewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('is_reviewed', 'photographer')


class TagSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UploadedImageSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("tag", )

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('photographer', 'user', 'state')


class OrderDetailSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('photographer', 'user', 'state')

    def get_queryset(self):
        query_set = Order.objects.all()
        states = self.request.query_params.get("states", None)
        print("states", states)
        if states is not None:
            excludes = []
            states_list = [int(i) for i in states.split(",")]
            for o in query_set:
                print(o.state, states_list, o.state not in states_list)
                if o.state not in states_list:

                    excludes.append(o.id)
            print(excludes)
            for id in excludes:
                query_set = query_set.exclude(id=id)
            return query_set
        return super().get_queryset()


class UserSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    # queryset = Photographer.objects.all()
    serializer_class = UserDetailSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('gender', 'pay_way', 'user_type')

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        # 取出所有摄影师，按订单数排序
        queryset = User.objects.order_by('-order_count').all()

        price_min = self.request.query_params.get("price_min", None)
        price_max = self.request.query_params.get("price_max", None)
        photographer = self.request.query_params.get("photographer", None)
        # user = self.request.query_params.get("user", None)
        # states = self.request.query_params.get("states", None)
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

        # if states is not None and user is not None and photographer is not None:
        #     excludes = []
        #     u = User.objects.get(id=user)
        #     p = User.objects.get(id=user)
        #     orders = Order.objects.filter(user=u, photographer=p)
        #     states_list = [int(i) for i in states.split(",")]
        #     from django.db.models import Q
        #     for s in states_list:
        #         orders = orders.filter(~Q(state=s))
        #     print("合格的order", orders)
        #     for q in queryset:
        #         # 如果条件不满足
        #
        #         excludes.append(q.id)
        #
        #     for e in excludes:
        #         queryset = queryset.exclude(e)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print("instance", instance)
        user = self.request.query_params.get("user", None)
        states = self.request.query_params.get("states", None)
        if states is not None and user is not None:
            u = User.objects.get(id=user)
            p = User.objects.get(id=user)
            # 找到共同订单
            orders = Order.objects.filter(user=u, photographer=p)
            print(orders)
            states_list = [int(i) for i in states.split(",")]
            from django.db.models import Q
            has = False
            for o in orders:
                print(o.state, states_list)
                # 只要有一个订单的状态满足
                if o.state in states_list:
                    has = True
                    break
            if not has:
                instance.phone = "支付订金后可查看"
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MomentSet(viewsets.ModelViewSet):
    serializer_class = MomentSerializer
    queryset = Moment.objects.all()


class MomentDetailSet(viewsets.ModelViewSet):
    serializer_class = MomentDetailSerializer
    http_method_names = ["get"]
    queryset = Moment.objects.all()


class MomentCommentSet(viewsets.ModelViewSet):
    serializer_class = MomentCommentSerializer
    queryset = MomentComment.objects.all()
