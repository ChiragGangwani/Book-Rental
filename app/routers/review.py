from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/reviews",
    tags=['Reviews']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ReviewBase)
async def add_review(review:schemas.Review,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    
    book=db.query(models.Book).filter(models.Book.id==review.book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book not exists with id {review.book_id}")
    
    new_review=models.Review(review=review.review,book=book,user=current_user)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

@router.delete("/{id}")
async def add_review(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    review=db.query(models.Review).filter(models.Review.id==id).first()
    if not review:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"review not exists with id {id}")
    
    if review.user_id!=current_user.id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"review with id {id} does not belongs to user with id {current_user.id}")
    
    db.delete(review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}",response_model=schemas.ReviewBase)
async def update_review(id:int,new_review:schemas.ReviewUpdate,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    review=db.query(models.Review).filter(models.Review.id==id).first()
    if not review:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"review not exists with id {id}")
    
    if review.user_id!=current_user.id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"review with id {id} does not belongs to user with id {current_user.id}")
    
    review.review=new_review.review
    db.commit()
    db.refresh(review)
    return review