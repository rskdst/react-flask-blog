#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: db.py
@time: 2022/11/26 22:30
@brief db
"""

from flask_sqlalchemy import SQLAlchemy
import pymysql
db = SQLAlchemy()
pymysql.install_as_MySQLdb()