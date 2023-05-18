"""create cart table

Revision ID: fc16ec26dabb
Revises: 3e157bfb8c98
Create Date: 2023-05-18 13:22:50.529741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc16ec26dabb'
down_revision = '3e157bfb8c98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('carts',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('rental_period', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=False))
    
    op.create_foreign_key(
        "user_cart_fk",
        "carts",
        "users",
        ["user_id"],
        ["id"]
    )

    op.create_foreign_key(
        "book_cart_fk",
        "carts",
        "books",
        ["book_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint('user_cart_fk','carts')
    op.drop_constraint('book_cart_fk','carts')
    op.drop_table('carts')
