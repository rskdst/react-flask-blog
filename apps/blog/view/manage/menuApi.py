#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: menuApi.py
@time: 2022/11/26 15:44
@brief 菜单管理api
"""
import base64

from flask import Blueprint, request, abort
from blog.apps.utils.constants import METHODTYPE
from apps.utils.interface import jsonApi
from apps.blog.model.permission import Menu,db

menu = Blueprint('menu', __name__, url_prefix='/api/menu')

# 菜单编辑
@menu.route('/edit',methods=[METHODTYPE.POST])
def edit_menu():
    if request.method == METHODTYPE.GET:
        abort(405)
    data = request.form
    icon = request.files['icon'].read()
    menu_obj = Menu(
        lable=data['lable'],
        pid=data['parent'],
        pname="",
        icon=icon,
        routePath=data['routePath'],
        state=data['state']
    )
    db.session.add(menu_obj)
    db.session.commit()
    return jsonApi([])
