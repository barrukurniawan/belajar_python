"""empty message

Revision ID: a1438e58beb3
Revises: 4d9c84f56d1f
Create Date: 2021-09-27 07:14:10.886535

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a1438e58beb3'
down_revision = '4d9c84f56d1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_name', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_user_name', 'user', ['name'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    # ### end Alembic commands ###
