# coding=utf-8
from django.db import models
# from django.utils.safestring import mark_safe
from .storage import *
import django.utils.timezone as timezone
from django.http import *
from django.db import transaction
import traceback
import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class DataCheckError(Exception):
    pass


class UploadedImage(models.Model):
    file = models.CharField(max_length=2048, verbose_name="地址")
    tag = models.CharField(max_length=1024, default="", db_index=True)

    def image(self):
        return '<img style="width:200px; height:200px" src="%s"/>' % self.file

    image.allow_tags = True

    class Meta:
        verbose_name = u"4.上传的图片"

    def __str__(self):
        return self.file + " " + self.tag


class Tag(models.Model):
    """

    """
    content = models.CharField(max_length=48, unique=True, verbose_name=u"标签名")
    count = models.IntegerField(default=0, verbose_name=u"使用次数")

    class Meta:
        verbose_name = u"5.标签"

    def __str__(self):
        return self.content


class User(models.Model):
    """
        用户类
    """
    phone = models.CharField(max_length=32, null=False, unique=True, verbose_name=u"手机")
    password = models.CharField(max_length=1024, verbose_name=u"密码", null=False, blank=False)
    name = models.CharField(verbose_name=u"姓名", max_length=1024, null=False, blank=False)
    gender = models.IntegerField(default=0, choices=((0, u"男"), (1, u"女")), verbose_name=u"性别", blank=True, null=True)

    avatar = models.CharField(max_length=2048, blank=True, verbose_name=u"头像", default=u"", null=True)
    token = models.CharField(max_length=4096, default="_", blank=True, null=True, verbose_name=u"令牌")

    qq = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"QQ号", default=u"")
    wechat = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"微信号", default=u"")

    money = models.FloatField(default=0.0, verbose_name=u"余额", blank=True)
    in_order_money = models.FloatField(default=0.0, verbose_name=u"冻结金额", blank=True)
    bank = models.CharField(max_length=48, verbose_name=u"开户银行", blank=True, default="")
    bank_card = models.CharField(max_length=1024, verbose_name=u"银行卡", blank=True)

    address = models.CharField(default="", max_length=1024, verbose_name=u"所在地区", null=True, blank=True)
    # 以下为摄影师字段
    order_count = models.IntegerField(verbose_name=u"已完成订单数", default=0, blank=True)
    user_type = models.BooleanField(verbose_name=u"是否为摄影师", choices=((False, u"普通用户"), (True, u"摄影师")), default=False, blank=True)
    is_reviewed = models.IntegerField(default=0, verbose_name=u"是否审核通过",
                                      choices=((0, u"未提交"), (1, u"审核中"), (2, u"审核通过"), (-1, u"审核未通过")), blank=True)
    tags = models.ManyToManyField(Tag, blank=True,  verbose_name=u"用户标签", default=None)
    desc = models.CharField(max_length=4096, verbose_name=u"个人签名", null=True, blank=True, default=u"")
    home_img = models.CharField(max_length=2048, verbose_name=u"主页图片",  blank=True)
    pay_way = models.IntegerField(default=0, verbose_name=u"收费方式", choices=((0, u"互免"), (1, u"收费")), null=False, blank=True)
    price = models.FloatField(default=0.0, verbose_name=u"价格", blank=True)
    visit = models.IntegerField(default=0, verbose_name=u"访问量", blank=True)

    likes = models.ManyToManyField("self", verbose_name=u"收藏", blank=True)  # 普通用户才能收藏
    available_date = models.TextField(verbose_name=u"可预约时间", blank=True, default="", null=True)

    class Meta:
        verbose_name = u"6.用户"

    def avatar_image(self):
        return u'<img style="width:60px; height:60px" src="%s"/>' % self.avatar

    avatar_image.allow_tags = True
    avatar_image.verbose_name = u"头像"

    def __str__(self):
        return self.phone


