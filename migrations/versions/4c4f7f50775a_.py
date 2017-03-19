"""empty message

Revision ID: 4c4f7f50775a
Revises: fda6133d98c7
Create Date: 2017-03-17 11:36:33.621000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4f7f50775a'
down_revision = 'fda6133d98c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('region', sa.Column('uuid', sa.String(), nullable=True))
    op.add_column('subRegion', sa.Column('uuid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subRegion', 'uuid')
    op.drop_column('region', 'uuid')
    # ### end Alembic commands ###