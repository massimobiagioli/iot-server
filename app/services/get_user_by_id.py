from app.exceptions import UserNotFoundException
from app.models import User
from app.lib.database import DBSession
from sqlmodel import select


class GetUserById:
    def __init__(self, db: DBSession):
        self.db = db

    def execute(self, user_id: str) -> User:
        statement = select(User).where(User.id == user_id)
        user = self.db.exec(statement).first()
        if not user:
            raise UserNotFoundException(f"User id '{user_id}' not found")
        return user
