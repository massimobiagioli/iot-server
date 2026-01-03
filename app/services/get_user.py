from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.exceptions import UserNotFoundException, BadCredentialsException
from app.repositories import UnitOfWork, UnitOfWorkProvider
from app.lib.passwords import verify_password
from app.lib.database import DBSession
from app.models import User


class GetUser:
    def __init__(self, session: Session, unit_of_work: UnitOfWork):
        self.session = session
        self.unit_of_work = unit_of_work

    def __call__(self, username: str, password: str = None) -> User:
        with self.unit_of_work(self.session) as uow:
            user = uow.users.get_by_username(username)
            if not user:
                raise UserNotFoundException(f"User '{username}' not found")
            if not password or not verify_password(password, user.password):
                raise BadCredentialsException("Bad credentials provided")
            self.session.expunge(user)
            return user


def get_user_service(session: DBSession, unit_of_work=UnitOfWorkProvider) -> GetUser:
    return GetUser(session=session, unit_of_work=unit_of_work)


GetUserService = Annotated[GetUser, Depends(get_user_service)]
