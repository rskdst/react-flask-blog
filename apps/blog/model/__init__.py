#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: role.py
@time: 2022/12/4 13:05
@brief
"""
import datetime
from apps.utils.db import db
from sqlalchemy import ForeignKey

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

# 菜单列表
class Menu(BaseModel):
    __tablename__ = "menu"
    label = db.Column(db.String(20),unique=True,nullable=False) # 菜单名称
    pid = db.Column(db.Integer) # 父级菜单id
    pname = db.Column(db.String(20)) # 父级菜单名称
    icon = db.Column(db.String(40)) # 图标
    routePath = db.Column(db.String(100),nullable=False) # 路由地址
    componentPath = db.Column(db.String(100),nullable=False) # 组件地址
    weight = db.Column(db.Integer,nullable=False) # 权重
    state = db.Column(db.String(1)) # 是否启用

# 角色
class Role(BaseModel):
    rolename = db.Column(db.String(10),unique=True) # 角色名字


# 用户表
class User(BaseModel):
    username = db.Column(db.String(20),unique=True,nullable=True) # 用户名
    password = db.Column(db.String(20)) # 密码
    phone = db.Column(db.String(11),unique=True,nullable=True) # 手机号
    mail = db.Column(db.String(30),unique=True,nullable=True) # 邮箱
    id_card = db.Column(db.String(18),unique=True,nullable=True) # 身份证号
    state = db.Column(db.Integer,default=1) # 状态
    create_date = db.Column(db.DateTime, default=datetime.datetime.now) # 创建时间
    update_date = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now) # 更新时间
    role_id = db.Column(db.Integer,ForeignKey("role.id"),default=1) # 角色id

    def verify_password(self, password):
        """校验密码"""
        return password == self.password

