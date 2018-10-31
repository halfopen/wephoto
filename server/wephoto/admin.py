# coding=utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe
from form_utils.widgets import *
from django.db import models
from wephoto.models import *
from django.utils.html import *

admin.site.name = u"约拍"
admin.site.site_header = "约拍后台管理"


# class MyImageWidget(ImageWidget):
#     template = '%(input)s<br />%(image)s'
#
#     def __init__(self, attrs=None, template=None, width=200, height=200):
#         if template is not None:
#             self.template = template
#         self.width = width
#         self.height = height
#         super(ImageWidget, self).__init__(attrs)
#
#     def render(self, name, value, attrs=None):
#         input_html = super(ImageWidget, self).render(name, value, attrs)
#         image_html = value
#         if hasattr(value, 'name'):
#             image_html = '<a href="/media/%s" target="_blank"><img style="width:200px; height:200px" ' \
#                          'src="/media/%s"/></a>' % (value.name, value.name)
#         output = self.template % {'input': input_html,
#                                   'image': image_html}
#         return mark_safe(output)


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'avatar_image')
    # formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}

    readonly_fields = (u'作品集', u"相册")

    list_filter = ('user_type', )

    def 作品集(self, obj):
        return format_html("""<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>作品集</a>""", str(obj.id)+"-works")

    def 相册(self, obj):
            return format_html("""<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>相册</a>""", str(obj.id)+"-album")


class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'tag')
    search_fields = ('tag',)
    # formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'photographer', 'state', 'type', 'price', 'place', 'place_type')
    date_hierarchy = 'date'


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


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)
admin.site.register(UploadedImage, UploadedImageAdmin)
admin.site.register(Moment)
admin.site.register(MomentComment)