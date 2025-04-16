import uuid
from datetime import datetime
from typing import Optional

from app.core.database.config import base
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID as SA_UUID


class BaseUser(BaseModel):
    created_at: datetime


class User(BaseUser):
    id: int
    email: str
    name: str
    last_name: str
    sex_type: str
    dni: str
    birth_date: datetime
    wallet_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str
    name: str
    last_name: str
    sex_type: str
    dni: str
    birth_date: datetime
    wallet_id: uuid.UUID


class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    sex_type: Optional[str] = None
    dni: Optional[str] = None
    birth_date: Optional[datetime] = None


class UserORM(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(
        SA_UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4
    )
    email = Column(String, unique=True, index=True)
    name = Column(String)
    last_name = Column(String)
    sex_type = Column(String)
    dni = Column(String)
    birth_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
