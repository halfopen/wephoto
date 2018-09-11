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
    phone = models.CharField(max_length=32, null=False, primary_key=True)
    username = models.CharField(max_length=1024, verbose_name="用户名")
    password = models.CharField(max_length=1024, verbose_name="密码")
    gender = models.IntegerField(default=0, choices=((0, u"男"), (1, u"女")))
    avator = models.ImageField(upload_to="avator", blank=True, verbose_name="头像", null=True)

    qq = models.CharField(max_length=32, null=True)
    wechat = models.CharField(max_length=32, null=True)

    money = models.FloatField(default=0.0, verbose_name=u"余额")
    in_order_money = models.FloatField(default=0.1, verbose_name=u"冻结金额")

    class Meta:
        abstract = True

    def avator_image(self):
        return '<img style="width:60px; height:60px" src="/media/%s"/>' % self.avator

    avator_image.allow_tags = True
    avator_image.verbose_name = "头像"

    def __str__(self):
        return self.phone+"-"+self.username


class Photographer(User):
    """
        摄影师
    """

    is_reviewed = models.IntegerField(default=0, verbose_name="是否审核通过")
    tags = models.ManyToManyField(Tag)
    desc = models.CharField(max_length=4096, verbose_name=u"个人签名")
    home_img = models.ImageField(verbose_name=u"主页图片", null=True, blank=True)
    pay_way = models.IntegerField(default=0, verbose_name=u"收费方式", choices=((0, u"互免"), (1, u"收费")))
    price = models.FloatField(default=0.0, verbose_name=u"价格")
    visit = models.IntegerField(default=0, verbose_name=u"访问量")

    class Meta:
        verbose_name = u"摄影师"


class CommonUser(User):
    """

    """
    class Meta:
        verbose_name = u"普通用户"


class Review(models.Model):
    """
        审核记录
    """
    photographer = models.OneToOneField(Photographer)
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
    model_user = models.ForeignKey(CommonUser, verbose_name="用户")
    photographer = models.ForeignKey(Photographer, verbose_name="摄影师")
    type = models.IntegerField(verbose_name="订单类型")
    price = models.FloatField(verbose_name="价格")
    place = models.CharField(max_length=1024, verbose_name=u"地点")
    place_type = models.IntegerField(default=0, choices=((0, u"室内"), (1, u"户外")))
    year = models.IntegerField(default=2018, verbose_name=u"年")
    month = models.IntegerField(default=1, verbose_name=u"月")
    day = models.IntegerField(default=1, verbose_name=u"日")

    class Meta:
        verbose_name = u"订单"


class OrderComment(models.Model):
    """
        订单评价
    """
    order = models.OneToOneField(Order)
    score = models.IntegerField(default=5, verbose_name="分数")
    content = models.CharField(max_length=4096)

    #images = models.OneToOneField(Gallery)


class AppConfig(models.Model):
    """
        系统统计
    """

    class Meta:
        verbose_name = u"系统设置"
