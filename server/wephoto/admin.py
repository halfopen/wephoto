from django.contrib import admin
from django.utils.safestring import mark_safe
from form_utils.widgets import *
from django.db import models
from wephoto.models import *
from django.utils.html import *

admin.site.name = "约拍"


class MyImageWidget(ImageWidget):
    template = '%(input)s<br />%(image)s'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        input_html = super(ImageWidget, self).render(name, value, attrs)
        image_html = value
        if hasattr(value, 'name'):
            image_html = '<a href="/media/%s" target="_blank"><img style="width:200px; height:200px" src="/media/%s"/></a>' %( value.name, value.name)
        output = self.template % {'input': input_html,
                                  'image': image_html}
        return mark_safe(output)


class PhotographerAdmin(admin.ModelAdmin):
    list_display = ('name', 'avator_image')
    formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}

    readonly_fields = ('works_url', )

    def works_url(self, obj):
        return format_html("""<a href='/admin/wephoto/uploadedimage/?q={0}'　target='_blank'>作品集</a>""", str(obj.id)+"-works")


class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'tag')
    search_fields = ('tag',)
    formfield_overrides = {models.ImageField: {'widget': MyImageWidget}}


admin.site.register(Photographer, PhotographerAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(CommonUser)
admin.site.register(Tag)
admin.site.register(UploadedImage, UploadedImageAdmin)