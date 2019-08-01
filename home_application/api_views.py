# -*- coding: utf-8 -*-
import json
import operator
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from blueking.component.shortcuts import get_client_by_request
from blueking.component.shortcuts import get_client_by_user
from .functions import str2localtime, get_current_week
from .models import Alarm, TypeCount, Option, BizCount, CPU, Mem, Disk


def biz_count(request):
    fields = {'percent', 'biz_name', 'count'}
    result = dict(data=list(BizCount.objects.values(*fields)))
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')

def type_count(request):
    fields = {'percent', 'count', 'type_name'}
    result = dict(data=list(TypeCount.objects.values(*fields)))
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')


def week_date(request):
    """
    查询每周数据
    :param request:
    :return:
    """
    type = request.GET.get('type')

    q1 = Q()
    q1.connector = 'OR'  # 连接方式
    if type == 1: #服务器
        q1.children.append(('alarm_type', 'proc_port'))
        q1.children.append(('alarm_type', 'proc'))
        q1.children.append(('alarm_type', 'load'))
    if type == 2: #中间件
        q1.children.append(('alarm_type', 'nginx'))
        q1.children.append(('alarm_type', 'tomcat'))
    if type == 3: #数据库
        q1.children.append(('alarm_type', 'mysql'))

    week_list = get_current_week()
    result = dict()
    list = []
    i = 0
    for day in week_list:
        list.append(Alarm.objects.filter(Q(alarm_time__year=day.year, alarm_time__month=day.month, alarm_time__day=day.day) & q1).count())
        i += i
    result['data'] = list
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')
    # def get_query_data(request):

def get_data(request):
    """
    获取业务下cpu,内存
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    bizs = client.cc.search_business()
    business = []
    for biz in bizs['data']['info']:
        cpu_kwargs = {
            'sql' : 'select max(usage) as cpu from ' +str(biz['bk_biz_id'])+ '_system_cpu_detail where time >= "1m" group by ip order by time desc limit 1'
        }
        mem_kwargs = {
            'sql': 'select max(pct_used) as mem from ' + str(
                biz['bk_biz_id']) + '_system_mem where time >= "1m" group by ip order by time desc limit 1'
        }
        disk_kwargs = {
            'sql': 'select max(in_use) as disk from ' + str(
                biz['bk_biz_id']) + '_system_disk where time >= "1m" group by ip order by time desc limit 1'
        }
        cpu = client.monitor.query_data(cpu_kwargs)
        mem = client.monitor.query_data(mem_kwargs)
        disk = client.monitor.query_data(disk_kwargs)
        if len(cpu['data']['list']) > 0 and len(mem['data']['list']) > 0 and len(disk['data']['list']):
            business.append({
                'biz_name' : biz['bk_biz_name'],
                'cpu' : round(cpu['data']['list'][0]['cpu'], 2),
                'mem' : round(mem['data']['list'][0]['mem'], 2),
                'disk' : round(disk['data']['list'][0]['mem'], 2),
            })
        else:
            business.append({
                'biz_name': biz['bk_biz_name'],
                'cpu': 0,
                'mem': 0,
                'disk':0,
            })
    result = dict()
    result['data'] = business
    result['code'] = 200
    result['message'] = "Success"

    return HttpResponse(json.dumps(result), content_type='application/json')


def disk_use(request):
    """
    获取业务下磁盘使用
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    bizs = client.cc.search_business()
    business = []
    for biz in bizs['data']['info']:
        kwargs = {
            'sql': 'select max(in_use) as disk from ' + str(
                biz['bk_biz_id']) + '_system_disk where time >= "1m" group by ip order by time desc limit 1'
        }
        disk = client.monitor.query_data(kwargs)
        if len(disk['data']['list']) > 0:
            business.append({
                'biz_name': biz['bk_biz_name'],
                'disk_use': round(disk['data']['list'][0]['disk'], 2),
            })
        else:
            business.append({
                'biz_name': biz['bk_biz_name'],
                'disk_use': 0,
            })
    result = dict()
    fun = operator.attrgetter('disk_use')
    business.sort(key=fun)
    result['data'] = business
    result['code'] = 200
    result['message'] = "Success"

    return HttpResponse(json.dumps(result), content_type='application/json')

def char_data(request):
    """
    图表数据
    :param request:
    :return:
    """

    type = int(request.GET.get('type'))
    data_list = []
    if type == 1:
        data_list = list(CPU.objects.values('cpu').order_by('-time')[0:10])
    if type == 2:
        data_list = list(Mem.objects.values('mem').order_by('-time')[0:10])
    if type == 3:
        data_list = list(Disk.objects.values('disk').order_by('-time')[0:10])
    date_list = Mem.objects.values('time').order_by('-time')[0:10]
    datelist = []
    datalist = []
    for date in date_list:
        datelist.append(date['time'].strftime("%H:%M:%S"))
    for data in data_list:
        datalist.append(data['cpu'])
    result = dict(data={
        'data_list':datalist,
        'date_list':datelist
    })

    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')


