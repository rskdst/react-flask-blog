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

from flask_jwt_extended import create_access_token,jwt_required

user = Blueprint('user', __name__, url_prefix='/api/user')


# 获取用户数据
@user.route("/user",methods=[METHODTYPE.POST])
def get_users():
    user_list = db.session.query(User.id,User.username,User.phone,User.id_card,User.mail,User.state,User.create_date,User.update_date,User.role_id,Role.rolename).filter(User.role_id==Role.id).all()
    user = queryToDict(user_list)
    
    return jsonApi(user)

# 新增用户
@user.route("/register",methods=[METHODTYPE.POST])
def add_user():
    data = request.form
    try:
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
    access_token = create_access_token(identity={"userid":user.id,"username":data.get("username",""),"phone":data.get("phone","")})
    response = make_response(jsonApi({"userid":user.id},200))
    response.headers["token"] = access_token
    response.headers.set("Access-Control-Expose-Headers","token")
    return response

# 为用户分配权限
@user.route("/adduserRole",methods=[METHODTYPE.POST])
@jwt_required()
def add_user_role():
    data = request.form
    
    user_id = data.get("user_id")
    role_id = data.get("role_id")
    res = db.session.query(User).filter(User.id == user_id).update({"role_id":role_id})
    db.session.commit()

    return jsonApi("添加成功")