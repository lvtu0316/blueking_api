# -*- coding: utf-8 -*-
import json
import operator
from datetime import datetime, timedelta
import numpy as np
from django.http import HttpResponse
from blueking.component.shortcuts import get_client_by_user
from .functions import get_current_week
from blueapps.account.decorators import login_exempt

@login_exempt
def biz_count(request):
    fields = {'percent', 'biz_name', 'count'}
    result = dict
    list = []
    total = 0
    user = 'admin'
    client = get_client_by_user(user)
    bizs = client.cc.search_business()
    for biz in bizs['data']['info']:
        kwargs = {'bk_biz_id': biz['bk_biz_id'],
                  'source_time__gte': '2019-07-01 00:00:00',
                  'source_time__lte': datetime.now()
                  }
        alarm = client.monitor.get_alarms(kwargs)
        if alarm['code'] == '0':
            list.append({
                'biz_name': biz['bk_biz_name'],
                'percent': alarm['data']['total']
            })
            total += alarm['data']['total']

    key = 0
    for one in list:
        list[key]['percent'] = round(one['percent']/total*100,2)
        key += 1
    list.sort(key=lambda k: (k.get('percent', 0)), reverse=True)
    result = dict(data=list)
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_exempt
def type_count(request):
    sys_type = 'proc_port,proc,load,base,cpu,mem,net,disk,system_env,base_alarm,gse_custom_event,proc_port,custom,keyword,process,selfscript'
    mid_type = 'nginx,tomcat,apache,ad,ceph,consul,iis,weblogic,zookeeper'
    database_type = 'mysql,oracle,memcache,mongodb,mssql,elastic,rabbitmq,redis'
    user = 'admin'
    client = get_client_by_user(user)
    bizs = client.cc.search_business()
    sys_sum = 0
    mid_sum = 0
    database_sum = 0
    for biz in bizs['data']['info']:
        kwargs = {'bk_biz_id': biz['bk_biz_id'],
                  'source_time__gte': '2019-07-01 00:00:00',
                  'page_size': 10000,
                  'source_time__lte': datetime.now()
                  }
        #服务器数据
        kwargs.update(alarm_type__in=sys_type)
        alarms = client.monitor.get_alarms(kwargs)
        if alarms['code'] == '0':
            sys_count = alarms['data']['total']
            sys_sum += sys_count
        #中间件
        kwargs.update(alarm_type__in=mid_type)
        alarms = client.monitor.get_alarms(kwargs)
        if alarms['code'] == '0':
            mid_count = alarms['data']['total']
            mid_sum += mid_count
        # 中间件
        kwargs.update(alarm_type__in=database_type)
        alarms = client.monitor.get_alarms(kwargs)
        if alarms['code'] == '0':
            database_count = alarms['data']['total']
            database_sum += database_count

    total = sys_sum + mid_sum + database_sum
    data = [
        {
            'type_name': '服务器',
            'percent': round(sys_sum/total*100, 2),
            'count': sys_sum,
        },
        {
            'type_name': '中间件',
            'percent': round(mid_sum/total*100, 2),
            'count' : mid_sum,
        },
        {
            'type_name': '数据库',
            'percent': round(database_sum/total*100, 2),
            'count': database_sum,
        }
    ]
    result = dict(data=data)
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_exempt
def week_date(request):
    """
    查询每周数据
    :param request:
    :return:
    """
    type = int(request.GET.get('type'))
    alarmtype = []
    if type == 1: #服务器
        alarmtype = 'proc_port,proc,load,base,cpu,mem,net,disk,system_env,base_alarm,gse_custom_event,proc_port,custom,keyword,process,selfscript'
    if type == 2: #中间件
        alarmtype = 'nginx,tomcat,apache,ad,ceph,consul,iis,weblogic,zookeeper'
    if type == 3: #数据库
        alarmtype = 'mysql,oracle,memcache,mongodb,mssql,elastic,rabbitmq,redis'
    user = 'admin'
    client = get_client_by_user(user)
    week_list = get_current_week()
    result = dict()
    list = []
    list_sum = [0, 0, 0, 0, 0, 0, 0]
    i = 0
    bizs = client.cc.search_business()
    sys_sum = 0
    mid_sum = 0
    database_sum = 0
    names = locals()
    for biz in bizs['data']['info']:
        names['list_%s' % biz['bk_biz_id']] = []
        for day in week_list:
            kwargs = {'bk_biz_id': biz['bk_biz_id'],
                      'source_time__gte': datetime.strptime(str(day), "%Y-%m-%d") + timedelta(hours=-8),
                      'source_time__lte': datetime.strptime(str(day + timedelta(1)), "%Y-%m-%d") + timedelta(hours=-8),
                      'alarm_type__in': alarmtype
                      }
            alarm = client.monitor.get_alarms(kwargs)
            if alarm['code'] == '0':
                names['list_%s'%biz['bk_biz_id']].append(alarm['data']['total'])
        list_sum = np.sum([list_sum, names['list_%s'%biz['bk_biz_id']]], axis = 0)
    result['data'] = list_sum.tolist()
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')
    # def get_query_data(request):

