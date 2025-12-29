import pytest
from app.services import GetUserById
from app.exceptions import UserNotFoundException
import uuid


def test_get_by_id_found(mock_db, get_user_data):
    user = get_user_data()
    mock_db.exec.return_value.first.return_value = user
    service = GetUserById(mock_db)
    result = service.execute(str(user.id))
    assert result == user


def test_get_by_id_not_found(mock_db):
    mock_db.exec.return_value.first.return_value = None
    service = GetUserById(mock_db)
    with pytest.raises(UserNotFoundException):
        service.execute(str(uuid.uuid4()))
