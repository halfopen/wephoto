# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-05 05:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='昵称')),
                ('username', models.CharField(max_length=1024, verbose_name='用户名')),
                ('password', models.CharField(max_length=1024, verbose_name='密码')),
                ('gender', models.CharField(default='男', max_length=2)),
                ('avator', models.ImageField(blank=True, null=True, upload_to='avator', verbose_name='原图')),
                ('phone', models.CharField(max_length=32)),
                ('qq', models.CharField(max_length=32, null=True)),
                ('wechat', models.CharField(max_length=32, null=True)),
            ],
            options={
                'verbose_name': '普通用户/模特',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(verbose_name='订单类型')),
                ('price', models.FloatField(verbose_name='价格')),
                ('place', models.CharField(max_length=1024, verbose_name='地点')),
                ('model_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wephoto.CommonUser', verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
            },
        ),
        migrations.CreateModel(
            name='OrderEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=5, verbose_name='分数')),
                ('content', models.CharField(max_length=4096)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wephoto.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='昵称')),
                ('username', models.CharField(max_length=1024, verbose_name='用户名')),
                ('password', models.CharField(max_length=1024, verbose_name='密码')),
                ('gender', models.CharField(default='男', max_length=2)),
                ('avator', models.ImageField(blank=True, null=True, upload_to='avator', verbose_name='原图')),
                ('phone', models.CharField(max_length=32)),
                ('qq', models.CharField(max_length=32, null=True)),
                ('wechat', models.CharField(max_length=32, null=True)),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='是否审核通过')),
                ('id_card_1', models.ImageField(upload_to='', verbose_name='正面身份证')),
                ('id_card_2', models.ImageField(upload_to='', verbose_name='反面身份证')),
                ('works', models.CharField(max_length=4096, verbose_name='作品集')),
            ],
            options={
                'verbose_name': '摄影师',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='是否审核通过')),
                ('comment', models.CharField(default='', max_length=4096, verbose_name='审核意见')),
                ('photographer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wephoto.Photographer')),
            ],
            options={
                'verbose_name': '审核记录',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=48, unique=True, verbose_name='标签名')),
                ('count', models.IntegerField(default=0, verbose_name='使用次数')),
            ],
            options={
                'verbose_name': '标签',
            },
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='', verbose_name='图片')),
                ('tag', models.CharField(default='', max_length=1024)),
            ],
            options={
                'verbose_name': '上传的图片',
            },
        ),
        migrations.AddField(
            model_name='photographer',
            name='tags',
            field=models.ManyToManyField(to='wephoto.Tag'),
        ),
        migrations.AddField(
            model_name='order',
            name='photophrapher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wephoto.Photographer', verbose_name='摄影师'),
        ),
    ]
