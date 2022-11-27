import os
from flask import Flask
from .blog import init_blue_print
from .utils import config_log
from blog.config import config

from apps.utils.db import db


def create_app():
    config_log()
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config.get(env))
    init_blue_print(app)
    db.init_app(app)

    return app
