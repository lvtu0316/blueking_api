# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-03 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0017_auto_20190903_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualparameter',
            name='middleware_img',
            field=models.ImageField(upload_to='media/image/%Y/%m', verbose_name='中间件图标'),
        ),
    ]
