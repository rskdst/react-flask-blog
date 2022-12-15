#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: menuApi.py
@time: 2022/11/26 15:44
@brief 菜单管理api
"""
from flask import Blueprint, request, abort
from blog.apps.utils.constants import METHODTYPE
from apps.utils.interface import jsonApi
from apps.utils.db import queryToDict
from apps.blog.model import db,Menu,Role,User
from flask_jwt_extended import jwt_required,get_jwt_identity

menu = Blueprint('menu', __name__, url_prefix='/api/menu')

# 获取侧边栏菜单列表
@menu.route("/menu",methods=[METHODTYPE.GET])
@jwt_required()
def get_tree_menu():
    identity = get_jwt_identity()
    userid = identity.get("userid")
    user = db.session.query(User).filter(User.id==userid).first()
    # menu_list = queryToDict(user.role.menus)
    menu_list = queryToDict(db.session.query(Menu).all())
    routes = get_trees(menu_list)
    return jsonApi(routes)


# 新增菜单
@menu.route('/addMenu',methods=[METHODTYPE.POST])
@jwt_required()
def add_menu():
    data = request.form
    menu_obj = Menu(
        label=data['label'],
        pid=data['pid'],
        pname=data['pname'],
        icon=data['icon'],
        routepath=data['routepath'],
        componentpath=data['componentpath'],
        type=data['type'],
        permission=data['permission'],
        weight=data["weight"],
        state=data['state']
    )
    db.session.add(menu_obj)
    db.session.commit()

    return jsonApi("添加成功")

# 菜单编辑
@menu.route('/editMenu',methods=[METHODTYPE.POST])
@jwt_required()
def edit_menu():
    data = request.form
    db.session.query(Menu).filter(Menu.id == data["id"]).update(data.to_dict())
    db.session.commit()

    return jsonApi("添加成功")

# 生成树结构
def get_trees(data,key_column='id',parent_column='pid',child_column='children',current_column=None,current_path=None):
    """
    :param data: 数据列表
    :param key_column: 主键字段，默认id
    :param parent_column: 父ID字段名，父ID默认从0开始
    :param child_column: 子列表字典名称
    :param current_column: 当前展开值字段名，若找到展开值增加['open'] = '1'
    :param current_path: 当前展开值
    :return: 树结构
    """
    data_dic = {}
    data = sorted(data,key=lambda x:x['weight'],reverse=True)
    for d in data:
        data_dic[d.get(key_column)] = d  # 以自己的权限主键为键,以新构建的字典为值,构造新的字典

    data_tree_list = []  # 整个数据大列表
    for d_id, d_dic in data_dic.items():
        pid = d_dic.get(parent_column)  # 取每一个字典中的父id
        if not pid:  # 父id=0，就直接加入数据大列表
            data_tree_list.append(d_dic)
        else:  # 父id>0 就加入父id队对应的那个的节点列表
            try:  # 判断异常代表有子节点，增加子节点列表=[]
                data_dic[pid][child_column].append(d_dic)
            except KeyError:
                data_dic[pid][child_column] = []
                data_dic[pid][child_column].append(d_dic)

        # 展开节点
        if current_path:
            if current_path == d_dic.get(current_column):
                d_dic['open'] = '1'
                while pid:
                    data_dic[pid]['open'] = '1'
                    pid = data_dic[pid][parent_column]
    return data_tree_list