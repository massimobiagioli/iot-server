import pytest

from app.models.user import User, Role
from app.lib.passwords import hash_password


@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock

    return MagicMock()


@pytest.fixture
def user_data():
    return User(
        username="testuser",
        password=hash_password("rightpass"),
        firstname="Test",
        lastname="User",
        role=Role.USER,
    )
