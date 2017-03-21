"""empty message

Revision ID: 538606942902
Revises: b6f3f1bd38ef
Create Date: 2017-03-20 09:33:15.071592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '538606942902'
down_revision = 'b6f3f1bd38ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    # ### end Alembic commands ###