@login_exempt
def get_data(request):
    """
    获取业务下cpu,内存
    :param request:
    :return:
    """
    type = request.GET.get('type')
    user = 'admin'
    client = get_client_by_user(user)
    bizs = client.cc.search_business()
    business = []
    for biz in bizs['data']['info'] :
        if biz['bk_biz_id'] == 2:
            continue
        cpu_kwargs = {
            'sql' : 'select usage as cpu from ' +str(biz['bk_biz_id'])+ '_system_cpu_detail order by time desc limit 1'
        }
        mem_kwargs = {
            'sql': 'select pct_used as mem from ' + str(
                biz['bk_biz_id']) + '_system_mem  order by time desc limit 1'
        }
        disk_kwargs = {
            'sql': 'select max(in_use) as disk from ' + str(
                biz['bk_biz_id']) + '_system_disk  order by time desc limit 1'
        }
        cpu = client.monitor.query_data(cpu_kwargs)
        mem = client.monitor.query_data(mem_kwargs)
        disk = client.monitor.query_data(disk_kwargs)
        if cpu['result'] != False and mem['result'] != False and disk['result'] != False\
                and cpu['code'] == '0' and mem['code'] == '0' and disk['code'] == '0':
            if len(cpu['data']['list']) > 0 and len(mem['data']['list']) > 0 and len(disk['data']['list']):
                business.append({
                    'biz_name' : biz['bk_biz_name'],
                    'cpu' : round(cpu['data']['list'][0]['cpu'], 2),
                    'mem' : round(mem['data']['list'][0]['mem'], 2),
                    'disk' : round(disk['data']['list'][0]['disk'], 2),
                })
            else:
                business.append({
                    'biz_name': biz['bk_biz_name'],
                    'cpu': 0,
                    'mem': 0,
                    'disk':0,
                })
                result = dict()

        else:
            break
    if type:
        business.sort(key=lambda k: (k.get(type, 0)), reverse=True)
    else:
        #排序 先排CPU，CPU相同排mem，都相同排disk
        business.sort(key=lambda k: (k.get('cpu', 0), k.get('mem', 0),k.get('disk', 0)), reverse=True)
    result['data'] = business
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_exempt
def disk_use(request):
    """
    获取业务下磁盘使用
    :param request:
    :return:
    """
    user = 'admin'
    client = get_client_by_user(user)
    bizs = client.cc.search_business()
    business = []
    for biz in bizs['data']['info']:
        if biz['bk_biz_id'] == 2:
            continue
        kwargs = {
            'sql': 'select max(in_use) as disk from ' + str(
                biz['bk_biz_id']) + '_system_disk order by time desc limit 1'
        }
        disk = client.monitor.query_data(kwargs)
        if disk['result'] != False and disk['code'] == '0':
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
        else:
            break
    result = dict()
    fun = operator.attrgetter('disk_use')
    business.sort(key = lambda x:x["disk_use"], reverse=True)
    result['data'] = business[0:3]
    result['code'] = 200
    result['message'] = "Success"

    return HttpResponse(json.dumps(result), content_type='application/json')

