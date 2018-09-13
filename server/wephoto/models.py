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
    gender = models.IntegerField(default=0, choices=((0, u"男"), (1, u"女")))
    avatar = models.ImageField(upload_to="avatar", blank=True, verbose_name="头像", null=True)

    qq = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"QQ号")
    wechat = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"微信号")
    birthday = models.DateField(verbose_name="出生年月日", null=True, blank=True)

    money = models.FloatField(default=0.0, verbose_name=u"余额", blank=True, null=True)
    in_order_money = models.FloatField(default=0.0, verbose_name=u"冻结金额", blank=True, null=True)
    album = models.ManyToManyField(UploadedImage, verbose_name=u"相册", blank=True, null=True)
    bank_card = models.CharField(max_length=1024, verbose_name=u"银行卡", blank=True, null=True)

    address = models.CharField(default="", max_length=1024, verbose_name=u"所在地区", null=True, blank=True)
    # 以下为摄影师字段
    user_type = models.BooleanField(verbose_name=u"是否为摄影师", choices=((False, u"普通用户"), (True, u"摄影师")))
    is_reviewed = models.IntegerField(default=0, verbose_name="是否审核通过",
                                      choices=((0, u"未提交"), (1, u"审核中"), (2, u"审核通过"), (-1, u"审核未通过")), blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    desc = models.CharField(max_length=4096, verbose_name=u"个人签名", null=True, blank=True, default="")
    home_img = models.ImageField(verbose_name=u"主页图片", null=True, blank=True)
    pay_way = models.IntegerField(default=0, verbose_name=u"收费方式", choices=((0, u"互免"), (1, u"收费")), null=True, blank=True)
    price = models.FloatField(default=0.0, verbose_name=u"价格", null=True, blank=True)
    visit = models.IntegerField(default=0, verbose_name=u"访问量", null=True, blank=True)

    likes = models.ManyToManyField("self", verbose_name="收藏", null=True, blank=True)  # 普通用户才能收藏

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

    class Meta:
        verbose_name = u"审核记录"


class Order(models.Model):
    """
        订单
    """
    model_user = models.ForeignKey(User, verbose_name="用户", related_name="order_model_user")
    photographer = models.ForeignKey(User, verbose_name="摄影师", related_name="order_photographer")
    state = models.IntegerField(default=0, verbose_name="订单状态", )
    type = models.IntegerField(verbose_name="订单类型")
    price = models.FloatField(verbose_name="价格")
    place = models.CharField(max_length=1024, verbose_name=u"地点")
    place_type = models.IntegerField(default=0, choices=((0, u"室内"), (1, u"户外")))
    year = models.IntegerField(default=2018, verbose_name=u"年")
    month = models.IntegerField(default=1, verbose_name=u"月")
    day = models.IntegerField(default=1, verbose_name=u"日")

    date = models.DateField(verbose_name="日期")

    class Meta:
        verbose_name = u"订单"


class OrderComment(models.Model):
    """
        订单评价
    """
    order = models.OneToOneField(Order)
    score = models.IntegerField(default=5, verbose_name="分数")
    content = models.CharField(max_length=4096)

    images = models.ManyToManyField(UploadedImage)


class AppConfig(models.Model):
    """
        系统统计
    """

    class Meta:
        verbose_name = u"系统设置"
