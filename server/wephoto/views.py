# coding: utf-8
from django.shortcuts import render
from django.http.response import *
from wephoto.models import *
from django.core.exceptions import *
import hashlib
from server import tokens


# 一些初始化
tags = Tag.objects.count()
if tags == 0:
    tags_list = ['时尚']

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
    user_type = req.GET.get("user_type", 0)

    if True or user_type == 0:
        user = None
        try:
            user = Photographer.objects.get(username=username, password=password)
            sec_str = str(user.id)+"-"+user.password+settings.SECRET_KEY
            token = hashlib.sha1(sec_str.encode("utf-8")).hexdigest()
            tokens[token] = 1
        except Photographer.DoesNotExist:
            print("用户名，密码错误")

        return JsonResponse(BaseJsonResponse("ok", user).info())


def like(req):
    pass