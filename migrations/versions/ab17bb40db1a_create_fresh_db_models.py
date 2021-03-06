"""Create fresh db models

Revision ID: ab17bb40db1a
Revises: 
Create Date: 2021-06-10 22:06:59.260108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab17bb40db1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pincodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pincode', sa.Integer(), nullable=False),
    sa.Column('sub_18_last_mail_sent_on', sa.DateTime(), nullable=True),
    sa.Column('sub_45_last_mail_sent_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pincode'),
    sa.UniqueConstraint('pincode')
    )
    op.create_table('preference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub_18', sa.Boolean(), nullable=False),
    sa.Column('sub_45', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('pincode_id', sa.Integer(), nullable=False),
    sa.Column('preference_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pincode_id'], ['pincodes.id'], ),
    sa.ForeignKeyConstraint(['preference_id'], ['preference.id'], ),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subscriber_id', 'pincode_id', 'preference_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    op.drop_table('users')
    op.drop_table('preference')
    op.drop_table('pincodes')
    # ### end Alembic commands ###
