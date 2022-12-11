
from .manage.menuApi import menu
from .manage.userApi import user
from .manage.roleApi import role

bps = [menu,user,role]


def init_blue_print(app):
    for bp in bps:
        app.register_blueprint(bp)
