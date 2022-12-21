#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: userApi.py
@time: 2022/12/4 13:24
@brief 角色相关api
"""
from flask import Blueprint, request, make_response
from blog.apps.utils.constants import METHODTYPE
from apps.utils.interface import jsonApi
from apps.utils.db import queryToDict
from apps.blog.model import Menu,Role,db
from sqlalchemy import exists,or_
from flask_jwt_extended import jwt_required,get_jwt_identity

from flask_jwt_extended import create_access_token

role = Blueprint('role', __name__, url_prefix='/api/role')

# 获取菜单列表
@role.route("/role",methods=[METHODTYPE.GET])
@jwt_required()
def get_role():
    role = queryToDict(db.session.query(Role).all())
    return jsonApi(role)

@role.route("/roleList",methods=[METHODTYPE.GET])
@jwt_required()
def get_roleList():
    role_id = request.args.get("id")
    role = db.session.query(Role).filter(Role.id==role_id).first()
    role_list = [x.id for x in role.menus]
    return jsonApi(role_list)

@role.route("/addMenuPermission",methods=[METHODTYPE.POST])
@jwt_required()
def add_menu_permission():
    form = request.form
    role_id = form.get("role_id")
    menu_ids = form.get("menu_ids").split(",")
    role = db.session.query(Role).filter(Role.id==role_id).first()
    menus = db.session.query(Menu).filter(Menu.id.in_(menu_ids)).all()
    for menu_id in role.menus:
        role.menus.remove(menu_id)
    role.menus = menus
    db.session.add(role)
    db.session.commit()
    return jsonApi("添加成功",200)

