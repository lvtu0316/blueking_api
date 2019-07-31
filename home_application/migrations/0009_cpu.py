# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-31 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0008_auto_20190726_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.FloatField(verbose_name='cpu 使用率')),
                ('ip', models.CharField(max_length=20, verbose_name='IP')),
                ('biz_id', models.IntegerField(verbose_name='业务ID')),
                ('biz_name', models.CharField(max_length=20, verbose_name='业务名称')),
                ('time', models.IntegerField(verbose_name='时间')),
            ],
        ),
    ]
