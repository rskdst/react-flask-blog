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
from apps.blog.model import User,Role,db
from sqlalchemy import exists,or_
from flask_jwt_extended import jwt_required

from flask_jwt_extended import create_access_token

role = Blueprint('role', __name__, url_prefix='/api/role')

# 获取菜单列表
@role.route("/role",methods=[METHODTYPE.GET])
@jwt_required()
def get_role():
    role_list = queryToDict(db.session.query(Role).all())
    return jsonApi(role_list)

