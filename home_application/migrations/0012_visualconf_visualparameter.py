# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-08-29 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0011_auto_20190731_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisualConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_num', models.IntegerField(verbose_name='页面编号')),
                ('modular_num', models.IntegerField(verbose_name='模块编号')),
                ('modular_name', models.CharField(max_length=20, verbose_name='模块名称')),
                ('biz_name', models.CharField(max_length=20, verbose_name='业务名称')),
            ],
        ),
        migrations.CreateModel(
            name='VisualParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middleware', models.CharField(max_length=20, verbose_name='中间件名称')),
                ('middleware_img', models.CharField(max_length=100, verbose_name='中间件图标')),
                ('parameter', models.CharField(max_length=20, verbose_name='配置参数')),
                ('api', models.CharField(max_length=200, verbose_name='接口地址')),
                ('visualConf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home_application.VisualConf', verbose_name='配置表')),
            ],
        ),
    ]
