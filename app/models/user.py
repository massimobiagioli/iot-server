import uuid
from enum import Enum

from sqlmodel import Field, SQLModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    role: Role = Field(default=Role.GUEST, nullable=False)


class User(UserBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
