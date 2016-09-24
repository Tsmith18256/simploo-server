"""Add social network relationship

Revision ID: d3ba2c7254eb
Revises: d261aa52ccfc
Create Date: 2016-09-24 15:12:02.056170

"""

# revision identifiers, used by Alembic.
revision = 'd3ba2c7254eb'
down_revision = 'd261aa52ccfc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('social_network_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'social_networks', ['social_network_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'social_network_id')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    ### end Alembic commands ###