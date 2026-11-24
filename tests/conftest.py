import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import Base, get_db
from app.database.test_connection import test_engine, override_get_db
from app.models.task import Task


@pytest.fixture()
def client():

    # Reset only the test database
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Override the original database dependency
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)