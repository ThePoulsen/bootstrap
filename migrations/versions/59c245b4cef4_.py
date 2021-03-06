"""empty message

Revision ID: 59c245b4cef4
Revises: 
Create Date: 2017-03-16 16:07:11.062733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c245b4cef4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('abbr', sa.String(length=10), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('region')
    # ### end Alembic commands ###
