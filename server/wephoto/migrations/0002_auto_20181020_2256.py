# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-20 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wephoto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='_', max_length=4096, null=True, verbose_name='令牌'),
        ),
    ]
