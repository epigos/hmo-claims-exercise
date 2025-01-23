from datetime import date

import pytest
from flask.testing import FlaskClient

from app import create_app
from app.extensions import database
from app.users import User


@pytest.fixture
def client() -> FlaskClient:
    app = create_app("testing")

    app.config["TESTING"] = True
    app.testing = True

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def db(client):
    # Create the database and the database table
    database.create_all()
    yield database
    database.session.remove()
    database.drop_all()


@pytest.fixture
def new_user(db) -> User:
    user = User(
        name="test", gender="male", salary=12000, date_of_birth=date(1990, 1, 1)
    )
    db.session.add(user)
    db.session.commit()
    return user
