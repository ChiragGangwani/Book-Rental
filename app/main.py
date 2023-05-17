from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import List
from . import models,schemas,util
from .database import engine,get_db
from sqlalchemy.orm import Session
from . routers import user,auth,book,author,genre,review,cart,rent_history

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(author.router)
app.include_router(genre.router)
app.include_router(review.router)
app.include_router(cart.router)
app.include_router(rent_history.router)

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='bookRental',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error = ", error)
#         time.sleep(2)



    