from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
