from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,util,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/carts",
    tags=['Carts']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_to_cart(cart:schemas.Cart,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    book=db.query(models.Book).filter(models.Book.id==cart.book_id,models.Book.avalability==True).first()
    already_cart=db.query(models.Cart).filter(models.Cart.book_id==cart.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book not available with id {cart.book_id}")
    
    if book.rental_period<cart.rental_period or cart.rental_period<1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Please check the rental period")
    
    if already_cart:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Book with id {cart.book_id} is already present in cart")

    new_cart=models.Cart(user_id=current_user.id,**cart.dict())
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return f"Book with id {cart.book_id} is added successfully"

@router.delete("/{id}")
async def add_to_cart(id:int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    cart=db.query(models.Cart).filter(models.Cart.id==id).first()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cart not available with id {id}")
    
    db.delete(cart)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  
    

@router.get("/checkout")
async def cart_checkout(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    carts=db.query(models.Cart).filter(models.Cart.user_id==current_user.id).all()
    if carts.__len__()==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No book available on cart")
    payment=0
    for cart in carts:
        book=db.query(models.Book).filter(models.Book.id==cart.book_id).first()
        if book.avalability==False or not book:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book not available with id {cart.book_id} kindly delete this book")
        book.user_id=current_user.id
        book.avalability=False
        rental=models.RentalHistory(amount=book.rental_price*cart.rental_period,book_id=book.id,user_id=current_user.id,rental_period=cart.rental_period)
        db.add(rental)
        db.commit()
        payment+=book.rental_price*cart.rental_period
    db.query(models.Cart).filter(models.Cart.user_id==current_user.id).delete()
    db.commit()
    return f"Order successfully placed and total payment is {payment}"