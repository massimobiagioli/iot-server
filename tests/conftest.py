import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import server
from app.models import User, Role
from app.lib.passwords import hash_password
from unittest.mock import MagicMock


@pytest.fixture
def client():
    with TestClient(server) as c:
        yield c


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_uow():
    mock = MagicMock()
    mock.user_repository = MagicMock()
    mock.__enter__.return_value = mock
    return mock


@pytest.fixture
def get_user_data():
    def _get_user_data(
        id=uuid.uuid4(),
        username="testuser",
        password="rightpass",
        firstname="Test",
        lastname="User",
        role=Role.USER,
    ):
        return User(
            id=id,
            username=username,
            password=hash_password(password),
            firstname=firstname,
            lastname=lastname,
            role=role,
        )

    return _get_user_data
