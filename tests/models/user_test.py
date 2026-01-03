from app.models import Role


def test_user_creation(get_user_data):
    user = get_user_data()

    assert user.is_admin() is False
    assert user.role == Role.USER


def test_admin_user_creation(get_user_data):
    user = get_user_data(role=Role.ADMIN)

    assert user.is_admin() is True
