import os
from flask import Flask
from .blog import init_blue_print
from .utils import config_log
from blog.config import config
from celery import Celery
from apps.utils.db import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    config_log()
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config.get(env))
    init_blue_print(app)
    db.init_app(app)
    jwt.init_app(app)

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    return app
