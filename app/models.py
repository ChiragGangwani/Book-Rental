from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String,Boolean,TIMESTAMP,Double
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    phoneNumber=Column(String,nullable=False)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)
    books=relationship("Book",back_populates="user")
    reviews=relationship("Review",back_populates="user")
    carts=relationship("Cart",back_populates="user")
    rental_histories=relationship("RentalHistory",back_populates="user")

class Book(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    rental_period=Column(Integer,nullable=False)
    rental_price=Column(Integer,nullable=False)
    availability=Column(Boolean,nullable=False,default=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    user=relationship("User",back_populates="books")
    reviews=relationship("Review",back_populates="book")
    carts=relationship("Cart",back_populates="book")
    authors=relationship("Author",secondary="association_book_author",back_populates="books")
    genres=relationship("Genre",secondary="association_book_genre",back_populates="books")
    rental_histories=relationship("RentalHistory",back_populates="book")
    

class Review(Base):
    __tablename__="reviews"
    id=Column(Integer,primary_key=True,nullable=False)
    review=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"))
    user=relationship("User",back_populates="reviews")
    book_id=Column(Integer,ForeignKey("books.id"))
    book=relationship("Book",back_populates="reviews")

class Cart(Base):
    __tablename__="carts"
    id=Column(Integer,primary_key=True,nullable=False)
    rental_period=Column(Integer,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"))
    user=relationship("User",back_populates="carts")
    book_id=Column(Integer,ForeignKey("books.id"))
    book=relationship("Book",back_populates="carts")

class AssociationBookAuthor(Base):
     __tablename__="association_book_author"
     id=Column(Integer,primary_key=True,nullable=False)
     book_id=Column(Integer,ForeignKey("books.id"))
     author_id=Column(Integer,ForeignKey("authors.id"))

class AssociationBookGenre(Base):
     __tablename__="association_book_genre"
     id=Column(Integer,primary_key=True,nullable=False)
     book_id=Column(Integer,ForeignKey("books.id"))
     genre_id=Column(Integer,ForeignKey("genres.id"))

class Author(Base):
    __tablename__="authors"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    books=relationship("Book",secondary="association_book_author",back_populates="authors")

class Genre(Base):
    __tablename__="genres"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    books=relationship("Book",secondary="association_book_genre",back_populates="genres")

class RentalHistory(Base):
    __tablename__="rental_histories"
    id=Column(Integer,primary_key=True,nullable=False)
    amount=Column(Double,nullable=False)
    status=Column(Boolean,nullable=False,default=True)
    rented_on=Column(TIMESTAMP(timezone=True),nullable=True,default="now()")
    rental_period=Column(Integer,nullable=False)
    book_id=Column(Integer,ForeignKey("books.id"),nullable=False)
    book=relationship("Book",back_populates="rental_histories")
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    user=relationship("User",back_populates="rental_histories")