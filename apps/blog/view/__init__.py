from .api import api
from .manage.menuApi import menu
from .manage.userApi import user

bps = [api,menu,user]


def init_blue_print(app):
    for bp in bps:
        app.register_blueprint(bp)
