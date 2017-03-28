"""empty message

Revision ID: df4144ce98e9
Revises: eed135efce5b
Create Date: 2017-03-28 13:49:04.070000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df4144ce98e9'
down_revision = 'eed135efce5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('impact', 'desc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('impact', sa.Column('desc', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
