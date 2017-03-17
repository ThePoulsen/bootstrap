"""empty message

Revision ID: fda6133d98c7
Revises: b504f7580cb3
Create Date: 2017-03-17 10:57:43.502000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fda6133d98c7'
down_revision = 'b504f7580cb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subRegion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('abbr', sa.String(length=10), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], [u'region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr', 'title', 'tenant_uuid')
    )
    op.drop_table('sub_region')
    op.drop_constraint(u'region_abbr_key', 'region', type_='unique')
    op.drop_constraint(u'region_title_key', 'region', type_='unique')
    op.create_unique_constraint(None, 'region', ['abbr', 'title', 'tenant_uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'region', type_='unique')
    op.create_unique_constraint(u'region_title_key', 'region', ['title'])
    op.create_unique_constraint(u'region_abbr_key', 'region', ['abbr'])
    op.create_table('sub_region',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('abbr', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('region_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tenant_uuid', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['region_id'], [u'region.id'], name=u'sub_region_region_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'sub_region_pkey'),
    sa.UniqueConstraint('abbr', name=u'sub_region_abbr_key'),
    sa.UniqueConstraint('title', name=u'sub_region_title_key')
    )
    op.drop_table('subRegion')
    # ### end Alembic commands ###
