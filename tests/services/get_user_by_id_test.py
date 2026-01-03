import pytest
from app.services import GetUserById
from app.exceptions import UserNotFoundException


def test_get_by_id_found(mock_session, mock_uow, get_user_data, new_uuid_as_string):
    user = get_user_data()
    mock_uow.users.get_by_id.return_value = user
    service = GetUserById(session=mock_session, unit_of_work=lambda _: mock_uow)
    result = service(new_uuid_as_string())
    assert result == user


def test_get_by_id_not_found(mock_session, mock_uow, new_uuid_as_string):
    mock_uow.users.get_by_id.return_value = None
    service = GetUserById(session=mock_session, unit_of_work=lambda _: mock_uow)
    with pytest.raises(UserNotFoundException):
        service(new_uuid_as_string())
