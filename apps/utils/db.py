#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: db.py
@time: 2022/11/26 22:30
@brief db
"""
import base64
from flask_sqlalchemy import SQLAlchemy
import pymysql
db = SQLAlchemy()
pymysql.install_as_MySQLdb()
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
# 解析处理类
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):

            fields = {}
            for field in  [x for x in dir(obj) if not x.startswith('query') and x != 'metadata' and not x.startswith('_')]:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, bytes):
                        data = base64.b64encode(data)
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

def model_to_dict(result):
    from collections import Iterable
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = []
            for res in result:
                key = res.__dict__.keys()
                value = res.__dict__.values()
                if isinstance(value, bytes):
                    value = str(value, encoding='utf-8')
                tmp.append(dict(zip(key, value)))
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')