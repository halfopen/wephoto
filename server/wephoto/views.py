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

# 初始化tag
try:
    tags = Tag.objects.count()
    if tags == 0:
        tags_list = ['清新', '日系', '少女', '情绪', '校园']
        for t in tags_list:
            o = Tag(content=t)
            o.save()
except:
    pass

# 初始化配置
try:
    if AppConfig.objects.count() == 0:
        AppConfig(server="http://118.25.221.34:8080", wechat="88888888", alipay="88888888", in_use=True).save()
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
        tokens[token] = user.id
    except User.DoesNotExist:
        return JsonResponse(BaseJsonResponse("用户名/密码错误", "").error())
    except:
        return JsonResponse(BaseJsonResponse("登录失败", "").error())

    return JsonResponse(BaseJsonResponse("登录成功", {"token":token, "id":user.id}).info())


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
        filename = str(time.time())+".jpeg"
        new_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        new_dir = os.path.join(settings.MEDIA_ROOT, new_date)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        img.save(os.path.join(new_dir, filename), format='JPEG')
        img.thumbnail((100, 100), Image.ANTIALIAS)
        img.save(os.path.join(new_dir, filename.replace(".jpeg", "-100x100.jpeg")), format='JPEG')
        u = UploadedImage(file=settings.SERVER_ADDR+"/media/"+new_date+"/"+filename, tag=tag)
        u.save()
        slz = UploadedImageSerializer(u)
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


def send_verify_code(req):
    print(req.META)
    if req.META.get('HTTP_X_FORWARDED_FOR'):
        ip = req.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = req.META['REMOTE_ADDR']
    print(ip)
    return JsonResponse(BaseJsonResponse("ok", {"ip":ip}).info())