class Review(models.Model):
    """
        审核记录
    """
    photographer = models.OneToOneField(User)
    name = models.CharField(verbose_name=u"姓名", max_length=1024, null=False, blank=False, default="")
    gender = models.IntegerField(default=0, choices=((0, u"男"), (1, u"女")), verbose_name=u"性别", blank=True, null=True)
    birthday = models.DateField(verbose_name=u"出生年月日",  blank=True,  default=u"1995-01-01", null=True)
    id_card_num = models.CharField(verbose_name=u"身份证号码", blank=True, null=True, default=u"000000000000000000", max_length=18)

    id_card_1 = models.CharField(verbose_name=u"正面身份证", max_length=2048, blank=True, null=True)
    id_card_2 = models.CharField(verbose_name=u"反面身份证", max_length=2048, blank=True, null=True)
    device_1 = models.CharField(verbose_name=u"使用设备－前面", max_length=2048, null=True, blank=True)
    device_2 = models.CharField(verbose_name=u"使用设备－后面", max_length=2048, null=True, blank=True)
    device_3 = models.CharField(verbose_name=u"使用设备－侧面", max_length=2048, null=True, blank=True)

    is_reviewed = models.IntegerField(default=0, verbose_name=u"是否审核通过", choices=((0, u"提交中"), (1, u"审核中"), (2, u"审核通过"), (-1, u"审核未通过")))
    comment = models.CharField(max_length=4096, verbose_name=u"审核意见", default="", blank=True, null=True)
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.photographer.is_reviewed = self.is_reviewed

        if self.photographer.is_reviewed == 2:
            self.photographer.user_type = True

        else:
            self.photographer.user_type = False
        self.photographer.save()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = u"3.审核记录"

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    """
        订单
    """
    class Const:
        FREE_ORDER_PRICE = 50.0

    user = models.ForeignKey(User, verbose_name=u"用户", related_name=u"order_model_user_user")
    photographer = models.ForeignKey(User, verbose_name=u"摄影师", related_name=u"order_photographer_photographer")
    state = models.IntegerField(default=0, verbose_name=u"订单状态", choices=((0, "预约中"), (1, "待付款"), (2, "进行中客户已付定金"),(3, "已确认客户支付全款"),(4, "已完成客户确认完成"), (5, "摄影师确认完成"), (6, "已取消")))
    type = models.IntegerField(verbose_name=u"订单类型", choices=((0, u"互免"), (1, u"收费")), default=0)
    price = models.FloatField(verbose_name=u"价格", default=0.0)
    place = models.CharField(max_length=1024, verbose_name=u"地点")
    place_type = models.IntegerField(default=0, choices=((0, u"室内"), (1, u"户外")), verbose_name=u"地点类型")

    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)
    time = models.DateTimeField(verbose_name="具体拍摄时间", default=timezone.now)

    score = models.IntegerField(default=0, verbose_name=u"分数", blank=True)
    content = models.CharField(max_length=4096, default=u"", blank=True, verbose_name=u"评价内容")

    images = models.ManyToManyField(UploadedImage, blank=True, verbose_name=u"评论图片")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.type == 0:
            self.price = Order.Const.FREE_ORDER_PRICE
        # 取消订单
        if self.state == 6 or self.state == 4:
            # 如果有订金已经支付，还给客户
            sid = transaction.savepoint()
            try:
                # 获取这个订单的已经支付的记录
                payments = Payment.objects.filter(order=self, state=2)
                total_pay = 0
                for p in payments:
                    # 如果有定金
                    if p.type == 0:
                        total_pay += Order.Const.FREE_ORDER_PRICE
                    # 如果是全款
                    else:
                        total_pay += p.order.price
                ################### 以下开始转帐 ########################
                if self.state == 4:
                    # 订单完成，开始转钱到摄影师
                    self.photographer.money = self.photographer.money + total_pay
                    self.photographer.save()
                else:
                    self.user.money = self.user.money + total_pay
                    self.user.save()
            except Payment.DoesNotExist:
                logger.debug(traceback.format_exc())
                transaction.savepoint_rollback(sid)



        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = u"7.订单"

    def __str__(self):
        return str(self.id) + u" - user:" + str(self.user)+" photographer:"+str(self.photographer)+" price:"+str(self.price)


class MomentComment(models.Model):
    """
        评论
    """
    user = models.ForeignKey(User, verbose_name="用户", related_name="moment_comment_user_user")
    reply_to = models.ForeignKey(User, blank=True, null=True, default=None, verbose_name="回复的用户", help_text="如果不是对回复的回复，则为空", related_name="moment_comment_reply_user")
    content = models.CharField(max_length=4096, verbose_name="内容", blank=False)
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    class Meta:
        verbose_name = u"8.发现的评论"


class Moment(models.Model):
    """
        一条朋友圈
    """
    user = models.ForeignKey(User, verbose_name="用户")
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)
    content = models.CharField(max_length=4096, verbose_name="内容", blank=False)
    images = models.ManyToManyField(UploadedImage, blank=True)
    comments = models.ManyToManyField(MomentComment, blank=True, verbose_name="相关评论")
    thumb_ups = models.IntegerField(default=0, verbose_name="点赞数")
    is_thumb_up = models.BooleanField(default=False, verbose_name="是否被点赞")

    class Meta:
        verbose_name = u"9.发现"

    def __str__(self):
        return str(self.id)


