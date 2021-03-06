"""empty message

Revision ID: a9a28384e63c
Revises: ac51d27bf5ff
Create Date: 2017-03-22 09:28:56.684000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9a28384e63c'
down_revision = 'ac51d27bf5ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('causingFactor', sa.Column('causingFactorType_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'causingFactor_causingFactorType_uuid_fkey', 'causingFactor', type_='foreignkey')
    op.create_foreign_key(None, 'causingFactor', 'causingFactorType', ['causingFactorType_id'], ['id'])
    op.drop_column('causingFactor', 'causingFactorType_uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('causingFactor', sa.Column('causingFactorType_uuid', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'causingFactor', type_='foreignkey')
    op.create_foreign_key(u'causingFactor_causingFactorType_uuid_fkey', 'causingFactor', 'causingFactorType', ['causingFactorType_uuid'], ['uuid'])
    op.drop_column('causingFactor', 'causingFactorType_id')
    # ### end Alembic commands ###
