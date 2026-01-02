import pytest
from app.services import GetUserById
from app.exceptions import UserNotFoundException
import uuid


def test_get_by_id_found(mock_session, mock_uow, get_user_data):
    user = get_user_data()
    mock_uow.users.get_user_by_id.return_value = user
    service = GetUserById(session=mock_session, unit_of_work=lambda _: mock_uow)
    result = service.execute(str(user.id))
    assert result == user


def test_get_by_id_not_found(mock_session, mock_uow):
    mock_uow.users.get_user_by_id.return_value = None
    service = GetUserById(session=mock_session, unit_of_work=lambda _: mock_uow)
    with pytest.raises(UserNotFoundException):
        service.execute(str(uuid.uuid4()))
