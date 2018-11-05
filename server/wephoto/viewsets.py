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
    queryset = Review.objects.order_by("-id").all()
    serializer_class = ReviewSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('is_reviewed', 'photographer')


class TagSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("-id").all()
    serializer_class = TagSerializer


class UploadedImageSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.order_by("-id").all()
    serializer_class = UploadedImageSerializer
    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("tag", )


class OrderSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by("-id").all()
    serializer_class = OrderSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('photographer', 'user', 'state')


class OrderDetailSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Order.objects.order_by('-id').all()
    serializer_class = OrderDetailSerializer

    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('photographer', 'user', 'state')

    def get_queryset(self):
        query_set = Order.objects.order_by("-id").all()
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
    queryset = User.objects.order_by("-id").all()
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
        queryset = User.objects.order_by('-id').all()

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
            itags = [int(i) for i in tags.split("-")]
            exclude_phones = []
            for q in queryset:
                t = [i[0] for i in q.tags.values_list()]
                if len(list(set(itags).intersection(set(t)))) ==0:
                    exclude_phones.append(q.phone)
            for p in exclude_phones:
                queryset = queryset.exclude(phone=p)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.query_params.get("user", None)
        states = self.request.query_params.get("states", None)
        if states is not None and user is not None:
            u = User.objects.get(id=user)
            p = User.objects.get(id=instance.id)
            # 找到共同订单
            orders = Order.objects.filter(user=u, photographer=p)
            states_list = [int(i) for i in states.split(",")]
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
    queryset = Moment.objects.order_by("-id").all()


class MomentDetailSet(viewsets.ModelViewSet):
    serializer_class = MomentDetailSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        query_set = Moment.objects.order_by("-id").all()
        user = self.request.query_params.get("user", None)
        if user:
            try:
                u = User.objects.get(id=user)
                for q in query_set:
                    t = ThumbUp.objects.filter(user=u, moment=q)
                    q.is_thumb_up = len(t) == 1
                    q.thumb_id = t[0].id
            except User.DoesNotExist:
                pass
        return query_set


class MomentCommentSet(viewsets.ModelViewSet):
    serializer_class = MomentCommentSerializer
    queryset = MomentComment.objects.order_by("-id").all()


class ThumbUpSet(viewsets.ModelViewSet):
    serializer_class = ThumbUpSerializer
    queryset = ThumbUp.objects.order_by("-id").all()
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('user', 'moment')


class AppConfigSet(viewsets.ModelViewSet):
    serializer_class = AppConfigSerializer
    queryset = AppConfig.objects.order_by('-id').all()
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('in_use', )


class PaymentSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post']
    queryset = Payment.objects.order_by('-id').all()
    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('order', 'state')


class WithdrawSet(viewsets.ModelViewSet):
    serializer_class = WithdrawSerializer
    http_method_names = ['get', 'post']
    queryset = Withdraw.objects.order_by('-id').all()

    filter_backends = (DjangoFilterBackend,)
    # 等值
    filter_fields = ('user', )