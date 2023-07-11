import os

import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from credito.app import app
from credito.db import engine
from credito.models import User


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)

def create_api_client_authenticated(email):

    try:
        create_user(email, email)
    except IntegrityError:
        pass

    client = TestClient(app)
    token = client.post(
        "/token",
        data={"username": email, "password": email},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture(scope="function")
def api_client_user1():
    return create_api_client_authenticated("user1@credito.com")


def create_user(email: str, password: str):
    with Session(engine) as session:
        user = User(email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user