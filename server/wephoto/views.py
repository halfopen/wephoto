from django.shortcuts import render
from django.http.response import *
from wephoto.models import *
from django.core.exceptions import *
from server import tokens


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
    username = req.GET.get("username", "")
    password = req.GET.get("password", "")
    user_type = req.GET.get("user_type", 0)

    if True or user_type == 0:
        user = None
        try:
            user = Photographer.objects.get(username=username, password=password)
        except Photographer.DoesNotExist:
            print("用户名，密码错误")
        tokens['1'] = 1
        return JsonResponse(BaseJsonResponse("ok", user).info())