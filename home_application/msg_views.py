# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from blueking.component.shortcuts import get_client_by_user
from blueapps.account.decorators import login_exempt
from django.views.decorators.csrf import csrf_exempt
import logging

@login_exempt
@csrf_exempt
def msg(request):
    alarm_type = request.POST.get('alarm_type')
    logger = logging.getLogger('app')  # 普通日志
    logger.error(alarm_type)
    result = dict()
    result['code'] = 200
    result['message'] = "Success"
    return HttpResponse(json.dumps(result), content_type='application/json')
