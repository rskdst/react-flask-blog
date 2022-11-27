# 权限模块

from apps.utils.db import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

# 菜单列表
class Menu(BaseModel):
    __tablename__ = "menu"
    lable = db.Column(db.String(20)) # 菜单名称
    pid = db.Column(db.Integer) # 父级菜单id
    pname = db.Column(db.String(20)) # 父级菜单名称
    icon = db.Column(db.LargeBinary) # 图标
    routePath = db.Column(db.String(100)) # 路由地址
    state = db.Column(db.String(1)) # 是否启用