class ThumbUp(models.Model):
    """
        点赞记录
    """
    user = models.ForeignKey(User, verbose_name="用户")
    moment = models.ForeignKey(Moment, verbose_name="被点赞的发现")

    def delete(self, using=None, keep_parents=False):
        r = super().delete(using, keep_parents)
        moment = self.moment
        moment.thumb_ups = len(ThumbUp.objects.filter(moment=self.moment))
        moment.save()
        return r

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        moment = self.moment
        moment.thumb_ups = len(ThumbUp.objects.filter(moment=self.moment))
        moment.save()

    class Meta:
        verbose_name = u"3.点赞记录"
        unique_together = (('user', 'moment'), )    # 联合主键


class Payment(models.Model):
    """
        用户支付记录， 用户可以多次请求

        支付接口返回：
        {
            "appid":"wx316cdc76b22cb345",
            "noncestr":"9yNQzX3bAJkv8lyt",
            "package":"Sign=WXPay",
            "partnerid":"1518622231",
            "prepayid":"wx112156415238697c3f4d51de1276925071",
            "timestamp":1541944601,
            "sign":"3FE8A768E03FAE75842F207EA9359E59"
        }
    """
    pay_way = models.IntegerField(verbose_name=u"支付方式", default=0, choices=( (0, "微信"), (1, "支付宝")))

    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)
    user = models.ForeignKey(User, verbose_name="支付用户")
    order = models.ForeignKey(Order, verbose_name="支付订单")
    type = models.IntegerField(verbose_name="支付类型", default=1, choices=( (0, "定金"), (1, "全款")))
    state = models.IntegerField(verbose_name="支付状态", default=0, choices=((0, "支付中"), (1, "支付失败"), (2, "支付成功")))
    fee = models.IntegerField(verbose_name="支付金额", default=0.0)
    # sign = models.CharField(verbose_name="sign", max_length=1024, default="")
    # noncestr = models.CharField(verbose_name="noncestr", max_length=1024, default="")
    # package = models.CharField(verbose_name="package", max_length=1024, default="")
    # prepayid = models.CharField(verbose_name="prepayid", max_length=1024, default="")
    # timestamp = models.CharField(verbose_name="timestamp", max_length=1024, default="")
    # appid = models.CharField(verbose_name="appid", max_length=1024, default="")
    transaction_id = models.CharField(verbose_name="微信支付订单号", max_length=1024, default="")
    out_trade_no = models.CharField(verbose_name="商户订单号", max_length=1024, default="")
    msg = models.TextField(verbose_name=u"支付信息", default="" )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 开启事物
        sid = transaction.savepoint()
        # 如果是定金，支付成功后
        if self.type == 0 and self.state == 2:
            self.order.state = 2
        # 如果是全款,支付成功后
        elif self.type == 1 and self.state == 2:
            self.order.state = 3
        try:
            self.order.save()
            super().save(force_insert, force_update, using, update_fields)
        except:
            transaction.savepoint_rollback(sid)

    class Meta:
        verbose_name = u"2.用户支付记录"


class Withdraw(models.Model):
    """
        提现记录
    """
    is_with_draw = models.BooleanField(verbose_name="是否已经处理", choices=((False, u"未处理"), (True, u"已经转帐")),
                                       default=False, help_text="确认后，后台会给用户扣除帐号金额,不要重复处理")
    money = models.FloatField(verbose_name="提现金额", default=0.0)
    user = models.ForeignKey(User, verbose_name="提现用户")
    date = models.DateTimeField(verbose_name=u"上一次操作时间", auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 如果是刚申请体现，短信通知管理员
        logger.debug(self.money)
        logger.debug(self.user.money)
        assert float(self.money) <= float(self.user.money) or self.money > 0
        # 如果提现已经处理完成，修改用户金额，并短信通知提现者
        sid = transaction.savepoint()
        try:
            if self.is_with_draw:
                self.user.money = self.user.money - self.money
                self.user.save()
            super().save(force_insert, force_update, using, update_fields)
        except:
            transaction.savepoint_rollback(sid)

    class Meta:
        verbose_name = u"1.提现记录"


class AppConfig(models.Model):
    """
        系统统计
    """
    server = models.CharField(max_length=1024, verbose_name="服务器地址", default="http://118.25.221.34:8080")
    alipay = models.CharField(verbose_name=u"后台支付宝帐号", default="88888888", max_length=48)
    wechat = models.CharField(verbose_name=u"后台微信支付帐号", default='88888888', max_length=48)
    in_use = models.BooleanField(default=True, verbose_name="是否启用", help_text=u"同时只能有一个生效")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        sid = transaction.savepoint()
        try:
            if self.in_use:
                for ac in AppConfig.objects.all():
                    ac.in_use = False
                    ac.save()
            super().save(force_insert, force_update, using, update_fields)
        except:
            transaction.savepoint_rollback(sid)

    class Meta:
        verbose_name = u"系统设置"
