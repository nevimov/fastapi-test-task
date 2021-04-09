"""Add url_count field to User model

Revision ID: 80ab7fd4ca8f
Revises: 38ce38f7cfc7
Create Date: 2021-04-06 21:14:10.006604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80ab7fd4ca8f'
down_revision = '38ce38f7cfc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('url_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'url_count')
    # ### end Alembic commands ###
