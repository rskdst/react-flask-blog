#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: interface.py
@time: 2022/11/26 15:52
@brief 响应接口封装
"""
from flask import jsonify

def jsonApi(data,code=200,message="请求成功"):
    return jsonify({'code' :code,'data': data,'message':message})