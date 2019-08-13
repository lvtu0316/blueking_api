# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from .functions import str2localtime
from blueking.component.shortcuts import get_client_by_user
from blueapps.account.decorators import login_exempt


@login_exempt
def hosts(request):
    """
    查询所有主机列表
    :param request:
    :return:
    """
    username = "admin"
    client = get_client_by_user(username)
    business = client.cc.search_business()
    result = dict()
    host_list = []
    if business['result'] == False:
        result['code'] = 500
        result['message'] = '服务异常'
    else:
        for biz in business['data']['info']:
            kwargs = {'bk_biz_id': biz['bk_biz_id']}
            hosts = client.cc.search_host(kwargs)
            if hosts['code'] == 0 and hosts['data']['count'] > 0:
                for host in hosts['data']['info']:
                    host_list.append({
                        'bk_host_id': host['host']['bk_host_id'],
                        'bk_host_name': host['host']['bk_host_name'],
                        'bk_os_bit': host['host']['bk_os_bit'],
                        'bk_host_innerip': host['host']['bk_host_innerip'],
                        'bk_os_name': host['host']['bk_os_name'],
                        'bk_os_version': host['host']['bk_os_version'],
                        'bk_cpu': host['host']['bk_cpu'],
                        'bk_cpu_mhz': host['host']['bk_cpu_mhz'],
                        'bk_disk': host['host']['bk_disk'],
                        'bk_biz_name': biz['bk_biz_name'],
                        'bk_biz_id': biz['bk_biz_id'],
                    })
                result = dict(data=host_list)

            else:
                result = dict(data=[])
    result['code'] = 200
    result['message'] = 'success'
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_exempt
def usage(request):
    """
    查询业务主机性能数据
    :param request:
        biz_id : 业务ID
    :return:
    """
    username = "admin"
    client = get_client_by_user(username)
    bk_biz_id = request.GET.get('bk_biz_id')
    host = []
    cpu_kwargs = {
        'sql': 'select max(usage) as cpu from ' + str(
            bk_biz_id) + '_system_cpu_detail where time >= "1m" group by ip order by time desc limit 1'
    }
    mem_kwargs = {
        'sql': 'select max(pct_used) as mem from ' + str(
            bk_biz_id) + '_system_mem where time >= "1m" group by ip order by time desc limit 1'
    }
    disk_kwargs = {
        'sql': 'select max(in_use) as disk from ' + str(
            bk_biz_id) + '_system_disk where time >= "1m" group by ip order by time desc limit 1'
    }
    cpu = client.monitor.query_data(cpu_kwargs)
    mem = client.monitor.query_data(mem_kwargs)
    disk = client.monitor.query_data(disk_kwargs)
    if cpu['result'] != False and mem['result'] != False and disk['result'] != False \
            and cpu['code'] == '0' and mem['code'] == '0' and disk['code'] == '0':
        if len(cpu['data']['list']) > 0 and len(mem['data']['list']) > 0 and len(disk['data']['list']):
            host.append({
                'cpu': round(cpu['data']['list'][0]['cpu'], 2),
                'mem': round(mem['data']['list'][0]['mem'], 2),
                'disk': round(disk['data']['list'][0]['disk'], 2),
            })
        else:
            host.append({
                'cpu': 0,
                'mem': 0,
                'disk': 0,
            })

    result = dict(data=host)
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_exempt
def alarms(request):
    """
    获取所有业务主机近5分钟报警信息
    :param request:
    :return:
    """
    username = "admin"
    client = get_client_by_user(username)
    business = client.cc.search_business()
    result = dict()
    alarms = []
    start_time = (datetime.now() - timedelta(minutes=5) - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    if not business['result']:
        result['code'] = 500
        result['message'] = '服务异常'
    else:
        for biz in business['data']['info']:
            kwargs = {
                    'bk_biz_id': biz['bk_biz_id'],
                    'source_time__gte': start_time,
                    'page_size': 10000,
                    'source_time__lte': datetime.now()
                }
            res = client.monitor.get_alarms(kwargs)
            if res['result'] == True and res['data']['total'] > 0:
                for alarm in res['data']['result']:
                    alarms.append({
                        'title': alarm['alarm_content']['title'],
                        'content': alarm['alarm_content']['content'],
                        'ip': alarm['ip'],
                        'bk_biz_id': alarm['bk_biz_id'],
                        'bk_biz_name': alarm['alarm_content']['cc_biz_name'],
                        'source_time': str2localtime(alarm['source_time']),
                    })
        result['data'] = alarms
        result['code'] = 200
        result['message'] = 'success'
    return HttpResponse(json.dumps(result), content_type='application/json')



