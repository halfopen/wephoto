# coding: utf-8
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from wephoto.models import *


def create_data():
    tags = Tag.objects.all()
    for i in range(20):
        User(name="摄影师"+str(i), phone=i, password="test", tags=tags, avatar="http://118.25.221.34:8080/media/1540193557.9864199293624_1_thumb.png").save()
    for i in range(21, 30):
        User(name="普通用户"+str(i), phone=i, password="test", tags=tags, avatar="http://118.25.221.34:8080/media/1540193557.9864199293624_1_thumb.png").save()


if __name__ == '__main__':
    create_data()