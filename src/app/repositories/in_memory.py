import logging
from typing import Any, Dict, List

from app.models.user import User, UserCreate, UserUpdate

from .base import UserRepository

logger = logging.getLogger(__name__)


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: List[User] = []
        self.next_id = 1

    async def get_users(
        self,
        filters: Dict[str, Any] = None,
        sort_field: str = "created_at",
        sort_direction: str = "ascending",
        skip: int = 0,
        limit: int = 10,
    ) -> List[User]:
        users = self.users

        if filters:
            for field, value in filters.items():
                users = [
                    u
                    for u in users
                    if getattr(u, field, "").lower() == value.lower()
                ]

        if sort_field:
            try:
                users = sorted(
                    users,
                    key=lambda u: getattr(u, sort_field),
                    reverse=(sort_direction == "descending"),
                )
            except AttributeError:
                pass

        return users[skip : skip + limit]

    async def get_by_email(self, wallet_id):
        for user in self.users:
            if user.email == wallet_id:
                return user

    async def get_by_wallet_id(self, wallet_id):
        for user in self.users:
            if user.wallet_id == wallet_id:
                return user

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(id=self.next_id, **user_create.model_dump())
        self.users.append(user)
        self.next_id += 1
        return user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        for user in self.users:
            if user.id == user_id:
                for field, value in user_update.model_dump(
                    exclude_unset=True
                ).items():
                    setattr(user, field, value)
                return user
        raise ValueError("User not found")

    async def delete_user(self, user_id: int) -> None:
        for user in self.users:
            if user.id == user_id:
                self.users.remove(user)
                return
        raise ValueError("User not found")
