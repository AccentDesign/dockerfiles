"""0001_initial

Revision ID: c1b846738469
Revises: 
Create Date: 2019-03-24 20:30:49.227292

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'c1b846738469'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('user_groups',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_groups')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('groups')
    # ### end Alembic commands ###
