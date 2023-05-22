import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("rental_period, book_id", [
    (10,1),
    (4,1)])
def test_add_book_to_cart_book_exist(authorized_client,rental_period,book_id,test_book,test_user):
    res=authorized_client.post(
        "/carts",json={"rental_period":rental_period,"book_id":book_id}
    )
    new_cart=res.json()
    assert new_cart==f"Book with id {book_id} is added successfully"
    assert res.status_code==201

@pytest.mark.parametrize("rental_period, book_id", [
    (10,1),
    (4,1)])
def test_add_book_to_cart_book_not_exist(authorized_client,rental_period,book_id):
    res=authorized_client.post(
        "/carts",json={"rental_period":rental_period,"book_id":book_id}
    )
    new_cart=res.json()
    assert new_cart['detail']==f"Book not available with id {book_id}"
    assert res.status_code==404



def test_delete_book_from_cart_book_exist(authorized_client,test_cart):
    res=authorized_client.delete(
        "/carts/1"
    )
    assert res.status_code==204

@pytest.mark.parametrize("id", [
    (10),
    (4)])
def test_delete_book_from_cart_book_not_exist(authorized_client,id):
    res=authorized_client.delete(
        f"/carts/{id}"
    )
    new_cart=res.json()
    assert new_cart['detail']==f"Cart not available with id {id}"
    assert res.status_code==404


def test_cart_checkout_successfully(authorized_client,test_cart,test_book):
    res=authorized_client.get(
        "/carts/checkout"
    )
    new_cart=res.json()
    assert new_cart.__contains__(f"Order successfully placed and total payment is")
    assert res.status_code==200


def test_cart_checkout_cart_empty(authorized_client):
    res=authorized_client.get(
        "/carts/checkout"
    )
    new_cart=res.json()
    assert new_cart['detail']==f"No book available on cart"
    assert res.status_code==404

