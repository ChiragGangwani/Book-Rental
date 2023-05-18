"""create review table

Revision ID: 3e157bfb8c98
Revises: 978e531fe8c2
Create Date: 2023-05-18 13:18:22.056862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e157bfb8c98'
down_revision = '978e531fe8c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('reviews',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('review', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=False))
    
    op.create_foreign_key(
        "user_review_fk",
        "reviews",
        "users",
        ["user_id"],
        ["id"]
    )

    op.create_foreign_key(
        "book_review_fk",
        "reviews",
        "books",
        ["book_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint('user_review_fk','reviews')
    op.drop_constraint('book_review_fk','reviews')
    op.drop_table('reviews')

