# coding: utf-8

from django.apps import AppConfig

import os

default_app_config = "wephoto.Config"


def get_current_app_name(file):
    return os.path.split(os.path.dirname(file))[-1]


class Config(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"约拍"

