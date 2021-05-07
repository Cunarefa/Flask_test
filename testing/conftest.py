from datetime import datetime
import os

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy.orm.session import close_all_sessions
from api2 import create_app, db
from api2.models import User


@pytest.fixture
def client():
    _app = create_app()
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    client = _app.test_client()

    with _app.app_context():
        db.create_all()

        yield client

        close_all_sessions()
        db.drop_all()


@pytest.fixture
def user():
    user = User(
        username="testuser1",
        password="12345",
        email="aldo@msail.ru",
        role="VIEWER",
        country="France",
        sex="MALE",
        date_of_birth=datetime.strptime('20-01-1999', '%d-%m-%Y').date()
    )
    return user


@pytest.fixture
def user_register(user):
    db.session.add(user)
    db.session.commit()


@pytest.fixture
def headers(user, user_register):
    access_token = create_access_token(identity=user.username)
    return {'Authorization': 'Bearer {}'.format(access_token)}
