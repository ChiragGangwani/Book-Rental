"""create book,author,genre table

Revision ID: 978e531fe8c2
Revises: c544d713b472
Create Date: 2023-05-18 12:48:24.047520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '978e531fe8c2'
down_revision = 'c544d713b472'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('books',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('rental_period', sa.Integer(), nullable=False),
                    sa.Column('rental_price', sa.Integer(), nullable=False),
                    sa.Column('availability', sa.Boolean(), nullable=False,default=True),
                    sa.Column('user_id', sa.Integer(), nullable=True))
    
    op.create_table('authors',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('name', sa.String(), nullable=False))
    
    op.create_table('genres',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('name', sa.String(), nullable=False))
    
    op.create_table('association_book_author',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('book_id', sa.Integer(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=False))
    
    op.create_table('association_book_genre',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('book_id', sa.Integer(), nullable=False),
                    sa.Column('genre_id', sa.Integer(), nullable=False))
    
    op.create_foreign_key(
        "user_book_fk",
        "books",
        "users",
        ["user_id"],
        ["id"]
    )

    op.create_foreign_key(
        "association_book_author_fk",
        "association_book_author",
        "books",
        ["book_id"],
        ["id"]
    )

    op.create_foreign_key(
        "association_author_book_fk",
        "association_book_author",
        "authors",
        ["author_id"],
        ["id"]
    )

    op.create_foreign_key(
        "association_book_genre_fk",
        "association_book_genre",
        "books",
        ["book_id"],
        ["id"]
    )

    op.create_foreign_key(
        "association_genre_book_fk",
        "association_book_genre",
        "genres",
        ["genre_id"],
        ["id"]
    )
def downgrade() -> None:
    op.drop_constraint('user_book_fk','books')
    op.drop_constraint('association_book_author_fk','association_book_author')
    op.drop_constraint('association_author_book_fk','association_book_author')
    op.drop_constraint('association_book_genre_fk','association_book_genre')
    op.drop_constraint('association_genre_book_fk','association_book_genre')
    op.drop_table('books')
    op.drop_table('authors')
    op.drop_table('genres')
