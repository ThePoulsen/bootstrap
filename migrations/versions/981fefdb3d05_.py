"""empty message

Revision ID: 981fefdb3d05
Revises: 1ecb44f95600
Create Date: 2017-03-19 16:22:24.539161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '981fefdb3d05'
down_revision = '1ecb44f95600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('causingFactor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    op.create_table('likelihood',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    op.create_table('processArea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    op.create_table('riskArea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    op.create_table('riskType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    op.create_table('valueChainArea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('valueChainArea')
    op.drop_table('riskType')
    op.drop_table('riskArea')
    op.drop_table('processArea')
    op.drop_table('likelihood')
    op.drop_table('causingFactor')
    # ### end Alembic commands ###
