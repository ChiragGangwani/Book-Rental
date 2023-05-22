import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("name", [
    ('kevin'),
    ('peter'),
    ('scarlatt')])
def test_add_author(authorized_client,name):
    res=authorized_client.post(
        "/authors",json={"name":name}
    )
    new_author=AuthorGet(**res.json())
    assert new_author.name==name
    assert res.status_code==201


def test_get_author_list_exist(authorized_client,test_author):
    res=authorized_client.get(
        "/authors/list"
    )
    assert len(res.json())==1
    assert res.status_code==200

def test_get_author_list_not_exist(authorized_client):
    res=authorized_client.get(
        "/authors/list"
    )
    assert res.json()['detail']=="No author exists"
    assert res.status_code==404


def test_get_author_by_id_exists(authorized_client,test_author):
    res=authorized_client.get(
        "/authors/1"
    )
    new_author=AuthorGet(**res.json())
    assert new_author.name==test_author.name
    assert new_author.id==test_author.id
    assert res.status_code==200


@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_get_author_by_id_not_exists(authorized_client,id):
    res=authorized_client.get(
        f"/authors/{id}"
    )
    response=res.json()
    assert response['detail']==f"Author not exists with id {id}"
    assert res.status_code==404

@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_delete_author_by_id_not_exists(authorized_client,id):
    res=authorized_client.delete(
        f"/authors/{id}"
    )
    response=res.json()
    assert response['detail']==f"Author not exists with id {id}"
    assert res.status_code==404


def test_delete_author_by_id_exists(authorized_client,test_author):
    res=authorized_client.delete(
        "/authors/1"
    )
    assert res.status_code==204


@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_update_author_by_id_not_exists(authorized_client,id):
    res=authorized_client.put(
        f"/authors/{id}",json={"name":"chirag"}
    )
    response=res.json()
    assert response['detail']==f"Author not exists with id {id}"
    assert res.status_code==404


def test_update_author_by_id_exists(authorized_client,test_author):
    res=authorized_client.put(
        "/authors/1",json={"name":"chirag"}
    )
    new_author=AuthorGet(**res.json())
    assert new_author.id==test_author.id
    assert res.status_code==200