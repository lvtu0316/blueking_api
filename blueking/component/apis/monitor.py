# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsMONITOR(object):
    """Collections of MONITOR APIS"""

    def __init__(self, client):
        self.client = client

        self.get_alarms = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/monitor/get_alarms/',
            description=u'通过筛选条件获取指定告警事件'
        )
        self.alarm_instance = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/monitor/alarm_instance/',
            description=u'返回指定id的告警数据'
        )
        self.list_alarm_instance = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/monitor/list_alarm_instance/',
            description=u'批量筛选告警'
        )
        self.query_data = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/monitor/query_data/',
            description=u'图表数据查询,根据给定的sql表达式查询指定的存储引擎'
        )
        self.list_component_instance = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/monitor/list_component_instance/',
            description=u'批量筛选组件'
        )
        self.component_instance = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/monitor/component_instance/',
            description=u'返回指定组件'
        )
