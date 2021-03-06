# -*- coding: utf-8 -*-
"""testapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.static import serve
from config import MEDIA_ROOT
from home_application import views, api_views, visualization_views, msg_views

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^$', views.home, name="home"),
    url(r'^conf$', views.conf, name="conf-list-view"),
    url(r'^conf/list$', views.ConfListView.as_view(), name="conf-list-data"),
    url(r'^conf/detail$', views.ConfDetailView.as_view(), name="conf-detail"),
    url(r'^conf/delete$', views.ConfDeleteView.as_view(), name="conf-delete"),
    url(r'^parameter$', views.parameter, name="parameter-list-view"),
    url(r'^parameter/list$', views.ParameterListView.as_view(), name="parameter-list-data"),
    url(r'^parameter/detail$', views.ParameterDetailView.as_view(), name="parameter-detail"),
    url(r'^parameter/delete$', views.ParameterDeleteView.as_view(), name="parameter-delete"),
    url(r'^parameter/upload$', views.UploadImageView.as_view(), name="parameter-upload"),
    url(r'^getimg$', views.getimg, name="api-getimg"),

    url(r'business$', views.getbusiness, name='api-getbuiness'),
    url(r'business/hosts$', views.get_business_host, name="api-get-business-host"),
    url(r'business/alarms$', views.get_alarms, name="api-get-business-alarms"),
    url(r'typecount$', views.type_alarm_count, name="api-type-alarm-count"),
    url(r'total_count$', views.total_count, name="api-total-count"),
    url(r'biz_count$', api_views.biz_count, name="api-biz-count"),
    url(r'type_count$', api_views.type_count, name="api-type-count"),
    url(r'week_data$', api_views.week_date, name="api-week-data"),
    url(r'get_data$', api_views.get_data, name="get-data"),
    url(r'disk_use$', api_views.disk_use, name="disk-use"),
    url(r'cpu_db$', views.cpu_db, name="cpu-db"),
    url(r'mem_db$', views.mem_db, name="mem-db"),
    url(r'disk_db$', views.disk_db, name="disk-db"),
    url(r'char_data$', api_views.char_data, name="char-data"),
    url(r'get_crux$', api_views.get_crux, name="get_crux"),
    url(r'get_proc$', api_views.get_proc, name="get_proc"),

    #3D 可视化
    url(r'hosts$', visualization_views.hosts, name="hosts"),
    url(r'usage$', visualization_views.usage, name="usage"),
    url(r'alarms$', visualization_views.alarms, name="alarms"),


    #消息测试
    url(r'msg$', msg_views.msg, name="msg")

]
