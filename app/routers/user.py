from datetime import datetime,timedelta
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List

import pytz
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..notification import send_email


router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse|str)
async def add_user(user:schemas.UserCreate,db: Session = Depends(get_db)):

    exist_user_by_email=db.query(models.User).filter(models.User.email==user.email).first()
    exist_user_by_phone=db.query(models.User).filter(models.User.phoneNumber==user.phoneNumber).first()

    if exist_user_by_email!=None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User already exists with email - {user.email}")
    
    if exist_user_by_phone!=None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User already exists with phone number - {user.phoneNumber}")
   
    hashed_password=util.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/list",response_model=List[schemas.UserResponse])
async def get_user_list(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    users=db.query(models.User).all()
    return users

@router.get("/{id}",response_model=schemas.UserResponse)
async def get_one_user(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not exists with id {id}")
    return user

@router.get("/",response_model=schemas.UserResponse)
async def get_current_user(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not exists")
     return current_user
    

@router.delete("/")
async def delete_user(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not exists")
     
     db.delete(current_user)
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT)    
    

@router.put("/",response_model=schemas.UserResponse)
async def update_user(user:schemas.UserUpdate,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    user_query=db.query(models.User).filter(models.User.id==current_user.id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not exists with id {id}")
    
    user_query.update(user.dict())
    db.commit()

    return user_query.first()
