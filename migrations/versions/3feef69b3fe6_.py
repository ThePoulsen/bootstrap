"""empty message

Revision ID: 3feef69b3fe6
Revises: a92014e14726
Create Date: 2017-03-21 11:05:11.424000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3feef69b3fe6'
down_revision = 'a92014e14726'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deliveryPoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=False),
    sa.Column('createdBy', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('valueChainStepType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=False),
    sa.Column('createdBy', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tenant_uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('valueChainStepType')
    op.drop_table('deliveryPoint')
    # ### end Alembic commands ###