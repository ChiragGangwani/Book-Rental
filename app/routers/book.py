from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/books",
    tags=['Books']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.BookAddReponse)
async def add_book(book:schemas.BookAdd,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    authors=[]
    genres=[]
    for id in book.authors:
        author=db.query(models.Author).filter(models.Author.id==id).first()
        if not author:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Author with id {id} not exists")
        else:
            authors.append(author)
    
    for id in book.genres:
        genre=db.query(models.Genre).filter(models.Genre.id==id).first()
        if not genre:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Genre with id {id} not exists")
        else:
            genres.append(genre)

    new_book=models.Book(authors=authors,genres=genres,title=book.title,description=book.description,rental_period=book.rental_period,rental_price=book.rental_price)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/list",response_model=List[schemas.BookBase])
async def get_books_list(title:Optional[str]="",author:Optional[str]="",genre:Optional[str]="",db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    books=db.query(models.Book).join(models.AssociationBookAuthor,models.AssociationBookAuthor.book_id==models.Book.id,isouter=True).join(models.Author,models.Author.id==models.AssociationBookAuthor.author_id).join(models.AssociationBookGenre,models.AssociationBookGenre.book_id==models.Book.id,isouter=True).join(models.Genre,models.Genre.id==models.AssociationBookGenre.genre_id).filter(models.Book.title.contains(title),models.Author.name.contains(author),models.Genre.name.contains(genre)).all()
   
    if books.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No book exists")
    
    return books


@router.get("/{id}",response_model=schemas.BookGet)
async def get_book(id:int,db: Session = Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} not exists")
    return book

@router.delete("/{id}",response_model=schemas.BookGet)
async def delete_book(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    book=db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} not exists")
    if book.availability==False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} is issued to user {book.user_id}")
    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/{id}",response_model=schemas.BookGet)
async def update_book(id:int,book:schemas.BookUpdate,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    exist_book=db.query(models.Book).filter(models.Book.id==id).first()
    if not exist_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} not exists")
    
    authors=[]
    genres=[]
    for id in book.authors:
        author=db.query(models.Author).filter(models.Author.id==id).first()
        if not author:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Author with id {id} not exists")
        else:
            authors.append(author)
    
    for id in book.genres:
        genre=db.query(models.Genre).filter(models.Genre.id==id).first()
        if not genre:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Genre with id {id} not exists")
        else:
            genres.append(genre)

    exist_book.availability=book.availability
    exist_book.authors=authors
    exist_book.genres=genres
    exist_book.title=book.title
    exist_book.description=book.description
    exist_book.rental_period=book.rental_period
    exist_book.rental_price=book.rental_price
    db.commit()
    db.refresh(exist_book)
    return exist_book

@router.put("/return/{id}")
async def return_book(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    book=db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No book with id {id}")
    
    book.avalability=True
    book.user_id=None
    rent_history=db.query(models.RentalHistory).filter(models.RentalHistory.book_id==id,models.RentalHistory.user_id==current_user.id,models.RentalHistory.status==True).first()
    if not rent_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You didn't rent book with id {id}")
    
    rent_history.status=False
    db.commit()
    return f"{book.title} is returned"