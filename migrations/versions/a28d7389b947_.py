"""empty message

Revision ID: a28d7389b947
Revises: 2ef7a934b47f
Create Date: 2017-03-23 15:59:28.059116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a28d7389b947'
down_revision = '2ef7a934b47f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('causingFactor', sa.Column('causingFactorType_uuid', sa.String(), nullable=True))
    op.drop_constraint(u'causingFactor_causingFactorType_id_fkey', 'causingFactor', type_='foreignkey')
    op.create_foreign_key(None, 'causingFactor', 'causingFactorType', ['causingFactorType_uuid'], ['uuid'])
    op.drop_column('causingFactor', 'causingFactorType_id')
    op.add_column('treatment', sa.Column('riskResponse_uuid', sa.String(), nullable=True))
    op.add_column('treatment', sa.Column('treatmentType_uuid', sa.String(), nullable=True))
    op.drop_constraint(u'treatment_riskResponse_id_fkey', 'treatment', type_='foreignkey')
    op.drop_constraint(u'treatment_treatmentType_id_fkey', 'treatment', type_='foreignkey')
    op.create_foreign_key(None, 'treatment', 'treatmentType', ['treatmentType_uuid'], ['uuid'])
    op.create_foreign_key(None, 'treatment', 'riskResponse', ['riskResponse_uuid'], ['uuid'])
    op.drop_column('treatment', 'treatmentType_id')
    op.drop_column('treatment', 'riskResponse_id')
    op.add_column('valueChain', sa.Column('valueChainArea_uuid', sa.String(), nullable=True))
    op.drop_constraint(u'valueChain_valueChainArea_id_fkey', 'valueChain', type_='foreignkey')
    op.create_foreign_key(None, 'valueChain', 'valueChainArea', ['valueChainArea_uuid'], ['uuid'])
    op.drop_column('valueChain', 'valueChainArea_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valueChain', sa.Column('valueChainArea_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'valueChain', type_='foreignkey')
    op.create_foreign_key(u'valueChain_valueChainArea_id_fkey', 'valueChain', 'valueChainArea', ['valueChainArea_id'], ['id'])
    op.drop_column('valueChain', 'valueChainArea_uuid')
    op.add_column('treatment', sa.Column('riskResponse_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('treatment', sa.Column('treatmentType_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'treatment', type_='foreignkey')
    op.drop_constraint(None, 'treatment', type_='foreignkey')
    op.create_foreign_key(u'treatment_treatmentType_id_fkey', 'treatment', 'treatmentType', ['treatmentType_id'], ['id'])
    op.create_foreign_key(u'treatment_riskResponse_id_fkey', 'treatment', 'riskResponse', ['riskResponse_id'], ['id'])
    op.drop_column('treatment', 'treatmentType_uuid')
    op.drop_column('treatment', 'riskResponse_uuid')
    op.add_column('causingFactor', sa.Column('causingFactorType_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'causingFactor', type_='foreignkey')
    op.create_foreign_key(u'causingFactor_causingFactorType_id_fkey', 'causingFactor', 'causingFactorType', ['causingFactorType_id'], ['id'])
    op.drop_column('causingFactor', 'causingFactorType_uuid')
    # ### end Alembic commands ###
