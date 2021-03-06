"""empty message

Revision ID: faac5ec77dbd
Revises: 458967b8340d
Create Date: 2017-03-20 09:52:11.660292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faac5ec77dbd'
down_revision = '458967b8340d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(), nullable=False))
    op.drop_column('user', 'roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('roles', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
