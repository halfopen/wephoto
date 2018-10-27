# coding=utf-8
from django.db import models
from django.utils.safestring import mark_safe
from .storage import *


class UploadedImage(models.Model):
    file = models.CharField(max_length=2048, verbose_name="地址")
    tag = models.CharField(max_length=1024, default="", db_index=True)

    def image(self):
        return '<img style="width:200px; height:200px" src="%s"/>' % self.file

    image.allow_tags = True

    class Meta:
        verbose_name = u"上传的图片"

    def __str__(self):
        return self.file + " " + self.tag


class Tag(models.Model):
    """

    """
    content = models.CharField(max_length=48, unique=True, verbose_name=u"标签名")
    count = models.IntegerField(default=0, verbose_name=u"使用次数")

    class Meta:
        verbose_name = u"标签"

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

    bank_card = models.CharField(max_length=1024, verbose_name=u"银行卡", blank=True)

    address = models.CharField(default="", max_length=1024, verbose_name=u"所在地区", null=True, blank=True)
    # 以下为摄影师字段
    order_count = models.IntegerField(verbose_name=u"已完成订单数", default=0, blank=True)
    user_type = models.BooleanField(verbose_name=u"是否为摄影师", choices=((False, u"普通用户"), (True, u"摄影师")), default=False, blank=True)
    is_reviewed = models.IntegerField(default=0, verbose_name=u"是否审核通过",
                                      choices=((0, u"未提交"), (1, u"审核中"), (2, u"审核通过"), (-1, u"审核未通过")), blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name=u"用户标签")
    desc = models.CharField(max_length=4096, verbose_name=u"个人签名", null=True, blank=True, default=u"")
    home_img = models.CharField(max_length=2048, verbose_name=u"主页图片",  blank=True)
    pay_way = models.IntegerField(default=0, verbose_name=u"收费方式", choices=((0, u"互免"), (1, u"收费")), null=False, blank=True)
    price = models.FloatField(default=0.0, verbose_name=u"价格", blank=True)
    visit = models.IntegerField(default=0, verbose_name=u"访问量", blank=True)

    likes = models.ManyToManyField("self", verbose_name=u"收藏", blank=True)  # 普通用户才能收藏
    available_date = models.TextField(verbose_name=u"可预约时间", blank=True, default="", null=True)
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    class Meta:
        verbose_name = u"用户"

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
        verbose_name = u"审核记录"


class Order(models.Model):
    """
        订单
    """
    user = models.ForeignKey(User, verbose_name=u"用户", related_name=u"order_model_user_user")
    photographer = models.ForeignKey(User, verbose_name=u"摄影师", related_name=u"order_photographer_photographer")
    state = models.IntegerField(default=0, verbose_name=u"订单状态", choices=((0, "预约中"), (1, "待付款"), (2, "进行中"),(3, "已确认"), (4, "已完成"), (5, "已取消")))
    type = models.IntegerField(verbose_name=u"订单类型", choices=((0, u"互免"), (1, u"收费")), default=0)
    price = models.FloatField(verbose_name=u"价格", default=0.0)
    place = models.CharField(max_length=1024, verbose_name=u"地点")
    place_type = models.IntegerField(default=0, choices=((0, u"室内"), (1, u"户外")), verbose_name=u"地点类型")

    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    score = models.IntegerField(default=5, verbose_name=u"分数", blank=True)
    content = models.CharField(max_length=4096, default=u"", blank=True, verbose_name=u"评价内容")

    images = models.ManyToManyField(UploadedImage, blank=True, verbose_name=u"评论图片")

    class Meta:
        verbose_name = u"订单"


class MomentComment(models.Model):
    """
        评论
    """
    user = models.ForeignKey(User, verbose_name="用户", related_name="moment_comment_user_user")
    reply_to = models.ForeignKey(User, blank=True, null=True, default=None, verbose_name="回复的用户", help_text="如果不是对回复的回复，则为空", related_name="moment_comment_reply_user")
    content = models.CharField(max_length=4096, verbose_name="内容", blank=False)
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    class Meta:
        verbose_name = u"发现的评论"


class Moment(models.Model):
    """
        一条朋友圈
    """
    user = models.ForeignKey(User, verbose_name="用户")
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)
    content = models.CharField(max_length=4096, verbose_name="内容", blank=False)
    images = models.ManyToManyField(UploadedImage, blank=True)
    comments = models.ManyToManyField(MomentComment, blank=True, verbose_name="相关评论")

    class Meta:
        verbose_name = u"发现"


class AppConfig(models.Model):
    """
        系统统计
    """

    class Meta:
        verbose_name = u"系统设置"
