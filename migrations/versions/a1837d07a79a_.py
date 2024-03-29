"""empty message

Revision ID: a1837d07a79a
Revises: c2bbe6aaad8a
Create Date: 2021-11-14 09:51:32.636216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1837d07a79a'
down_revision = 'c2bbe6aaad8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_refresh_token',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('refresh_token', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=128), nullable=True),
    sa.Column('expire_in', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('refresh_token')
    )
    op.create_table('auth_token',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=128), nullable=True),
    sa.Column('expire_in', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_auth_token_user_id'), 'auth_token', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_auth_token_user_id'), table_name='auth_token')
    op.drop_table('auth_token')
    op.drop_table('auth_refresh_token')
    # ### end Alembic commands ###
