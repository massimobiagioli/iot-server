from typing import Annotated
from fastapi import Depends
from app.exceptions import UserNotFoundException
from app.lib.database import DBSession
from app.models import User
from app.repositories import UnitOfWork, UnitOfWorkProvider
from sqlmodel import Session
import uuid


class GetUserById:
    def __init__(self, session: Session, unit_of_work: UnitOfWork):
        self.session = session
        self.unit_of_work = unit_of_work

    def execute(self, user_id: str) -> User:
        with self.unit_of_work(self.session) as uow:
            user = uow.users.get_user_by_id(str(uuid.UUID(user_id)))
            if not user:
                raise UserNotFoundException(f"User id '{user_id}' not found")
            return user


def get_user_by_id_service(
    session: DBSession, unit_of_work=UnitOfWorkProvider
) -> GetUserById:
    return GetUserById(session=session, unit_of_work=unit_of_work)


GetUserByIdService = Annotated[GetUserById, Depends(get_user_by_id_service)]
