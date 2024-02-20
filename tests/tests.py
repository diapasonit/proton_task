import json

import pytest

from main import app
from migration import db_creation


@pytest.fixture(scope='module')
def create_new_db():
    db_creation('homework_order_lines.csv')


def test_basic_response(create_new_db):
    response = app.test_client().get('/orders/')
    assert response.status_code == 200


def test_empty_list(create_new_db):
    response = app.test_client().get('/orders/follow-up/')
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert len(response_json['order_list']) == 0


def test_description_positive(create_new_db):
    response = app.test_client().get('/orders/5120857')
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['items']) == 4
    assert response_json['items'][1]['name'] == 'Truefit Seals'


def test_description_negative(create_new_db):
    response = app.test_client().get('/orders/12345678')
    assert response.status_code == 404


def test_follow_positive(create_new_db):
    response = app.test_client().post('/orders/follow-up/5120857')
    assert response.status_code == 201


def test_follow_negative(create_new_db):
    response = app.test_client().post('/orders/follow-up/12345678')
    assert response.status_code == 404


def test_unfollow_positive(create_new_db):
    response = app.test_client().post('/orders/unfollow-up/5120857')
    assert response.status_code == 201


def test_unfollow_negative(create_new_db):
    response = app.test_client().post('/orders/unfollow-up/12345678')
    assert response.status_code == 404


def test_follow_unfollow_list(create_new_db):
    test_follow_positive(create_new_db)
    response = app.test_client().get('/orders/follow-up/')
    assert response.status_code == 200
    response_json = json.loads(response.text)
    assert len(response_json) == 1
    assert len(response_json['order_list']) == 1
    test_unfollow_positive(create_new_db)
    response = app.test_client().get('/orders/follow-up/')
    assert response.status_code == 200
    response_json = json.loads(response.text)
    assert len(response_json) == 1
    assert len(response_json['order_list']) == 0
