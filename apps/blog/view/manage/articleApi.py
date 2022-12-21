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
from apps.blog.model import Menu,Role,db
from sqlalchemy import exists,or_
from flask_jwt_extended import jwt_required,get_jwt_identity

from flask_jwt_extended import create_access_token

article = Blueprint('article', __name__, url_prefix='/api/article')

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