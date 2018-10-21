# coding: utf-8
from django.shortcuts import *
from django.http.response import *
from wephoto.models import *
from wephoto.serializers import *
from django.core.exceptions import *

import hashlib
from server import tokens
from rest_framework.renderers import JSONRenderer


try:
    tags = Tag.objects.count()
    if tags == 0:
        tags_list = ['清新', '日系', '少女', '情绪', '校园']
        for t in tags_list:
            o = Tag(content=t)
            o.save()
except:
    pass


class BaseJsonResponse:
    def __init__(self, info, data):
        self.obj = dict()
        self.obj['info'] = info
        self.obj['data'] = data

    def error(self):
        self.obj['code'] = -1
        return self.obj

    def info(self):
        self.obj['code'] = 0
        return self.obj


def login(req):
    """
        用户登录
    :param req:
    :return:
    """
    username = req.GET.get("username", "")
    password = req.GET.get("password", "")

    try:
        user = User.objects.get(username=username, password=password)
        sec_str = str(user.id)+"-"+user.password+settings.SECRET_KEY
        token = hashlib.sha1(sec_str.encode("utf-8")).hexdigest()
        user.token = token
        user.save()
        tokens[str(user.id)] = token
    except User.DoesNotExist:
        return JsonResponse(BaseJsonResponse("用户名/密码错误", "").error())
    except:
        return JsonResponse(BaseJsonResponse("登录失败", "").error())

    return JsonResponse(BaseJsonResponse("登录成功", {"token":token, "id":user.id}).info())


def like(req):
    """
        收藏
    :param req:
    :return:
    """
    pass

# 上传upload image对象
def upload_image(req):
    # print(req)
    if req.method == "POST":    # 请求方法为POST时，进行处理
        myFile =req.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        tag = req.POST.get("tag", "")
        # print(req.FILES)
        if not myFile:
            return HttpResponse("no files for upload!")
        filename = str(time.time())+myFile.name
        destination = open(os.path.join(settings.MEDIA_ROOT, filename),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        u = UploadedImage(file=filename, tag=tag)
        u.save()
        slz = UploadedImageSerializer(u)
        print(type(slz.data), slz.data)
        data = slz.data
        data['file'] = settings.SERVER_ADDR+data['file']
        return JsonResponse(data)

# 上传用户头像
def upload_avatar(req):
    if req.method == "POST":
        avatar = req.FILES.get("avatar", None)
        uid = req.POST.get("id", None)
        if not avatar:
            return JsonResponse(BaseJsonResponse("no file for upload", "").error())
        if not uid:
            return JsonResponse(BaseJsonResponse("need provide uid", "").error())
        user = User.objects.get(id=uid)
        if not user:
            return JsonResponse(BaseJsonResponse("user do not exist", "").error())
        filename = str(time.time()) + avatar.name
        avatar_root = os.path.join(settings.MEDIA_ROOT, "avatar")
        print(avatar_root)
        destination = open(os.path.join(avatar_root, filename), 'wb+')
        for chunk in avatar.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        user.avatar = "/avatar/"+filename
        user.save()
        return JsonResponse(BaseJsonResponse("upload ok", {"avatar":settings.SERVER_ADDR+"/media/avatar/"+filename}).info())


# 上传个人首页图片
def upload_home_img(req):
    if req.method == "POST":
        home_img = req.FILES.get("home_img", None)
        uid = req.POST.get("id", None)
        if not home_img:
            return JsonResponse(BaseJsonResponse("no file for upload", "").error())
        if not uid:
            return JsonResponse(BaseJsonResponse("need provide uid", "").error())
        user = User.objects.get(id=uid)
        if not user:
            return JsonResponse(BaseJsonResponse("user do not exist", "").error())
        filename = str(time.time()) + home_img.name
        avatar_root = os.path.join(settings.MEDIA_ROOT, "home_img")
        print(avatar_root)
        destination = open(os.path.join(avatar_root, filename), 'wb+')
        for chunk in home_img.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        user.home_img = "/home_img/" + filename
        user.save()
        return JsonResponse(
            BaseJsonResponse("upload ok", {"home_img": settings.SERVER_ADDR + "/media/home_img/" + filename}).info())


