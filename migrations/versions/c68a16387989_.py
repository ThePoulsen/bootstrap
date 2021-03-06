"""empty message

Revision ID: c68a16387989
Revises: 433337456820
Create Date: 2017-03-28 14:08:20.372000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c68a16387989'
down_revision = '433337456820'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('risk', sa.Column('impact_uuid', sa.String(), nullable=False))
    op.add_column('risk', sa.Column('probability_uuid', sa.String(), nullable=False))
    op.create_foreign_key(None, 'risk', 'impact', ['impact_uuid'], ['uuid'])
    op.create_foreign_key(None, 'risk', 'probability', ['probability_uuid'], ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'risk', type_='foreignkey')
    op.drop_constraint(None, 'risk', type_='foreignkey')
    op.drop_column('risk', 'probability_uuid')
    op.drop_column('risk', 'impact_uuid')
    # ### end Alembic commands ###
