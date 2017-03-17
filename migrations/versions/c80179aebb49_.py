"""empty message

Revision ID: c80179aebb49
Revises: 59c245b4cef4
Create Date: 2017-03-16 16:11:05.639822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c80179aebb49'
down_revision = '59c245b4cef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('abbr', sa.String(length=10), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], [u'region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sub_region')
    # ### end Alembic commands ###