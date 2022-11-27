from .api import api
from .manage.menuApi import menu

bps = [api,menu]


def init_blue_print(app):
    for bp in bps:
        app.register_blueprint(bp)
