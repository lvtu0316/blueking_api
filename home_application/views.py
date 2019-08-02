# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from blueking.component.shortcuts import get_client_by_request
from blueking.component.shortcuts import get_client_by_user
from .functions import str2localtime, get_current_week
from .models import Alarm, TypeCount, Option, BizCount, CPU, Mem, Disk

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')


def getbusiness(request):
    """
    查询所有业务
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    result = client.cc.search_business()
    return HttpResponse(json.dumps(result), content_type='application/json')


def get_business_host(request):
    """
    查询业务下主机
    :method POST
    :param request:
    :return:
    """
    user = 'admin'
    client = get_client_by_user(user)
    biz_id = request.GET.get('biz_id')
    print(biz_id)
    # 参
    kwargs = {'bk_biz_id': biz_id}
    result = client.cc.search_host(kwargs)
    print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')


def get_alarms(request):
    """
    通过筛选条件获取指定告警事件
    :method: GET
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    biz_id = request.GET.get('biz_id')
    source_time__gte = '2019-07-01 00:00:00'
    source_time__lte = datetime.now()
    # 参数
    kwargs = {'bk_biz_id': biz_id,
              'source_time__gte': source_time__gte,
              'page_size':10000,
              'source_time__lte': source_time__lte
              }
    result = client.monitor.get_alarms(kwargs)
    if result['code'] == '0':
        for data in result['data']['result']:
            # print(data['status'])
            dic = {'bk_biz_id': data['bk_biz_id'],
                   'cc_biz_name': data['alarm_content']['cc_biz_name'],
                   'ip': data['ip'],
                   'alarm_type': data['alarm_type'],
                   'alarm_title': data['alarm_content']['title'],
                   'alarm_content': data['alarm_content']['content'],
                   'alarm_time': str2localtime(data['source_time'])
                   }
            Alarm.objects.create(**dic)
    return HttpResponse(json.dumps(result), content_type='application/json')


def type_alarm_count(request):
    """
    统计数量并判断报警所属类型，存入表 type_count
    :param request:
    :return:
    """
    total = int(Option.objects.get(name='total_count').value)
    q1 = Q()
    q1.connector = 'OR'  # 连接方式
    # base(基础)、cpu(CPU)、mem(内存)、net(网络)、disk(磁盘)、system_env(系统)、
    # base_alarm(事件)、gse_custom_event(字符型)、proc_port(进程端口)、
    # custom(自定义)、keyword(关键字)、process(进程)、selfscript(脚本)、
    # uptimecheck(服务拨测)、apache、mysql、nginx、redis、tomcat、ad、ceph、
    # consul、elastic、exchange2010、haproxy、iis、jmx、kafka、memcache、
    # mongodb、mssql、oracle、rabbitmq、weblogic、zookeeper
    # 等
    q1.children.append(('alarm_type', 'proc_port'))
    q1.children.append(('alarm_type', 'proc'))
    q1.children.append(('alarm_type', 'load'))
    q1.children.append(('alarm_type', 'base'))
    q1.children.append(('alarm_type', 'cpu'))
    q1.children.append(('alarm_type', 'mem'))
    q1.children.append(('alarm_type', 'net'))
    q1.children.append(('alarm_type', 'process'))
    q1.children.append(('alarm_type', 'selfscript'))
    q1.children.append(('alarm_type', 'disk'))
    q1.children.append(('alarm_type', 'system_env'))
    q1.children.append(('alarm_type', 'base_alarm'))
    q1.children.append(('alarm_type', 'gse_custom_event'))
    q1.children.append(('alarm_type', 'custom'))
    q1.children.append(('alarm_type', 'keyword'))



    count = Alarm.objects.filter(q1).count()
    dic = {
        'type_name': '服务器',
        'count': count,
        'percent': "%.2f%%" % (count/total*100)
    }
    if TypeCount.objects.filter(type_name='服务器').exists() == False:
        TypeCount.objects.create(**dic)
    else:
        TypeCount.objects.filter(type_name='服务器').update(**dic)
    return HttpResponse(count, content_type='application/json')


