from datetime import datetime
from typing import List
from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    name:str
    phoneNumber:str
    email:EmailStr


class UserCreate(UserBase):
    password:str


class UserUpdate(BaseModel):
    name:str
    phoneNumber:str

class Book(BaseModel):
    id:int
    title:str
    description:str

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id:int
    books:List[Book]
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str

class TokenData(BaseModel):
    id:int

class BookBase(BaseModel):
    title:str
    description:str

    class Config:
        orm_mode = True

class BookAddReponse(BookBase):
    id:int

class BookAdd(BookBase):
    rental_period:str
    rental_price:str
    authors:List[int]
    genres:List[int]

class AuthorBase(BaseModel):
    name:str

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name:str

    class Config:
        orm_mode = True

class AuthorGet(AuthorBase):
    id:int

class GenreGet(GenreBase):
    id:int

class ReviewBase(BaseModel):
    review:str
    user:AuthorBase

    class Config:
        orm_mode = True

class BookGet(BookBase):
    rental_period:str
    rental_price:str
    authors:List[AuthorBase]
    genres:List[GenreBase]
    reviews:List[ReviewBase]

    class Config:
        orm_mode = True

class BookUpdate(BookAdd):
    availabilty:bool

class Review(BaseModel):
    review:str
    book_id:int

class ReviewUpdate(BaseModel):
    review:str

class Cart(BaseModel):
    rental_period:int
    book_id:int

class RentHistory(BaseModel):
    rental_period:int
    rented_on:datetime
    amount:int
    status:bool
    book_id:int