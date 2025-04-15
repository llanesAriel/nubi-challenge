from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base


class User(BaseModel):
    email: str
    name: str
    last_name: str
    sex_type: str
    dni: str
    birth_date: datetime
    wallet_id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    pass


class UserUpdate(User):
    pass


class PGUser(declarative_base()):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    last_name = Column(String)
    sex_type = Column(String)
    dni = Column(String)
    birth_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
