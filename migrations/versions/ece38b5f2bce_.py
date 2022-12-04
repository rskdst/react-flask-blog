"""empty message

Revision ID: ece38b5f2bce
Revises: 95237cdedf51
Create Date: 2022-12-04 13:38:15.892210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece38b5f2bce'
down_revision = '95237cdedf51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'role', ['rolename'])
    op.create_unique_constraint(None, 'user', ['username'])
    op.create_unique_constraint(None, 'user', ['phone'])
    op.create_unique_constraint(None, 'user', ['mail'])
    op.create_unique_constraint(None, 'user', ['id_card'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    # ### end Alembic commands ###