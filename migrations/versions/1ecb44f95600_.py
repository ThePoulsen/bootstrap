"""empty message

Revision ID: 1ecb44f95600
Revises: 55d38b0d83bf
Create Date: 2017-03-19 16:20:54.091207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ecb44f95600'
down_revision = '55d38b0d83bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eventType',
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
    op.create_table('riskResponse',
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
    op.create_table('severity',
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
    op.drop_table('severity')
    op.drop_table('riskResponse')
    op.drop_table('eventType')
    # ### end Alembic commands ###
