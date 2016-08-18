"""添加用户评论表

Revision ID: 67e9fe07faa8
Revises: f78818458b3b
Create Date: 2016-08-19 00:38:06.897537

"""

# revision identifiers, used by Alembic.
revision = '67e9fe07faa8'
down_revision = 'f78818458b3b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('disabled', sa.Boolean(), nullable=True))
    op.drop_column('comments', 'disable')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('disable', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('comments', 'disabled')
    ### end Alembic commands ###
