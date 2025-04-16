from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.user import User, UserCreate, UserUpdate


class UserRepository(ABC):
    @abstractmethod
    async def get_users(self) -> List[User]:
        pass

    @abstractmethod
    async def create_user(self, user_create: UserCreate) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_wallet_id(self, wallet_id: str) -> Optional[User]:
        pass
