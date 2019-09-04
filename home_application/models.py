# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Alarm(models.Model):
    """
    报警信息
    """
    type = (
        ("0", "主机"),
        ("1", "中间件"),
        ("2", "数据库")

    )
    bk_biz_id = models.IntegerField(blank=True, null=True, verbose_name="业务id")
    cc_biz_name = models.CharField(max_length=20, default='', verbose_name='业务名称')
    ip = models.CharField(max_length=30, verbose_name="ip")
    alarm_type = models.CharField(choices=type, max_length=20, default="1", verbose_name="报警类型")
    alarm_title = models.CharField(max_length=128, default='', verbose_name='报警标题')
    alarm_content = models.CharField(max_length=128, default='', verbose_name='报警内容')
    alarm_time = models.DateTimeField(verbose_name="报警时间")


class TypeCount(models.Model):
    type_name = models.CharField(max_length=5,default='',verbose_name='名称')
    percent = models.CharField(max_length=5,default=0,verbose_name='占比')
    count = models.IntegerField(default=0,verbose_name='报警数量')

class BizCount(models.Model):
    percent = models.CharField(max_length=5,default=0,verbose_name='占比')
    count = models.IntegerField(default=0,verbose_name='报警数量')
    biz_id = models.IntegerField(blank=True, null=True, verbose_name="业务id")
    biz_name = models.CharField(max_length=20, default='', verbose_name='业务名称')


class Option(models.Model):
    name = models.CharField(blank=False, max_length=15, verbose_name="属性名称" )
    value = models.CharField(blank=False, max_length=20, verbose_name="属性值")
    remark = models.CharField(blank=True, max_length=20, null=True, verbose_name="备注")

class CPU(models.Model):
    cpu = models.FloatField(verbose_name="cpu 使用率")
    ip = models.CharField(max_length=20, verbose_name="IP")
    biz_id = models.IntegerField(verbose_name="业务ID")
    biz_name = models.CharField(max_length=20, verbose_name="业务名称")
    time = models.DateTimeField(verbose_name="时间")


class Mem(models.Model):
    mem = models.FloatField(verbose_name="cpu 使用率")
    ip = models.CharField(max_length=20, verbose_name="IP")
    biz_id = models.IntegerField(verbose_name="业务ID")
    biz_name = models.CharField(max_length=20, verbose_name="业务名称")
    time = models.DateTimeField(verbose_name="时间")

class Disk(models.Model):
    disk = models.FloatField(verbose_name="disk 使用率")
    ip = models.CharField(max_length=20, verbose_name="IP")
    biz_id = models.IntegerField(verbose_name="业务ID")
    biz_name = models.CharField(max_length=20, verbose_name="业务名称")
    time = models.DateTimeField(verbose_name="时间")


#可视化配置表
class VisualConf(models.Model):
    page_num = models.IntegerField(verbose_name="页面编号")
    modular_num = models.IntegerField(verbose_name="模块编号")
    modular_name = models.CharField(max_length=20, verbose_name="模块名称")
    biz_name = models.CharField(max_length=20, verbose_name="业务名称", null=True)
    biz_id = models.IntegerField(verbose_name="业务id", null=True)
    api = models.CharField(max_length=200, verbose_name="接口地址")
    kwargs = models.CharField(max_length=200, null=True, verbose_name="参数")


class VisualParameter(models.Model):
    middleware = models.CharField(max_length=20, verbose_name="中间件名称")
    middleware_img = models.ImageField(upload_to="media/image/%Y/%m", max_length=100, verbose_name="中间件图标")

