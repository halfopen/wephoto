from django.db import models
from django.utils.safestring import mark_safe


class UploadedImage(models.Model):
    file = models.ImageField(verbose_name="图片")
    tag = models.CharField(max_length=1024, default="")

    def image(self):
        return '<img style="width:60px; height:60px" src="/media/%s"/>' % self.file

    image.allow_tags = True

    class Meta:
        verbose_name = u"上传的图片"

    def __str__(self):
        return self.file.name + " "+ self.tag


class Tag(models.Model):
    """

    """
    content = models.CharField(max_length=48, unique=True, verbose_name="标签名")
    count = models.IntegerField(default=0, verbose_name="使用次数")

    class Meta:
        verbose_name = u"标签"

    def __str__(self):
        return self.content


class User(models.Model):
    """
        用户抽象类
    """
    phone = models.CharField(max_length=32, null=False, unique=True, verbose_name=u"手机")
    username = models.CharField(max_length=1024, verbose_name="用户名", null=False, blank=False)
    password = models.CharField(max_length=1024, verbose_name="密码", null=False, blank=False)
    gender = models.IntegerField(default=0, choices=((0, u"男"), (1, u"女")), verbose_name=u"性别")
    avatar = models.ImageField(upload_to="avatar", blank=True, verbose_name="头像", default="")

    qq = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"QQ号", default="")
    wechat = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"微信号", default="")
    birthday = models.DateField(verbose_name="出生年月日",  blank=True,  default="1995-01-01")

    money = models.FloatField(default=0.0, verbose_name=u"余额", blank=True)
    in_order_money = models.FloatField(default=0.0, verbose_name=u"冻结金额", blank=True)
    album = models.ManyToManyField(UploadedImage, verbose_name=u"相册", blank=True)
    bank_card = models.CharField(max_length=1024, verbose_name=u"银行卡", blank=True)

    address = models.CharField(default="", max_length=1024, verbose_name=u"所在地区", null=True, blank=True)
    # 以下为摄影师字段
    order_count = models.IntegerField(verbose_name="已完成订单数", default=0, blank=True)
    user_type = models.BooleanField(verbose_name=u"是否为摄影师", choices=((False, u"普通用户"), (True, u"摄影师")), default=False, blank=True)
    is_reviewed = models.IntegerField(default=0, verbose_name="是否审核通过",
                                      choices=((0, u"未提交"), (1, u"审核中"), (2, u"审核通过"), (-1, u"审核未通过")), blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name=u"用户标签")
    desc = models.CharField(max_length=4096, verbose_name=u"个人签名", null=True, blank=True, default="")
    home_img = models.ImageField(verbose_name=u"主页图片",  blank=True)
    pay_way = models.IntegerField(default=0, verbose_name=u"收费方式", choices=((0, u"互免"), (1, u"收费")), null=False, blank=True)
    price = models.FloatField(default=0.0, verbose_name=u"价格", blank=True)
    visit = models.IntegerField(default=0, verbose_name=u"访问量", blank=True)

    likes = models.ManyToManyField("self", verbose_name="收藏", blank=True)  # 普通用户才能收藏
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    class Meta:
        verbose_name = u"用户"

    def avatar_image(self):
        return '<img style="width:60px; height:60px" src="/media/%s"/>' % self.avatar

    avatar_image.allow_tags = True
    avatar_image.verbose_name = "头像"

    def __str__(self):
        return self.phone+"-"+self.username


class Review(models.Model):
    """
        审核记录
    """
    photographer = models.OneToOneField(User)
    id_card_1 = models.ImageField(verbose_name="正面身份证")
    id_card_2 = models.ImageField(verbose_name="反面身份证")
    device_1 = models.ImageField(verbose_name=u"使用设备－前面")
    device_2 = models.ImageField(verbose_name=u"使用设备－后面")
    device_3 = models.ImageField(verbose_name=u"使用设备－侧面")

    is_reviewed = models.IntegerField(default=False, verbose_name="是否审核通过")
    comment = models.CharField(max_length=4096, verbose_name=u"审核意见", default="")
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    class Meta:
        verbose_name = u"审核记录"


class OrderComment(models.Model):
    """
        订单评价
    """
    score = models.IntegerField(default=5, verbose_name="分数")
    content = models.CharField(max_length=4096, default="", blank=True, verbose_name="内容")
    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    images = models.ManyToManyField(UploadedImage, blank=True)

    class Meta:
        verbose_name = u"订单评价"


class Order(models.Model):
    """
        订单
    """
    user = models.ForeignKey(User, verbose_name="用户", related_name="order_model_user_user")
    photographer = models.ForeignKey(User, verbose_name="摄影师", related_name="order_photographer_photographer")
    state = models.IntegerField(default=0, verbose_name="订单状态", choices=((0, "新建"), (1, "进行中"), (2, "已完成"), (3, "已取消")))
    type = models.IntegerField(verbose_name="订单类型", choices=((0, "互免"), (1, "收费")), default=0)
    price = models.FloatField(verbose_name="价格", default=0.0)
    place = models.CharField(max_length=1024, verbose_name=u"地点")
    place_type = models.IntegerField(default=0, choices=((0, u"室内"), (1, u"户外")))

    date = models.DateTimeField(verbose_name=u"最后修改日期", auto_now=True)

    comment = models.OneToOneField(OrderComment, null=True, blank=True)

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
    comments = models.ManyToManyField(MomentComment, blank=True)

    class Meta:
        verbose_name = u"发现"


class AppConfig(models.Model):
    """
        系统统计
    """

    class Meta:
        verbose_name = u"系统设置"
