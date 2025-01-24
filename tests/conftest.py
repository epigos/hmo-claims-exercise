import typing
from datetime import date

import pytest
from flask.testing import FlaskClient

from app import create_app
from app.claim import Claim, Service
from app.claim.forms import HMO_CHOICES, SERVICE_TYPE_CHOICES
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


@pytest.fixture
def claim_data() -> dict[str, typing.Any]:
    return dict(
        diagnosis="Malaria",
        hmo=HMO_CHOICES[1][0],
        service_charge=10,
        total_cost=100,
        final_cost=110,
    )


@pytest.fixture
def services_data() -> list[dict[str, typing.Any]]:
    return [
        {
            "service_name": "Malaria test",
            "service_date": date.today(),
            "service_type": SERVICE_TYPE_CHOICES[0],
            "provider_name": "Acacia",
            "source": "OPD",
            "cost_of_service": 50,
        },
        {
            "service_name": "Widal test",
            "service_date": date.today(),
            "service_type": SERVICE_TYPE_CHOICES[0],
            "provider_name": "Acacia",
            "source": "OPD",
            "cost_of_service": 50,
        },
    ]


@pytest.fixture
def new_claim(db, new_user, claim_data, services_data) -> Claim:
    claim = Claim(user_id=new_user.id, age=new_user.get_age(), **claim_data)
    db.session.add(claim)
    db.session.commit()

    for service in services_data:
        new_service = Service(
            claim_id=claim.id,
            service_date=service.get("service_date"),
            service_name=service.get("service_name"),
            type=service.get("service_type"),
            provider_name=service.get("provider_name"),
            source=service.get("source"),
            cost_of_service=service.get("cost_of_service"),
        )
        db.session.add(new_service)
    db.session.commit()
    db.session.refresh(claim)
    return claim
