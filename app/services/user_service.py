from repositories.base import UserRepository
from models.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self):
        return self.repository.get_users()

    def create_user(self, user_create: UserCreate):
        return self.repository.create_user(user_create)

    def update_user(self, user_id: int, user_update: UserUpdate):
        return self.repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int):
        return self.repository.delete_user(user_id)
