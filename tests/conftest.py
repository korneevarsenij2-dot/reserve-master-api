import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """тестовый клиент для всех файлов тестов"""
    with TestClient(app) as test_client:
        yield test_client