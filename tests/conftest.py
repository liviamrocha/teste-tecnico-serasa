import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from credito.app import app
from credito.cli import create_user


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


