"""empty message

Revision ID: 115386638ad5
Revises: 297851713137
Create Date: 2022-05-26 19:45:42.146658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '115386638ad5'
down_revision = '297851713137'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('swans', sa.Column('birthday', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('swans', 'birthday')
    # ### end Alembic commands ###
