import logging
from typing import List

from app.core.config import settings
from app.models.query_params import UserQueryParams
from app.models.user import User, UserCreate, UserUpdate
from app.repositories import PostgresqlUserRepository, UserRepository
from fastapi import HTTPException, status
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

    async def create_user(self, user_create: UserCreate) -> User:
        # Check if the wallet_id already exists
        existing = await self.repository.get_by_wallet_id(
            user_create.wallet_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="wallet_id ya existe",
            )

        # Check if the email already exists
        existing = await self.repository.get_by_email(user_create.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email ya existe",
            )

        return await self.repository.create_user(user_create)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        return await self.repository.update_user(user_id, user_update)

    async def delete_user(self, user_id: int) -> User | None:
        return await self.repository.delete_user(user_id)
