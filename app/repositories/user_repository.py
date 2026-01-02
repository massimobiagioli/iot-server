from app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()
