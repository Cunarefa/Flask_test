import os

import pytest
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
        email="aldsojkpy1@msail.ru"
    )
    return user
