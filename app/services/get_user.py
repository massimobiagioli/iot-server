from app.exceptions import UserNotFoundException, BadCredentialsException
from app.lib.passwords import verify_password
from app.models.user import User
from app.lib.database import DBSession
from sqlmodel import select


class GetUser:
    def __init__(self, db: DBSession):
        self.db = db

    def execute(self, username: str, password: str = None) -> User:
        statement = select(User).where(User.username == username)
        user = self.db.exec(statement).first()
        if not user:
            raise UserNotFoundException(f"User '{username}' not found")
        if not password or not verify_password(password, user.password):
            raise BadCredentialsException("Bad credentials provided")
        return user
