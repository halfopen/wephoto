# coding=utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe
from form_utils.widgets import *
from django.db import models
from wephoto.models import *
from django.utils.html import *

admin.site.name = u"约拍"
admin.site.site_header = "约拍后台管理"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'avatar_image', "name", "user_type", "gender")
    # formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}

    readonly_fields = (u'作品集', u"相册", '用户头像', '主页图片')
    exclude = ('avatar', 'home_img', )

    list_filter = ('user_type', 'gender')

    def 作品集(self, obj):
        return format_html("""<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>作品集</a>""", str(obj.id)+"-works")

    def 相册(self, obj):
        return format_html("""<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>相册</a>""", str(obj.id)+"-album")

    def 用户头像(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.avatar)

    def 主页图片(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.home_img)


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'tag')
    search_fields = ('tag',)
    # formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'photographer', 'state', 'type', 'price', 'place', 'place_type')
    date_hierarchy = 'date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('photographer', 'is_reviewed', 'comment')
    list_filter = ('is_reviewed',)

    readonly_fields = ('id_card_1_view', 'id_card_2_view', 'device_1_view', "device_2_view", "device_3_view", "审核作品")
    exclude = ('id_card_1','id_card_2', 'device_1', 'device_2', 'device_3')

    def id_card_1_view(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.id_card_1)

    def id_card_2_view(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.id_card_2)

    def device_1_view(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.device_1)

    def device_2_view(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.device_2)

    def device_3_view(self, obj):
        return format_html(u'<img style="width:200px; height:200px" src="%s"/>' % obj.device_3)

    def 审核作品(self, obj):
        return format_html("<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>审核作品</a>", str(obj.photographer.id)+"-review-works")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content')
    readonly_fields = ('images_view', )
    exclude = ('images', )
    date_hierarchy = 'date'

    def images_view(self, obj):

        html = ""
        print("qxk", obj.images, type(obj.images), obj.images.all())
        for i in obj.images.all():
            html = html+ u'<img style="width:200px; height:200px" src="%s"/>' % i.file
        return format_html(html)
    images_view.verbose_name = "图片"


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'money', '用户名', '手机', '开户银行', '银行卡号', 'date')
    list_filter = ('is_with_draw', )
    date_hierarchy = 'date'
    list_display = ('id', 'user', '用户名', '手机', 'money', 'is_with_draw', 'date',)

    def 手机(self, obj):
        return str(obj.user.phone)

    def 用户名(self, obj):
        return obj.user.name

    def 开户银行(self, obj):
        return obj.user.bnak

    def 银行卡号(self, obj):
        return obj.user.bank_card

    def has_add_permission(self, request):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ('id', 'order', 'user', 'pay_way', 'msg', 'date')
    date_hierarchy = 'date'
    list_display = ('id', 'order', 'user', 'pay_way', 'msg', 'date')

    def has_add_permission(self, request):
        return False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')


@admin.register(MomentComment)
class MomentCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'reply_to', 'date')
    date_hierarchy = 'date'


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'alipay', 'wechat', 'in_use')