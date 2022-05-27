"""empty message

Revision ID: 9c0390f84024
Revises: d3a63190bf46
Create Date: 2022-05-26 09:04:22.270069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c0390f84024'
down_revision = 'd3a63190bf46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('api_token', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'api_token')
    # ### end Alembic commands ###
