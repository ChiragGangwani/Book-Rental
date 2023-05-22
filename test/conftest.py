from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.schemas import *
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"name":"chirag","phoneNumber":"9876545678","email": "c@gmail.com",
                 "password": "c@123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"name":"ram","phoneNumber":"78636846836","email": "ram@gmail.com",
                 "password": "r@123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_author(authorized_client):
    author_data = {"name":"kevin"}
    res = authorized_client.post("/authors", json=author_data)

    assert res.status_code == 201

    new_author =AuthorGet(**res.json())
    new_author.name =="kevin"
    return new_author

@pytest.fixture
def test_genre(authorized_client):
    genre_data = {"name":"action"}
    res = authorized_client.post("/genres", json=genre_data)

    assert res.status_code == 201

    new_genre =GenreGet(**res.json())
    new_genre.name =="action"
    return new_genre

@pytest.fixture
def test_book(authorized_client,test_author,test_genre):
    res=authorized_client.post(
        f"/books",json={"title":"marvel","description":"marvel", "rental_period":10, "rental_price":100, "authors":[1], "genres":[1]}
    )
    book=BookAddReponse(**res.json())
    
    assert book.title=="marvel"
    assert book.description=="marvel"
    assert res.status_code==201
    return book

@pytest.fixture
def test_book_issued(authorized_client,test_author,test_genre):
    res=authorized_client.post(
        f"/books",json={"title":"marvel","description":"marvel", "rental_period":10, "rental_price":100, "authors":[1], "genres":[1]}
    )
    book=BookUpdate(**res.json())
    book.availabilty=False
    assert book.title=="marvel"
    assert book.description=="marvel"
    assert book.availabilty==False
    assert res.status_code==201
    return book


@pytest.fixture
def test_review(authorized_client,test_book,test_user):
    res=authorized_client.post(
        "/reviews",json={"review":"good","book_id":1}
    )
    new_review=ReviewBase(**res.json())
    assert new_review.review=="good"
    assert res.status_code==201
    return new_review

@pytest.fixture
def test_cart(authorized_client,test_book,test_user):
    res=authorized_client.post(
        "/carts",json={"rental_period":10,"book_id":1}
    )
    new_cart=res.json()
    assert new_cart==f"Book with id 1 is added successfully"
    assert res.status_code==201
    return new_cart

@pytest.fixture
def test_checkout(authorized_client,test_cart,test_book):
    res=authorized_client.get(
        "/carts/checkout"
    )
    new_cart=res.json()
    assert new_cart.__contains__(f"Order successfully placed and total payment is")
    assert res.status_code==200
    return new_cart