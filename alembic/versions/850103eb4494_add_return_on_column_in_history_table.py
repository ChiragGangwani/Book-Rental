"""add return on column in history table

Revision ID: 850103eb4494
Revises: 1db5d214d0de
Create Date: 2023-05-19 16:54:51.886383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '850103eb4494'
down_revision = '1db5d214d0de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('rental_histories',sa.Column('return_on', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('rental_histories','return_on')
