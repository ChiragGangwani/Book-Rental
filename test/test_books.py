import pytest
from app.main import app
from app.schemas import *
from app.config import settings


@pytest.mark.parametrize("title, description, rental_period, rental_price, authors, genres", [
    ('book1', 'marvel', 5, 150, [1], [1] ),
    ('book2', 'game', 10, 100, [1],[1])])
def test_add_book(authorized_client,test_author, test_genre, title, description, rental_period, rental_price, authors, genres):
    res=authorized_client.post(
        f"/books",json={"title":title,"description":description, "rental_period":rental_period, "rental_price":rental_price, "authors":authors, "genres":genres}
    )
    print(res.json())
    book=BookAddReponse(**res.json())
    
    assert book.title==title
    assert book.description==description
    assert res.status_code==201


@pytest.mark.parametrize("title, description, rental_period, rental_price, authors, genres", [
    ('book1', 'marvel', 5, 150, [1], [1] ),
    ('book2', 'game', 10, 100, [2],[1])])
def test_add_book_author_not_exists(authorized_client, test_genre, title, description, rental_period, rental_price, authors, genres):
    res=authorized_client.post(
        f"/books",json={"title":title,"description":description, "rental_period":rental_period, "rental_price":rental_price, "authors":authors, "genres":genres}
    )
    response=res.json()
    assert response['detail']==f"Author with id {authors[0]} not exists"
    assert res.status_code==404


@pytest.mark.parametrize("title, description, rental_period, rental_price, authors, genres", [
    ('book1', 'marvel', 5, 150, [1], [2] ),
    ('book2', 'game', 10, 100, [1],[3])])
def test_add_book_genre_not_exists(authorized_client, test_author, title, description, rental_period, rental_price, authors, genres):
    res=authorized_client.post(
        f"/books",json={"title":title,"description":description, "rental_period":rental_period, "rental_price":rental_price, "authors":authors, "genres":genres}
    )
    response=res.json()
    assert response['detail']==f"Genre with id {genres[0]} not exists"
    assert res.status_code==404

def test_get_book_list(authorized_client,test_book):
    res=authorized_client.get(
        f"/books/list"
    )
    assert len(res.json()) ==1
    assert res.status_code==200


def test_get_book_exists(authorized_client,test_book):
    res=authorized_client.get(
        f"/books/{1}"
    )
    book=BookGet(**res.json())
    assert book.title==test_book.title
    assert book.description==test_book.description
    assert res.status_code==200

@pytest.mark.parametrize("id", [
    (1),
    (2)])
def test_get_book_not_exists(authorized_client,id):
    res=authorized_client.get(
        f"/books/{id}"
    )
    book=res.json()
    assert book['detail']==f"Book with id {id} not exists"
    assert res.status_code==404


def test_delete_book_exists(authorized_client,test_book):
    res=authorized_client.delete(
        f"/books/{1}"
    )
    assert res.status_code==204

@pytest.mark.parametrize("id", [
    (1),
    (2)])
def test_delete_book_not_exists(authorized_client,id):
    res=authorized_client.delete(
        f"/books/{id}"
    )
    response=res.json()
    assert response['detail']==f"Book with id {id} not exists"
    assert res.status_code==404


@pytest.mark.parametrize("id, title, description, rental_period, rental_price, authors, genres, availability", [
    (1, 'book1', 'marvel', 5, 150, [1], [1], True),
    (1, 'book2', 'game', 10, 100, [1],[1], False)])
def test_update_book_exists(authorized_client,id,test_book,test_author, test_genre, title, description, rental_period, rental_price, authors, genres,availability):
    res=authorized_client.put(
        f"/books/{id}",json={"title":title,"description":description, "rental_period":rental_period, "rental_price":rental_price, "authors":authors, "genres":genres,"availability":availability}
    )
    book=BookGet(**res.json())
    assert book.title==title
    assert book.description==description
    assert res.status_code==200

@pytest.mark.parametrize("id, title, description, rental_period, rental_price, authors, genres, availability", [
    (1, 'book1', 'marvel', 5, 150, [1], [1], True),
    (1, 'book2', 'game', 10, 100, [1],[1], False)])
def test_update_book_not_exists(authorized_client,id,test_author, test_genre, title, description, rental_period, rental_price, authors, genres,availability):
    res=authorized_client.put(
        f"/books/{id}",json={"title":title,"description":description, "rental_period":rental_period, "rental_price":rental_price, "authors":authors, "genres":genres,"availability":availability}
    )
    response=res.json()
    assert response['detail']==f"Book with id {id} not exists"
    assert res.status_code==404