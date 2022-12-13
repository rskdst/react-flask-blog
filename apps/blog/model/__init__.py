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
from sqlalchemy.orm import relationship
from sqlalchemy import Column,String,Integer,text,DateTime,ForeignKey,Table

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True,comment="id")

# 菜单角色表
menu_to_role = Table(
    "menu_to_role",db.metadata,
    Column("menu_id",Integer,ForeignKey("menu.id")),
    Column("role_id",Integer,ForeignKey("role.id")),
)
# 菜单列表
class Menu(BaseModel):
    __tablename__ = "menu"
    label = Column(String(20),unique=True,nullable=False,comment="菜单名称")
    pid = Column(Integer,comment="父级菜单id")
    pname = Column(String(20),comment="父级菜单名称")
    icon = Column(String(40),comment="图标")
    routepath = Column(String(100),nullable=False,comment="路由地址")
    componentpath = Column(String(100),nullable=False,comment="组件地址")
    type = Column(String(10),nullable=True,comment="类型")
    permission = Column(String(100),comment="权限标记")
    weight = Column(Integer,nullable=False,comment="权重")
    state = Column(String(1),comment="是否启用")

    roles = relationship("Role",secondary=menu_to_role,backref="menus")

# 角色
class Role(BaseModel):
    rolename = Column(String(10),unique=True,comment="角色名字")
    # did = Column(Integer,ForeignKey("department.id"),default=1,server_default="1",nullable=False,comment="所属部门")
    create_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'),comment="创建时间")
    update_date = Column(DateTime,  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),comment="更新时间")

    users = relationship("User",backref="role")

# 部门
class Department(BaseModel):
    department_name = Column(String(20),unique=True,comment="部门名字")
    pid = Column(Integer,comment="父级部门id")
    create_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'),comment="创建时间")
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),comment="更新时间")

    # roles = relationship("Role",backref="department")

# 用户表
class User(BaseModel):
    username = Column(String(20),unique=True,nullable=True,comment="用户名")
    password = Column(String(20),comment="密码")
    phone = Column(String(11),unique=True,nullable=True,comment="手机号")
    mail = Column(String(30),unique=True,nullable=True,comment="邮箱")
    id_card = Column(String(18),unique=True,nullable=True,comment="身份证号")
    state = Column(Integer,default=1,server_default="1",comment="状态")
    create_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'),comment="创建时间")
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),comment="更新时间")
    role_id = Column(Integer,ForeignKey("role.id"),default=1,server_default="1",nullable=False,comment="角色id")

    def to_dict(self,rolename):
        return {
            "username":self.username,
            "password":self.password,
            "phone":self.phone,
            "mail":self.mail,
            "id_card":self.id_card,
            "state":self.state,
            "create_date":self.create_date.strftime("%Y-%m-%d %H:%M:%S"),
            "update_date":self.update_date.strftime("%Y-%m-%d %H:%M:%S"),
            "role_id":self.role_id,
            "rolename":rolename,
        }

    def verify_password(self, password):
        """校验密码"""
        return password == self.password

