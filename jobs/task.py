from datetime import datetime,timedelta
from fastapi import Depends
import pytz
from app import models
from app import models
from sqlalchemy.orm import Session
from app.notification import send_email
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings





# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def rental_period_expire():
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

    engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    db = SessionLocal()

    rentals=db.query(models.RentalHistory).filter(models.RentalHistory.status==True).all()
    for rental in rentals:
        time=rental.rented_on+timedelta(days=rental.rental_period)
        if time>=datetime.now(tz=pytz.utc) and time<=datetime.now(tz=pytz.utc)+timedelta(days=1):
            await send_email([rental.user.email],f"Your Book {rental.book.title} and Id {rental.book.id} is going to expired. Kindly return it and issue again. \n\nThanks\nChirag Gangwani\nSleevesUp Book Store","Book Rental Period is about to expied")
        elif time<datetime.now(tz=pytz.utc):
            overdue=str(datetime.now(tz=pytz.utc)-time)
            await send_email([rental.user.email],f"Your Book {rental.book.title} and Id {rental.book.id} is Overdue by {overdue[0:overdue.find(',')]}. Kindly return it and issue again. \n\nThanks\nChirag Gangwani\nSleevesUp Book Store","Book Rental Period is Overdue")
    return "mail sended successfully"



