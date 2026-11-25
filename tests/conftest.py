import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import Base, get_db
from app.database.test_connection import test_engine, override_get_db
from app.models.task import Task
from app.models.user import User



@pytest.fixture()
def client():

    # Reset only the test database
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Override the original database dependency
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:

            # Register a test user
            test_client.post(
                "/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "TestPassword123"
                }
            )

            # Login and obtain JWT token
            login_response = test_client.post(
                "/auth/token",
                data={
                    "username": "test@example.com",
                    "password": "TestPassword123"
                }
            )

            token = login_response.json()["access_token"]

            # Authenticate all requests made by this test client
            test_client.headers.update({
                "Authorization": f"Bearer {token}"
            })

            yield test_client

    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)