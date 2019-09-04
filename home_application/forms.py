# -*- coding: UTF-8 -*-

import re
from django import forms
from .models import VisualConf, VisualParameter


class VisualConfForm(forms.ModelForm):

    kwargs = forms.CharField(required=False)
    biz_id = forms.IntegerField(required=False)
    biz_name = forms.CharField(required=False)
    class Meta:
        model = VisualConf
        fields = "__all__"

        error_messages = {
            "page_num": {"required": "请输入页面编号"},
            "modular_num": {"required": "请输入模块编号"},
            "modular_name": {"required": "请输入模块名"},
            "api": {"required": "请输入接口地址"},
        }


class ParameterConfForm(forms.ModelForm):

    class Meta:
        model = VisualParameter
        fields = '__all__'

        error_messages = {
            "middleware": {"required": "请输入中间件名称"},
            "middleware_img": {"required": "请选择中间件图标"},
        }


