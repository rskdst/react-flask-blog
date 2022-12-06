#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: userApi.py
@time: 2022/12/4 13:24
@brief 用户相关api
"""

from flask import Blueprint, request, make_response
from blog.apps.utils.constants import METHODTYPE
from apps.utils.interface import jsonApi
from apps.utils.db import queryToDict
from apps.blog.model import User,Role,db
from sqlalchemy import exists,or_

from flask_jwt_extended import create_access_token

user = Blueprint('user', __name__, url_prefix='/api/user')


# 获取用户数据
@user.route("/user",methods=[METHODTYPE.POST])
def get_users():
    user_list = db.session.query(User,Role.rolename).filter(User.role_id==Role.id).all()
    user = [user[0].to_dict(user[1]) for user in user_list]
    return jsonApi(user)

# 新增用户
@user.route("/register",methods=[METHODTYPE.POST])
def add_user():
    # if request.method == METHODTYPE.GET:
    #     return jsonApi("请求失败",500)
    data = request.form
    try:
        # user = User.query.filter_by(username=data["username"])
        have_user = db.session.query(exists().where( User.username==data.get("username"))).scalar()
        if have_user:
            return jsonApi("用户已存在，请登录",201)
        user = User(
            username=data["username"],
            password=data["password"],
            phone=data["phone"]
        )
        db.session.add(user)
        db.session.commit()
        return jsonApi("注册成功")
    except:
        return jsonApi("注册失败")


# 用户登录
@user.route("/login",methods=[METHODTYPE.POST])
def login():
    data = request.form
    user = User.query.filter(or_(User.username == data.get("username",""), User.phone == data.get("phone",""))).first()
    if not user:
        return jsonApi("用户不存在，请先注册",202)
    if not user.verify_password(data.get("password")):
        return jsonApi("用户名或密码不正确",203)
    access_token = create_access_token(identity={"username":data.get("username",""),"phone":data.get("phone","")})
    response = make_response(jsonApi({"userid":user.id},200))
    response.headers["token"] = access_token
    response.headers.set("Access-Control-Expose-Headers","token")
    return response
