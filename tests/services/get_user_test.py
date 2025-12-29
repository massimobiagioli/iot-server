import pytest
from app.services import GetUser
from app.exceptions import UserNotFoundException, BadCredentialsException


def test_execute_blank_password(mock_db):
    service = GetUser(mock_db)
    with pytest.raises(BadCredentialsException):
        service.execute("testuser", password="")


def test_execute_user_not_found(mock_db):
    mock_db.exec.return_value.first.return_value = None
    service = GetUser(mock_db)
    with pytest.raises(UserNotFoundException):
        service.execute("notfound", password="rightpass")


def test_execute_bad_password(mock_db, get_user_data):
    mock_db.exec.return_value.first.return_value = get_user_data()
    service = GetUser(mock_db)
    with pytest.raises(BadCredentialsException):
        service.execute("testuser", password="wrongpass")


def test_execute_correct_password(mock_db, get_user_data):
    user = get_user_data()
    mock_db.exec.return_value.first.return_value = user
    service = GetUser(mock_db)
    result = service.execute("testuser", password="rightpass")
    assert result == user
