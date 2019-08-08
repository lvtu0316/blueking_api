# -*- coding: utf-8 -*-
import json
from django.utils import timezone
from datetime import date, datetime, timedelta, timezone


def str2localtime(str):
    strlist = str.split('+')
    date_time = datetime.strptime(strlist[0], '%Y-%m-%d %H:%M:%S')
    local_time = date_time + timedelta(hours=8)
    return local_time

def get_current_week():
    """
    获取当前周的 周一及周日 时间
    :return:
    """
    now = date.today()
    monday, tuesday, wednesday, thursday, friday, saturday, sunday,  = now, now,now,now,now,now,now
    one_day = timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    tuesday = monday + one_day
    wednesday = tuesday + one_day
    thursday = wednesday + one_day
    friday = thursday + one_day
    saturday = friday + one_day
    sunday = saturday + one_day
    # 返回当前的一星期的日期
    week = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    return week

