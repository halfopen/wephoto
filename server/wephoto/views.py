# coding: utf-8
from django.shortcuts import *
from django.http.response import *
from wephoto.models import *
from wephoto.serializers import *
from django.core.exceptions import *

import hashlib
from server import tokens
from rest_framework.renderers import JSONRenderer
from PIL import Image

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
    phone = req.GET.get("phone", "")
    password = req.GET.get("password", "")

    try:
        user = User.objects.get(phone=phone, password=password)
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
        img = Image.open(myFile)
        if img.size[0] > 800 or img.size[1] > 600:
            newWidth = 800
            newHeight = float(800) / img.size[0] * img.size[1]
            img.thumbnail((newWidth,newHeight),Image.ANTIALIAS)
        filename = str(time.time())+".png"
        destination = open(os.path.join(settings.MEDIA_ROOT, filename),'wb+')    # 打开特定的文件进行二进制的写操作
        # for chunk in myFile.chunks():      # 分块写入文件
        #     destination.write(chunk)
        # destination.close()
        img.save(os.path.join(settings.MEDIA_ROOT, filename), format='PNG')
        u = UploadedImage(file=settings.SERVER_ADDR+"/media/"+filename, tag=tag)
        u.save()
        slz = UploadedImageSerializer(u)
        print(type(slz.data), slz.data)
        data = slz.data
        return JsonResponse(data)


def comment_moment(req):
    if req.method == "POST":
        user = req.POST.get("user")
        reply_to = req.POST.get("reply_to")
        content = req.POST.get("content")
        moment_id = req.POST.get("moment_id")

        moment = Moment.objects.get(id=moment_id)
        user = User.objects.get(id=user)
        moment_comment = MomentComment(user=user, content=content, reply_to=reply_to)
        moment_comment.save()
        moment.comments.add(moment_comment)
        moment.save()

        slz = MomentSerializer(moment)
        return JsonResponse(slz)


# def save_file(file, dir):
#     filename = str(time.time()) + file.name
#     root = os.path.join(settings.MEDIA_ROOT, dir)
#     if not os.path.exists(root):
#         os.mkdir(root)
#     destination = open(os.path.join(root, filename), 'wb+')
#     for chunk in file.chunks():  # 分块写入文件
#         destination.write(chunk)
#     destination.close()
#     return filename


# # 上传用户头像
# def upload_avatar(req):
#     if req.method == "POST":
#         avatar = req.FILES.get("avatar", None)
#         uid = req.POST.get("id", None)
#         if not avatar:
#             return JsonResponse(BaseJsonResponse("no file for upload", "").error())
#         if not uid:
#             return JsonResponse(BaseJsonResponse("need provide uid", "").error())
#         user = User.objects.get(id=uid)
#         if not user:
#             return JsonResponse(BaseJsonResponse("user do not exist", "").error())
#         filename = save_file(avatar, "avatar")
#         user.avatar = "/avatar/"+filename
#         user.save()
#         return JsonResponse(BaseJsonResponse("upload ok", {"avatar":settings.SERVER_ADDR+"/media/avatar/"+filename}).info())
#
#
# # 上传个人首页图片
# def upload_home_img(req):
#     if req.method == "POST":
#         home_img = req.FILES.get("home_img", None)
#         uid = req.POST.get("id", None)
#         if not home_img:
#             return JsonResponse(BaseJsonResponse("no file for upload", "").error())
#         if not uid:
#             return JsonResponse(BaseJsonResponse("need provide uid", "").error())
#         user = User.objects.get(id=uid)
#         if not user:
#             return JsonResponse(BaseJsonResponse("user do not exist", "").error())
#         filename = save_file(home_img, "home_img")
#         user.home_img = "/home_img/" + filename
#         user.save()
#         return JsonResponse(
#             BaseJsonResponse("upload ok", {"home_img": settings.SERVER_ADDR + "/media/home_img/" + filename}).info())


# def review(req):
#     """
#         添加一个审核，提交个人资料
#     :param req:
#     :return:
#     """
#     if req.method == "POST":
#         id = req.POST.get("id", None) # 摄影师id
#         name = req.POST.get("name", None)
#         id_card_num = req.POST.get("id_card_num", None)
#         gender = req.POST.get("gender", None)
#         birthday = req.POST.get("birthday", None)
#
#         if not id:
#             return JsonResponse(BaseJsonResponse("need provide id", "").error())
#         p = User.objects.get(id=id)
#         try:
#             r = Review.objects.get(photographer=p)
#         except Review.DoesNotExist:
#             r = Review(photographer=p, is_reviewed=0)
#         r.name = name
#         r.id_card_num = id_card_num
#         r.gender = gender
#         r.birthday = birthday
#         r.save()
#         return JsonResponse(BaseJsonResponse("ok", "").info())
#
#
# def submit_review_image(req):
#     """
#         提交审核的三张照片
#     :param req:
#     :return:
#     """
#     if req.method == "POST":
#         device_1 = req.FILES.get("device_1", None)
#         device_2 = req.FILES.get("device_2", None)
#         device_3 = req.FILES.get("device_3", None)
#         id_card_1 = req.FILES.get("id_card_1", None)
#         id_card_2 = req.FILES.get("id_card_2", None)
#         id_card_1_file = save_file(id_card_1, "id_card")
#         id_card_2_file = save_file(id_card_2, "id_card")
#
#
#         id = req.POST.get("id", None)
#         if not id:
#             return JsonResponse(BaseJsonResponse("need provide id", "").error())
#         r = Review.objects.get(photographer=id)
#         if not r:
#             return JsonResponse(BaseJsonResponse("review do not exist", "").error())
#
#         device_1_file = save_file(device_1, "device")
#         device_2_file = save_file(device_2, "device")
#         device_3_file = save_file(device_3, "device")
#         r.device_1 = "/device/"+device_1_file
#         r.device_2 = "/device/"+device_2_file
#         r.device_3 = "/device/"+device_3_file
#         r.save()
#         return JsonResponse(BaseJsonResponse("upload ok", "").info())
#
#
# def submit_review(req):
#     """
#         提交审核申请
#     :param req:
#     :return:
#     """
#     if req.method == "POST":
#         id = req.POST.get("id", None)
#         if not id:
#             return JsonResponse(BaseJsonResponse("need provide id", "").error())
#         p = User.objects.get(id=id)
#         r = Review.objects.get(photographer=p)
#         if not r:
#             return JsonResponse(BaseJsonResponse("review do not exist", "").error())
#         r.is_reviewed = 1
#         r.save()
#         return JsonResponse(BaseJsonResponse("ok", "").info())