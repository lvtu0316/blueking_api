# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-25 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_biz_id', models.IntegerField(blank=True, null=True, verbose_name='业务id')),
                ('cc_biz_name', models.CharField(default='', max_length=20, verbose_name='业务名称')),
                ('ip', models.CharField(max_length=30, verbose_name='ip')),
                ('alarm_type', models.CharField(choices=[('0', '主机'), ('1', '中间件'), ('2', '数据库')], default='1', max_length=20, verbose_name='报警类型')),
                ('alarm_title', models.CharField(default='', max_length=128, verbose_name='报警标题')),
                ('alarm_content', models.CharField(default='', max_length=128, verbose_name='报警内容')),
                ('alarm_time', models.DateTimeField(verbose_name='报警时间')),
            ],
        ),
    ]
