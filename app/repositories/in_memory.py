from typing import List
from .base import UserRepository
from models.user import User, UserCreate, UserUpdate
import requests
import logging


logger = logging.getLogger(__name__)


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = []
        self.next_id = 1

    def get_users(self) -> List[User]:
        return self.users

    def create_user(self, user_create: UserCreate) -> User:
        user = User(id=self.next_id, **user_create.dict())
        self.users.append(user)
        self.next_id += 1
        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        for user in self.users:
            if user.id == user_id:
                if user_update.name is not None:
                    user.name = user_update.name
                if user_update.email is not None:
                    user.email = user_update.email
                return user
        raise ValueError("User not found")

    def delete_user(self, user_id: int) -> None:
        for user in self.users:
            if user.id == user_id:
                self.users.remove(user)
                return
        raise ValueError("User not found")

    def load_initial_data(self):
        if self.users:
            logger.info("Initial data already loaded. Skipping.")
            return
        try:
            response = requests.get("https://nubi-challenge.wiremockapi.cloud/users")
            response.raise_for_status()
            users_data = response.json()

            for user_data in users_data:
                user = User(
                    id=self.next_id,
                    name=user_data["name"],
                    email=user_data["email"]
                )
                self.users.append(user)
                self.next_id += 1

            logger.info(f"Loaded {len(self.users)} users from mock API.")

        except Exception as e:
            logger.warning(f"Could not fetch initial users. Starting with empty repository. Error: {e}")
