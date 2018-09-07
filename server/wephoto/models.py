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


class User(models.Model):
    """
        用户抽象类
    """
    name = models.CharField(max_length=1024, verbose_name="昵称")
    username = models.CharField(max_length=1024, verbose_name="用户名")
    password = models.CharField(max_length=1024, verbose_name="密码")
    gender = models.CharField(max_length=2, default="男")
    avator = models.ImageField(
        upload_to="avator", blank=True,
        verbose_name="原图", null=True)
    phone = models.CharField(max_length=32, null=False)
    qq = models.CharField(max_length=32, null=True)
    wechat = models.CharField(max_length=32, null=True)

    class Meta:
        abstract = True

    def avator_image(self):
        return '<img style="width:60px; height:60px" src="/media/%s"/>' % self.avator

    avator_image.allow_tags = True
    avator_image.verbose_name = "头像"


class Photographer(User):
    """

    """

    is_reviewed = models.IntegerField(default=0, verbose_name="是否审核通过")
    id_card_1 = models.ImageField(verbose_name="正面身份证")
    id_card_2 = models.ImageField(verbose_name="反面身份证")

    works = models.CharField(max_length=4096, verbose_name="作品集")

    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = u"摄影师"


class CommonUser(User):
    """

    """
    class Meta:
        verbose_name = u"普通用户"


class Review(models.Model):
    """
        审核请求
    """
    photographer = models.OneToOneField(Photographer)
    is_reviewed = models.IntegerField(default=False, verbose_name="是否审核通过")
    comment = models.CharField(max_length=4096, verbose_name=u"审核意见", default="")

    class Meta:
        verbose_name = u"审核记录"


class Order(models.Model):
    """
        订单
    """
    model_user = models.OneToOneField(CommonUser, verbose_name="用户")
    photophrapher = models.OneToOneField(Photographer, verbose_name="摄影师")
    type = models.IntegerField(verbose_name="订单类型")
    price = models.FloatField(verbose_name="价格")
    place = models.CharField(max_length=1024, verbose_name=u"地点")

    class Meta:
        verbose_name = u"订单"


class OrderEvaluation(models.Model):
    """
        订单评价
    """
    order = models.OneToOneField(Order)
    score = models.IntegerField(default=5, verbose_name="分数")
    content = models.CharField(max_length=4096)
    #images = models.OneToOneField(Gallery)

