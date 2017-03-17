"""empty message

Revision ID: b504f7580cb3
Revises: c80179aebb49
Create Date: 2017-03-16 17:19:52.776752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b504f7580cb3'
down_revision = 'c80179aebb49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('region', sa.Column('tenant_uuid', sa.String(), nullable=True))
    op.add_column('sub_region', sa.Column('tenant_uuid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sub_region', 'tenant_uuid')
    op.drop_column('region', 'tenant_uuid')
    # ### end Alembic commands ###
