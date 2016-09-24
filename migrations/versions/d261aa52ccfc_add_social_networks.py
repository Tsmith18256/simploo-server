"""Add social networks

Revision ID: d261aa52ccfc
Revises: 01b39c33b171
Create Date: 2016-09-24 15:06:49.069515

"""

# revision identifiers, used by Alembic.
revision = 'd261aa52ccfc'
down_revision = '01b39c33b171'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_networks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=31), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_networks')
    ### end Alembic commands ###