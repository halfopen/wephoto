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
import random
import traceback

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
import uuid
import oss2
import  xml.dom.minidom as xmldom
from django.db.models.aggregates import Count
import os

import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__business_id = uuid.uuid1()

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '16mm')


region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


from server.settings import *
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
        traceback.print_exc()
        return JsonResponse(BaseJsonResponse("登录失败", "").error())

    return JsonResponse(BaseJsonResponse("登录成功", {"token":token, "id":user.id}).info())


def register(req):
    """
        用户注册
    :param req:
    :return:
    """
    phone = req.GET.get("phone", "")
    password = req.GET.get("password", "")
    code = req.GET.get("code", "")
    try:
        print("code:", cache.get("wephoto-phone-"+phone), code)
        if not cache.get("wephoto-phone-"+phone) or int(cache.get("wephoto-phone-"+phone)) != int(code):
            return JsonResponse(BaseJsonResponse("验证码错误", {}).error())
        user = User(name=phone, phone=phone, password=password)
        sec_str = str(user.id)+"-"+user.password+settings.SECRET_KEY
        token = hashlib.sha1(sec_str.encode("utf-8")).hexdigest()
        user.token = token
        user.save()
        tokens[token] = user.id
        return JsonResponse(BaseJsonResponse("注册成功", {"token":token, "id":user.id}).info())
    except:
        traceback.print_exc()
        return JsonResponse(BaseJsonResponse("注册失败", "").error())


# 上传upload image对象
def upload_image(req):
    # print(req)
    if req.method == "POST":    # 请求方法为POST时，进行处理
        myFile =req.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        tag = req.POST.get("tag", "")
        # print(req.FILES)
        if not myFile:
            return HttpResponse("no files for upload!")
        file_ext = os.path.splitext(myFile.name)[1]
        filename = str(time.time())+file_ext
        filepath = os.path.join("/tmp/", filename)
        with open(filepath, "wb") as f:
            for t in myFile.chunks():
                f.write(t)
        bucket.put_object_from_file(filename, filepath)
        os.remove(filepath)

        u = UploadedImage(file="http://16mm.oss-cn-hangzhou.aliyuncs.com/"+filename, tag=tag)
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
    # print(req.META)
    if req.META.get('HTTP_X_FORWARDED_FOR'):
        ip = req.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = req.META['REMOTE_ADDR']
    print(ip)
    # 同一个ip, 一分钟最多20次
    count = cache.get("wephoto-ip-"+ip)
    print("count ip:"+str(count))
    if count is None:
        cache.set("wephoto-ip-"+ip, 1)
        cache.expire("wephoto-ip-"+ip, 60)
    elif int(count) >= 20:
        print(cache.ttl("wephoto-ip-"+ip))
        return JsonResponse(BaseJsonResponse("please request later", {}).error())
    else:
        t = cache.ttl("wephoto-ip-"+ip)
        print(t)
        cache.set("wephoto-ip-"+ip, int(count)+1)
        cache.expire("wephoto-ip-"+ip, t)

    # 同一个手机号 50秒一次
    if req.method == "POST":
        phone = req.POST.get("phone", None)
        if phone is None:
            return JsonResponse(BaseJsonResponse("please provide phone number", {}).error())
        if cache.get("wephoto-phone-"+phone) is not None and int(cache.ttl("wephoto-phone-"+phone)> 10):
            print(cache.get("wephoto-phone-"+phone), cache.ttl("wephoto-phone-"+phone))
            return JsonResponse(BaseJsonResponse("please request later", {}).error())
        code = str(random.random()).replace('0.', '')[:5]
        cache.set("wephoto-phone-"+phone, code)
        cache.expire("wephoto-phone-"+phone, 300)
        print(code)
        # send_sms()
        params = "{\"code\":\""+code+"\"}"
        r = send_sms(__business_id, str(phone), "16mm", "SMS_150173093", params)
        print(r)
        return JsonResponse(BaseJsonResponse("发送成功", {"sms_response": r.decode("utf-8")}).info())
    return JsonResponse(BaseJsonResponse("ok", {"ip":ip}).info())


def order_count(req):
    user = req.GET.get("user", None)
    photographer = req.GET.get("photographer", None)
    resp = []
    qs = None
    try:
        if user is not None:
            u = User.objects.get(id=user)
            print(u)
            qs = Order.objects.filter(user=u).values('state').annotate(count=Count('id'))
        elif photographer is not None:
            p = User.objects.get(id=photographer)
            qs = Order.objects.filter(photographer=p).values('state').annotate(count=Count('id'))
        print(qs)
    except:
        logger.debug(traceback.format_exc())
    if qs is not None:
        resp = [q for q in qs]
    return JsonResponse(resp, safe=False)


def notify(req):
    try:
        raw_data = req.read()
        xml_obj = xmldom.parseString(raw_data.decode("utf-8"))
        print("raw_data", raw_data, xml_obj)
        logger.debug(raw_data.decode("utf-8"))
        logger.debug(str(xml_obj))
        root = xml_obj.documentElement
        out_trade_no = root.getElementsByTagName("out_trade_no")[0].childNodes[0]
        total_fee = root.getElementsByTagName("total_fee")[0].childNodes[0]
        result_code = root.getElementsByTagName("result_code")[0].childNodes[0]
        print("result code", result_code.nodeValue, total_fee.nodeValue)
        payment = Payment.objects.get(out_trade_no=out_trade_no.nodeValue)
        logger.debug(payment.fee)
        logger.debug(total_fee.nodeValue)
        if payment.state == 0:
            if result_code.nodeValue == "SUCCESS" and float(total_fee.nodeValue)/100.0 == float(payment.fee):
                payment.state = 2
            else:
                payment.msg = "支付订单失败"
                payment.state = 1
            payment.save()

        print(out_trade_no, total_fee, result_code)
        print(out_trade_no.nodeValue, total_fee.nodeValue, result_code.nodeValue)
    except:
        # traceback.print_exc()
        logger.debug(traceback.format_exc())
    xml_data = "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
    return HttpResponse(xml_data, content_type="text/xml")