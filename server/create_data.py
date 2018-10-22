# coding: utf-8
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from wephoto.models import *


def create_data():
    tags = Tag.objects.all()
    User(name="摄影师", phone=1, password="test", tags=tags).save()
    User(name="普通用户", phone=2, password="test", tags=tags).save()


if __name__ == '__main__':
    create_data()