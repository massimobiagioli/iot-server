from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

import os


db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)


def get_session():
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_session)]