def total_count(request):
    """
    统计并保存所有业务报警数量
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    result = client.cc.search_business()
    count = 0
    if result['code'] == 0:
        for info in result['data']['info']:
            source_time__gte = '2019-07-01 00:00:00'
            source_time__lte = datetime.now()
            # 参数
            kwargs = {'bk_biz_id': info['bk_biz_id'],
                      'source_time__gte': source_time__gte,
                      'source_time__lte': source_time__lte
                      }
            result = client.monitor.get_alarms(kwargs)
            if result['code'] == '0':
                count = count + result['data']['total']
                percent = "%.2f%%" % (result['data']['total']/count*100)
                biz = {
                    'biz_id': info['bk_biz_id'],
                    'biz_name': info['bk_biz_name'],
                    'count': result['data']['total'],
                    'percent': percent
                }
                if BizCount.objects.filter(biz_id= info['bk_biz_id']).exists() == False:
                    BizCount.objects.create(**biz)
                else:
                    BizCount.objects.filter(biz_id=info['bk_biz_id']).update(count=result['data']['total'], percent=percent)

    if Option.objects.filter(name='total_count').exists() == False:
        dic = {
            'name': 'total_count',
            'value': count,
            'remark': '报警总数量'
        }
        Option.objects.create(**dic)
    else:
        Option.objects.filter(name='total_count').update( value=count)
    return HttpResponse(count, content_type='application/json')


def biz_total_count(request):
    """
    统计各业务报警数量并保存
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    result = client.cc.search_business()
    count = 0
    if result['code'] == 0:
        for info in result['data']['info']:
            source_time__gte = '2019-07-01 00:00:00'
            source_time__lte = datetime.now()
            # 参数
            kwargs = {'bk_biz_id': info['bk_biz_id'],
                      'source_time__gte': source_time__gte,
                      'source_time__lte': source_time__lte
                      }
            result = client.monitor.get_alarms(kwargs)
            if result['code'] == '0':
               count = result['data']['total']
    if Option.objects.filter(name='total_count').exists() == False:
        dic = {
            'name': 'total_count',
            'value': count,
            'remark': '报警总数量'
        }
        Option.objects.create(**dic)
    else:
        Option.objects.filter(name='total_count').update( value=count)
    return HttpResponse(count, content_type='application/json')


def cpu_db(request):
    """
    保存CPU 数据到本地
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    bizs = client.cc.search_business()
    for biz in bizs['data']['info']:
        kwargs = {
            'sql': 'select max(usage) as cpu from ' + str(
                biz['bk_biz_id']) + '_system_cpu_detail where time >= "1m" group by ip order by time desc limit 1'
        }
        cpu = client.monitor.query_data(kwargs)
        if len(cpu['data']['list']) > 0:
            dic = {
                'biz_name': biz['bk_biz_name'],
                'biz_id': biz['bk_biz_id'],
                'cpu': round(cpu['data']['list'][0]['cpu']),
                'ip': cpu['data']['list'][0]['ip'],
                'time': datetime.fromtimestamp(cpu['data']['list'][0]['time']/1000),

            }
            CPU.objects.create(**dic)
    return HttpResponse(True, content_type='application/json')

def mem_db(request):
    """
    保存内存 数据到本地
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    bizs = client.cc.search_business()
    for biz in bizs['data']['info']:
        kwargs = {
            'sql': 'select max(pct_used) as mem from ' + str(
                biz['bk_biz_id']) + '_system_mem where time >= "1m" group by ip order by time desc limit 1'
        }
        mem = client.monitor.query_data(kwargs)
        if len(mem['data']['list']) > 0:
            dic = {
                'biz_name': biz['bk_biz_name'],
                'biz_id': biz['bk_biz_id'],
                'mem': round(mem['data']['list'][0]['mem']),
                'ip': mem['data']['list'][0]['ip'],
                'time': datetime.fromtimestamp(mem['data']['list'][0]['time']/1000),

            }
            Mem.objects.create(**dic)
    return HttpResponse(True, content_type='application/json')

def disk_db(request):
    """
    保存磁盘数据到本地
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    bizs = client.cc.search_business()
    for biz in bizs['data']['info']:
        kwargs = {
            'sql': 'select max(in_use) as disk from ' + str(
                biz['bk_biz_id']) + '_system_disk where time >= "1m" group by ip order by time desc limit 1'
        }
        mem = client.monitor.query_data(kwargs)
        if len(mem['data']['list']) > 0:
            dic = {
                'biz_name': biz['bk_biz_name'],
                'biz_id': biz['bk_biz_id'],
                'disk': round(mem['data']['list'][0]['mem']),
                'ip': mem['data']['list'][0]['ip'],
                'time': datetime.fromtimestamp(mem['data']['list'][0]['time']),

            }
            Disk.objects.create(**dic)
    return HttpResponse(True, content_type='application/json')


