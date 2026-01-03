import pytest
from app.services import GetUser
from app.exceptions import UserNotFoundException, BadCredentialsException


def test_execute_blank_password(mock_session, mock_uow, get_user_data):
    user = get_user_data()
    mock_uow.users.get_by_username.return_value = user
    service = GetUser(session=mock_session, unit_of_work=lambda _: mock_uow)
    with pytest.raises(BadCredentialsException):
        service("testuser", password="")


def test_execute_user_not_found(mock_session, mock_uow):
    mock_uow.users.get_by_username.return_value = None
    service = GetUser(session=mock_session, unit_of_work=lambda _: mock_uow)
    with pytest.raises(UserNotFoundException):
        service("notfound", password="rightpass")


def test_execute_bad_password(mock_session, mock_uow, get_user_data):
    user = get_user_data()
    mock_uow.users.get_by_username.return_value = user
    service = GetUser(session=mock_session, unit_of_work=lambda _: mock_uow)
    with pytest.raises(BadCredentialsException):
        service("testuser", password="wrongpass")


def test_execute_correct_password(mock_session, mock_uow, get_user_data):
    user = get_user_data()
    mock_uow.users.get_by_username.return_value = user
    service = GetUser(session=mock_session, unit_of_work=lambda _: mock_uow)
    result = service("testuser", password="rightpass")
    assert result == user
