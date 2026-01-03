import pytest
import uuid
from app import get_settings
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from app.main import server
from app.models import User, Role
from app.lib.passwords import hash_password
from unittest.mock import MagicMock


settings = get_settings()

engine = create_engine(settings.database_test_url)


@pytest.fixture
def client():
    with TestClient(server) as c:
        yield c


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_uow():
    mock = MagicMock()
    mock.user_repository = MagicMock()
    mock.__enter__.return_value = mock
    return mock


@pytest.fixture(scope="function")
def db_session():
    SQLModel.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        SQLModel.metadata.drop_all(engine)


@pytest.fixture
def user_builder():
    def _builder(
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

    return _builder


@pytest.fixture
def store_user(db_session, user_builder):
    def _store_user(**kwargs):
        user = user_builder(**kwargs)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _store_user


@pytest.fixture
def new_uuid_as_string():
    return lambda: str(uuid.uuid4())


@pytest.fixture
def wrong_uuid():
    return uuid.UUID("00000000-0000-0000-0000-000000000000")
