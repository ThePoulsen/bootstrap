"""empty message

Revision ID: 4962da500bf5
Revises: 8b224981bc71
Create Date: 2017-03-19 15:27:39.917700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4962da500bf5'
down_revision = '8b224981bc71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('abbr', sa.String(length=10), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('createdBy', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modifiedBy', sa.String(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], [u'country.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr', 'tenant_uuid'),
    sa.UniqueConstraint('title', 'tenant_uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('zone')
    # ### end Alembic commands ###
