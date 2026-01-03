from app.models import Role


def test_user_creation(user_builder):
    user = user_builder()

    assert user.is_admin() is False
    assert user.role == Role.USER


def test_admin_user_creation(user_builder):
    user = user_builder(role=Role.ADMIN)

    assert user.is_admin() is True
