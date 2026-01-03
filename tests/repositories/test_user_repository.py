from app.repositories import UserRepository


def test_get_by_id(store_user, db_session):
    new_user = store_user()
    
    user_repository = UserRepository(db_session)
    user = user_repository.get_by_id(new_user.id)

    assert user is not None
    assert user.id == new_user.id
    assert user.username == new_user.username
    assert user.firstname == new_user.firstname
    assert user.lastname == new_user.lastname
    assert user.role == new_user.role


def test_get_by_id_not_found(db_session, wrong_uuid):
    user_repository = UserRepository(db_session)
    user = user_repository.get_by_id(wrong_uuid)
    
    assert user is None


def test_get_by_username(store_user, db_session):
    new_user = store_user()

    user_repository = UserRepository(db_session)
    user = user_repository.get_by_username(new_user.username)
    
    assert user is not None
    assert user.id == new_user.id
    assert user.username == new_user.username
    assert user.firstname == new_user.firstname
    assert user.lastname == new_user.lastname
    assert user.role == new_user.role


def test_get_by_username_not_found(db_session):
    user_repository = UserRepository(db_session)
    user = user_repository.get_by_username("nonexistentuser")
    
    assert user is None