import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("name", [
    ('action'),
    ('drama'),
    ('novel')])
def test_add_genre(authorized_client,name):
    res=authorized_client.post(
        "/genres",json={"name":name}
    )
    new_genre=GenreGet(**res.json())
    assert new_genre.name==name
    assert res.status_code==201


def test_get_genre_list_exist(authorized_client,test_genre):
    res=authorized_client.get(
        "/genres/list"
    )
    assert len(res.json())==1
    assert res.status_code==200

def test_get_genre_list_not_exist(authorized_client):
    res=authorized_client.get(
        "/genres/list"
    )
    assert res.json()['detail']=="No genre exists"
    assert res.status_code==404


def test_get_genre_by_id_exists(authorized_client,test_genre):
    res=authorized_client.get(
        "/genres/1"
    )
    new_genre=GenreGet(**res.json())
    assert new_genre.name==test_genre.name
    assert new_genre.id==test_genre.id
    assert res.status_code==200


@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_get_genre_by_id_not_exists(authorized_client,id):
    res=authorized_client.get(
        f"/genres/{id}"
    )
    response=res.json()
    assert response['detail']==f"Genre not exists with id {id}"
    assert res.status_code==404

@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_delete_genre_by_id_not_exists(authorized_client,id):
    res=authorized_client.delete(
        f"/genres/{id}"
    )
    response=res.json()
    assert response['detail']==f"Genre not exists with id {id}"
    assert res.status_code==404


def test_delete_genre_by_id_exists(authorized_client,test_genre):
    res=authorized_client.delete(
        "/genres/1"
    )
    assert res.status_code==204


@pytest.mark.parametrize("id", [
    (1),
    (33),
    (75)])
def test_update_genre_by_id_not_exists(authorized_client,id):
    res=authorized_client.put(
        f"/genres/{id}",json={"name":"action"}
    )
    response=res.json()
    assert response['detail']==f"Genre not exists with id {id}"
    assert res.status_code==404


def test_update_genre_by_id_exists(authorized_client,test_genre):
    res=authorized_client.put(
        "/genres/1",json={"name":"action"}
    )
    new_genre=GenreGet(**res.json())
    assert new_genre.id==test_genre.id
    assert res.status_code==200