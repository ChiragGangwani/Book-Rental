from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/authors",
    tags=['Authors']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.AuthorGet)
async def add_author(author:schemas.AuthorBase,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    new_author=models.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/list",response_model=List[schemas.AuthorGet])
async def get_authors_list(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    authors=db.query(models.Author).all()
    if authors.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No author exists")
    return authors

@router.get("/{id}",response_model=schemas.AuthorGet)
async def get_author(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     author=db.query(models.Author).filter(models.Author.id==id).first()
     if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Author not exists with id {id}")
     return author

@router.delete("/{id}")
async def delete_author(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     author=db.query(models.Author).filter(models.Author.id==id).first()
     if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Author not exists with id {id}")
     db.delete(author)
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}",response_model=schemas.AuthorGet)
async def update_user(id:int,author:schemas.AuthorBase,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    author_query=db.query(models.Author).filter(models.Author.id==id)
    if not author_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Author not exists with id {id}")
    
    author_query.update(author.dict())
    db.commit()
    return author_query.first()