import logging
from typing import List

from app.core.config import settings
from app.models.query_params import UserQueryParams
from app.models.user import User, UserCreate, UserUpdate
from app.repositories import PostgresqlUserRepository, UserRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @classmethod
    def from_config(cls, db: Session = None):
        if settings.REPOSITORY_TYPE == "pgsql" and db:
            repository = PostgresqlUserRepository(db)
        elif settings.REPOSITORY_TYPE == "memory":
            repository = UserRepository()
        else:
            raise ValueError(
                f"Invalid repository type: {settings.REPOSITORY_TYPE}"
            )
        return cls(repository)

    async def list_users(self, params: UserQueryParams) -> List[User]:
        skip = (params.page - 1) * params.limit
        limit = params.limit
        sort_field = params.sortBy or "created_at"
        sort_direction = params.sortDirection.value
        filters = params.match or {}

        return await self.repository.get_users(
            filters=filters,
            sort_field=sort_field,
            sort_direction=sort_direction,
            skip=skip,
            limit=limit,
        )

    def create_user(self, user_create: UserCreate):
        return self.repository.create_user(user_create)

    def update_user(self, user_id: int, user_update: UserUpdate):
        return self.repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int):
        return self.repository.delete_user(user_id)
