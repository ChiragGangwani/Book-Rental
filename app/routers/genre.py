from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/genres",
    tags=['Genres']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.GenreGet)
async def add_genre(genre:schemas.GenreBase,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    new_genre=models.Genre(**genre.dict())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre

@router.get("/list",response_model=List[schemas.GenreGet])
async def get_genres_list(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    genres=db.query(models.Genre).all()
    if genres.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No genre exists")
    return genres

@router.get("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.GenreGet)
async def get_genre(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     genre=db.query(models.Genre).filter(models.Genre.id==id).first()
     if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Genre not exists with id {id}")
     return genre

@router.delete("/{id}")
async def delete_genre(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
     genre=db.query(models.Genre).filter(models.Genre.id==id).first()
     if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Genre not exists with id {id}")
     db.delete(genre)
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}",response_model=schemas.GenreGet)
async def update_user(id:int,genre:schemas.GenreBase,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    genre_query=db.query(models.Genre).filter(models.Genre.id==id)
    if not genre_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Genre not exists with id {id}")
    
    genre_query.update(genre.dict())
    db.commit()
    return genre_query.first()