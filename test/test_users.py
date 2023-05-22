import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("email, password, name, phoneNumber", [
    ('cc@gmail.com', 'C@123', 'chirag', '6792625262' ),
    ('ccc@gmail.com', 'Pass123', 'naman', '9876053456'),
    ('chirag@gmail.com', 'Password@123', 'chirag', '98646557753')])
def test_create_user(client,email,password,phoneNumber,name):
    res=client.post(
        "/users",json={"name":name,"phoneNumber":phoneNumber,"email":email,"password":password}
    )
    print(res)
    new_user=UserResponse(**res.json())
    assert new_user.email==email
    assert res.status_code==201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    # print("test_user")
    assert id == test_user['id']
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('cc@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sss@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code


@pytest.mark.parametrize("id", [
    (1),
    (2)])
def test_get_user_exist(authorized_client,id,test_user2):
    res=authorized_client.get(
        f"/users/{id}"
    )
    new_user=UserResponse(**res.json())
    assert new_user.id==id
    assert res.status_code==200

@pytest.mark.parametrize("id", [
    (2),
    (3)])
def test_get_user_not_exist(authorized_client,id):
    res=authorized_client.get(
        f"/users/{id}"
    )
    assert res.status_code==404

def test_get_user_list(authorized_client,test_user2):
    res=authorized_client.get(
        "/users/list"
    )
    def validate(user):
        return UserResponse(**user)
    user_map = map(validate, res.json())
    users_list = list(user_map)
    assert len(res.json()) ==2
    assert res.status_code==200


def test_delete_user_exist(authorized_client):
    res=authorized_client.delete(
        f"/users"
    )
    assert res.status_code==204

def test_delete_user_not_authorize(client):
    res=client.delete(
        f"/users"
    )
    assert res.status_code==401

@pytest.mark.parametrize("name, phoneNumber", [
    ('chirag', '6792625262' ),
    ('naman', '9876053456')])
def test_update_user_exist(authorized_client,name,phoneNumber):
    res=authorized_client.put(
        f"/users",json={"name":name,"phoneNumber":phoneNumber}
    )
    user=UserResponse(**res.json())
    assert user.name==name
    assert user.phoneNumber==phoneNumber
    assert res.status_code==200

@pytest.mark.parametrize("name, phoneNumber", [
    ('chirag', '6792625262' ),
    ('naman', '9876053456')])
def test_update_user_not_authorized(client,name,phoneNumber):
    res=client.put(
        f"/users",json={"name":name,"phoneNumber":phoneNumber}
    )
    assert res.status_code==401