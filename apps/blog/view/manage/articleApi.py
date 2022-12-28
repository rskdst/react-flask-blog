#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: liujing
# @version: 1.0.0
# @file: articleApi.py
# @time: 2022/12/20 20:54 
# @brief:

import os
import uuid
from flask import Blueprint, request, make_response,current_app,Response,send_file
from blog.apps.utils.constants import METHODTYPE
from apps.utils.interface import jsonApi
from apps.utils.db import queryToDict
from apps.blog.model import Article,ArticleCategory,db,User
from sqlalchemy import insert,or_
from flask_jwt_extended import jwt_required,get_jwt_identity

from flask_jwt_extended import create_access_token

article = Blueprint('article', __name__, url_prefix='/api/article')



# 保存文章
@article.route("/save",methods=[METHODTYPE.POST])
@jwt_required()
def save():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    form = request.form.to_dict()
    article = Article(
        title = form.get("title"),
        content = form.get("content"),
        cover_type = form.get("cover_type"),
        cover_pictrue = form.get("cover_pictrue"),
        abstract = form.get("abstract"),
        article_type = form.get("article_type"),
        original_link = form.get("original_link"),
        pulish_type = form.get("pulish_type"),
        content_level = form.get("content_level"),
        tags = form.get("tags[]"),
        user_id=userid
    )
    categorys = form.get("category[]").split(",")
    category_objs = db.session.query(ArticleCategory).filter(ArticleCategory.id.in_(categorys)).all()
    article.categorys = category_objs
    db.session.add(article)
    db.session.commit()
    return jsonApi("保存成功")

# 获取文章数据
@article.route("/list",methods=[METHODTYPE.GET])
@jwt_required()
def get_article_list():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    articles = db.session.query(Article).filter(Article.user_id==userid and Article.state == 1).all()
    all = len(articles)
    enable = len([x for x in articles if x.content_level == 1])
    private = all-enable
    articles = queryToDict(articles)
    return jsonApi({
        "count":{"all":all,"enable":enable,"private":private},
        "list":articles
    })


# 添加专栏
@article.route("/addCategory",methods=[METHODTYPE.POST])
@jwt_required()
def add_category():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    form = request.form.to_dict()
    articleCategory = ArticleCategory(
        category_name = form.get("category_name"),
        category_introduction = form.get("category_introduction"),
        category_picture = form.get("category_picture"),
        user_id = userid
    )
    db.session.add(articleCategory)
    db.session.commit()
    return jsonApi("添加成功")

# 获取专栏数据
@article.route("/getCategory",methods=[METHODTYPE.GET])
@jwt_required()
def get_category():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    user = db.session.query(User).filter(User.id==userid).first()
    categorys = queryToDict(user.user_categorys)

    return jsonApi(categorys)

# 文件上传
@article.route("/upload",methods=[METHODTYPE.POST])
@jwt_required()
def upload():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    upload_path = current_app.config.get("UPLOAD_PATH")
    if not os.path.exists(os.path.join(upload_path, str(userid))):
        os.mkdir(os.path.join(upload_path, str(userid)))
    file = request.files["file"]
    filename = str(uuid.uuid4())+"."+file.filename.rsplit(".")[1]
    file.save(os.path.join(upload_path, "{}/{}".format(userid,filename)))
    filepath = "http://"+request.environ.get('HTTP_HOST')+"/api/article/{}/{}".format(userid,filename)
    return jsonApi({"filepath":filepath},200)

# 文件下载
@article.route("/download/<userid>/<filename>",methods=[METHODTYPE.GET])
def download(userid, filename):
    print(userid,filename)
    upload_path = current_app.config.get("UPLOAD_PATH")
    filepath = os.path.join(upload_path, "{}/{}".format(userid.replace("/",""),filename.replace("/","")))
    response = send_file(filepath,as_attachment=True, download_name=filename)
    response.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    return response

# 文件展示
@article.route("/<userid>/<filename>",methods=[METHODTYPE.GET])
def show_file(userid, filename):
    print(userid,filename)
    upload_path = current_app.config.get("UPLOAD_PATH")
    filepath = os.path.join(upload_path, "{}/{}".format(userid.replace("/",""),filename.replace("/","")))
    image_data = open(filepath, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


# 获取文章相关数据
@article.route("/getQueryCriteria",methods=[METHODTYPE.GET])
@jwt_required()
def get_query_criteria():
    jwt_identity = get_jwt_identity()
    userid = jwt_identity["userid"]
    user = db.session.query(User).filter(User.id==userid).first()
    categorys = queryToDict(user.user_categorys)
    date = list(set(x.create_date.year for x in user.articles))
    return jsonApi({"categorys":categorys,"date":date})