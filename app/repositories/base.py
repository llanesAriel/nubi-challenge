from abc import ABC, abstractmethod
from typing import List
from models.user import User, UserCreate, UserUpdate


class UserRepository(ABC):
    @abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, user_create: UserCreate) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass
