"""empty message

Revision ID: 19f6cb38ba28
Revises: 
Create Date: 2022-12-10 23:37:34.715625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f6cb38ba28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('department_name', sa.String(length=20), nullable=True, comment='部门名字'),
    sa.Column('pid', sa.Integer(), nullable=True, comment='父级部门id'),
    sa.Column('create_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('department_name')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('label', sa.String(length=20), nullable=False, comment='菜单名称'),
    sa.Column('pid', sa.Integer(), nullable=True, comment='父级菜单id'),
    sa.Column('pname', sa.String(length=20), nullable=True, comment='父级菜单名称'),
    sa.Column('icon', sa.String(length=40), nullable=True, comment='图标'),
    sa.Column('routepath', sa.String(length=100), nullable=False, comment='路由地址'),
    sa.Column('componentpath', sa.String(length=100), nullable=False, comment='组件地址'),
    sa.Column('type', sa.String(length=10), nullable=True, comment='类型'),
    sa.Column('permission', sa.String(length=100), nullable=True, comment='权限标记'),
    sa.Column('weight', sa.Integer(), nullable=False, comment='权重'),
    sa.Column('state', sa.String(length=1), nullable=True, comment='是否启用'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('rolename', sa.String(length=10), nullable=True, comment='角色名字'),
    sa.Column('create_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rolename')
    )
    op.create_table('menu_to_role',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], )
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('username', sa.String(length=20), nullable=True, comment='用户名'),
    sa.Column('password', sa.String(length=20), nullable=True, comment='密码'),
    sa.Column('phone', sa.String(length=11), nullable=True, comment='手机号'),
    sa.Column('mail', sa.String(length=30), nullable=True, comment='邮箱'),
    sa.Column('id_card', sa.String(length=18), nullable=True, comment='身份证号'),
    sa.Column('state', sa.Integer(), server_default='1', nullable=True, comment='状态'),
    sa.Column('create_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
    sa.Column('role_id', sa.Integer(), server_default='1', nullable=False, comment='角色id'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_card'),
    sa.UniqueConstraint('mail'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('menu_to_role')
    op.drop_table('role')
    op.drop_table('menu')
    op.drop_table('department')
    # ### end Alembic commands ###
