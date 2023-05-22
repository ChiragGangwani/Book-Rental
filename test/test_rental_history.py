import pytest
from app.main import app
from app.schemas import *
from jose import jwt
from app.config import settings



def test_get_all_rental_history_exists(authorized_client,test_checkout):
    res=authorized_client.get(
        "/rent-history/all"
    )
    assert len(res.json())==1
    assert res.status_code==200

def test_get_all_rental_history_not_exists(authorized_client):
    res=authorized_client.get(
        "/rent-history/all"
    )
    assert res.json()['detail']=="No rental history"
    assert res.status_code==404

def test_get_rental_history_by_id_exists(authorized_client,test_checkout):
    res=authorized_client.get(
        "/rent-history/1"
    )
    history=res.json()
    assert res.status_code==200

@pytest.mark.parametrize("id", [
    (10),
    (4)])
def test_get_rental_history_by_user_id_not_exists(authorized_client,id,test_user):
    res=authorized_client.get(
        f"/rent-history/{id}"
    )
    assert res.json()['detail']==f"No rental history for user {id}"
    assert res.status_code==404