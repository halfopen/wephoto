"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from server import settings
import wephoto.urls
from wephoto.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^api/', include(wephoto.urls)),
    url(r'^login', login),
    url(r'^register', register),
    url(r'^upload_image', upload_image),
    url(r'^send_verify_code', send_verify_code),
    url(r'^notify', notify),
    url(r'^order_count', order_count)

    # url(r'^comment_moment', comment_moment)
    # url(r'^upload_avatar', upload_avatar),
    # url(r'^upload_home_img', upload_home_img),
    # url(r'^review', review),
    # url(r'^submit_review_device', submit_review_device),
    # url(r'^submit_review', submit_review),
]
