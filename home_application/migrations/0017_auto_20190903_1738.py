# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-03 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0016_auto_20190830_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualparameter',
            name='middleware_img',
            field=models.ImageField(upload_to='image/%Y/%m', verbose_name='中间件图标'),
        ),
    ]