@login_exempt
def char_data(request):
    """
    图表数据
    :param request:
    :return:
    """

    type = int(request.GET.get('type'))
    biz_id = request.GET.get('id')
    if biz_id is None or biz_id == '':
        biz_id = 2
    data_list = []
    if type == 1:
        kwargs = {
            'sql': 'select max(usage) as usage from ' + str(biz_id) + '_system_cpu_detail where time >= "1h" '
                                                                 'group by ip,minute10 order by time desc limit 10'
        }
    if type == 2:
        kwargs = {
            'sql': 'select max(pct_used) as usage from ' + str(biz_id) + '_system_mem where time >= "1h"'
                                                                    ' group by ip,minute10 order by time desc limit 10'
        }
    if type == 3:
        kwargs = {
            'sql': 'select max(in_use) as usage from ' + str(biz_id) + '_system_disk where time >= "1h" '
                   'group by ip,minute10 order by time desc limit 10'
        }
    user = 'admin'
    client = get_client_by_user(user)
    date_list = client.monitor.query_data(kwargs)
    datalist = []
    datelist = []
    if date_list['code'] == '0' and date_list['result'] != False:
        for date in date_list['data']['list']:
            datelist.append(datetime.fromtimestamp(date['time']/1000).strftime('%H:%M'))
            if date['usage'] is None:
                datalist.append(0)
            else:
                datalist.append( round(date['usage'],2))
        result = dict(data={
            'data_list':datalist,
            'date_list':datelist
        })

        result['code'] = 200
        result['message'] = "Success"
    else:
        result = dict()
        result['code'] = 500
        result['message'] = "数据获取异常"
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_exempt
def get_crux(request):
    """
    获取CPU使用最大业务id
    :param request:
    :return:
    """
    user = 'admin'
    client = get_client_by_user(user)
    bizs = client.cc.search_business()
    business = []
    for biz in bizs['data']['info']:
        cpu_kwargs = {
            'sql' : 'select max(usage) as cpu from ' +str(biz['bk_biz_id'])+ '_system_cpu_detail where time >= "1m" group by ip order by time desc limit 1'
        }

        cpu = client.monitor.query_data(cpu_kwargs)
        if cpu['result'] != False and cpu['code'] == '0':
            if len(cpu['data']['list']) > 0:
                business.append({
                    'biz_id': biz['bk_biz_id'],
                    'biz_name': biz['bk_biz_name'],
                    'cpu': round(cpu['data']['list'][0]['cpu'], 2),
                })
            else:
                business.append({
                    'biz_id': biz['bk_biz_id'],
                    'biz_name': biz['bk_biz_name'],
                    'cpu': 0,
                })
                result = dict()

        else:
            break
    business.sort(key=lambda k: (k.get('cpu', 0)), reverse=True)
    result['data'] = business[0]
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_exempt
def get_proc(request):
    """
    获取进程使用资源情况
    :param request:
    :return:
    """
    user = 'admin'
    client = get_client_by_user(user)
    biz_id = 3
    para = {'bk_biz_id': biz_id}
    host = client.cc.search_host(para)

    kwargs = {
                'sql' : 'select cpu_usage_pct,mem_usage_pct,mem_res,mem_virt,fd_num from '+str(biz_id)+'_system_proc  group by proc_name order by time desc limit 1'
    }
    res = client.monitor.query_data(kwargs)
    data = dict(list=res['data']['list'])
    data['host'] = host['data']['info'][0]['host']['bk_host_innerip']
    if res['result'] != False and res['code'] == '0':
        if len(res['data']['list']) > 0:
            result=dict(data=data)
            result['code'] = 200
            result['message'] = "Success"

        else:
            result = dict()
            result['code'] = 500
            result['message'] = "fail"

    return HttpResponse(json.dumps(result), content_type='application/json')
