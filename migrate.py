#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: liujing
@version: 1.0.0
@file: migrate.py
@time: 2022/11/26 15:25
@brief 数据库迁移
"""
import os
import sys

def init_env_path(_file_):
    package_dir = os.path.join(os.path.dirname(_file_), '../')
    abs_path = os.path.abspath(package_dir)
    if abs_path not in sys.path:
        print(f'Add {abs_path} to python path')
        sys.path.insert(0, abs_path)


init_env_path(__file__)

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from apps import create_app
from apps.blog.model import db


app = create_app()
manage = Manager(app) # 实例化一个Manager对象，用它来管理app
migrate = Migrate(app,db)
manage.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manage.run()
