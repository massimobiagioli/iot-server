from app.models import User
from sqlmodel import select


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id: str) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = self.session.exec(statement)
        return result.first()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement)
        return result.first()
