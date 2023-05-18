"""create rental history table

Revision ID: 1db5d214d0de
Revises: fc16ec26dabb
Create Date: 2023-05-18 13:28:25.654953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1db5d214d0de'
down_revision = 'fc16ec26dabb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('rental_histories',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('amount', sa.Double(), nullable=False),
                    sa.Column('status', sa.Boolean(), nullable=False,default=True),
                    sa.Column('rented_on', sa.TIMESTAMP(timezone=True), nullable=False,default="now()"),
                    sa.Column('rental_period', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False))
    
    op.create_foreign_key(
        "user_history_fk",
        "rental_histories",
        "users",
        ["user_id"],
        ["id"]
    )

    op.create_foreign_key(
        "user_book_fk",
        "rental_histories",
        "books",
        ["book_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint('user_history_fk','rental_histories')
    op.drop_constraint('user_book_fk','rental_histories')
    op.drop_table('rental_histories')
