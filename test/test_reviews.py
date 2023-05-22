import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("review, book_id", [
    ('good',1),
    ('bad',1)])
def test_add_review(authorized_client,review,book_id,test_book,test_user):
    res=authorized_client.post(
        "/reviews",json={"review":review,"book_id":book_id}
    )
    new_review=ReviewBase(**res.json())
    assert new_review.review==review
    assert res.status_code==201

def test_delete_review_exists(authorized_client,test_book,test_user,test_review):
    res=authorized_client.delete(
        "/reviews/1"
    )
    assert res.status_code==204


@pytest.mark.parametrize("id", [
    (1),
    (17238)])
def test_delete_review_not_exists(authorized_client,id):
    res=authorized_client.delete(
        f"/reviews/{id}"
    )
    response=res.json()
    assert response['detail']==f"review not exists with id {id}"
    assert res.status_code==404


def test_update_review_exists(authorized_client,test_book,test_user,test_review):
    res=authorized_client.put(
        "/reviews/1",json={"review":"Excellent"}
    )
    updated_review=ReviewBase(**res.json())
    assert updated_review.review=="Excellent"
    assert res.status_code==200


@pytest.mark.parametrize("id, review", [
    (1,"Gooddd"),
    (17238,"Ok")])
def test_update_review_not_exists(authorized_client,id,review):
    res=authorized_client.put(
        f"/reviews/{id}",json={"review":review}
    )
    response=res.json()
    assert response['detail']==f"review not exists with id {id}"
    assert res.status_code==404