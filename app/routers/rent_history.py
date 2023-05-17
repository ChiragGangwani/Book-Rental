from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/rent-history",
    tags=['Rent History']
)

@router.get("/all")
async def get_all_history(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    histories=db.query(models.RentalHistory).all()

    if histories.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No rental history")
    
    return histories

@router.get("/{id}")
async def get_history(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    histories=db.query(models.RentalHistory).filter(models.RentalHistory.user_id==id).all()

    if histories.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No rental history for user {id}")
    
    return histories


