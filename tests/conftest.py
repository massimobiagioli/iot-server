import pytest
import uuid
from app.models import User, Role
from app.lib.passwords import hash_password


@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock

    return MagicMock()


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
