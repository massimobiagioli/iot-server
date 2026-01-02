from typing import Annotated
from fastapi import Depends
from app.lib.database import DBSession
from app.repositories import UserRepository


class UnitOfWork:
    def __init__(self, session):
        self.session = session
        self.users = None

    def __enter__(self):
        self.users = UserRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


def get_unit_of_work(session: DBSession) -> UnitOfWork:
    return UnitOfWork(session)


UnitOfWorkProvider = Annotated[UnitOfWork, Depends(get_unit_of_work)]
