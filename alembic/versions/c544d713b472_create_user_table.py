"""create user table

Revision ID: c544d713b472
Revises: 
Create Date: 2023-05-18 12:36:20.440624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c544d713b472'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('phoneNumber', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('users')
