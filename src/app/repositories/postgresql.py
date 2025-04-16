import logging
from typing import Any, Dict, List

from sqlalchemy import asc, desc
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.user import UserCreate, UserORM, UserUpdate

logger = logging.getLogger(__name__)


class PostgresqlUserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_users(
        self,
        filters: Dict[str, Any],
        sort_field: str = "created_at",
        sort_direction: str = "ascending",
        skip: int = 0,
        limit: int = 10,
    ) -> List[UserORM]:
        stmt = select(UserORM)

        for field_name, value in filters.items():
            if not hasattr(UserORM, field_name):
                logger.warning(f"Ignorando campo inválido: {field_name}")
                continue
            column = getattr(UserORM, field_name)
            if column is not None:
                stmt = stmt.filter(column.ilike(f"%{value}%"))

        sort_col = getattr(UserORM, sort_field, None)
        if sort_col is not None:
            stmt = stmt.order_by(
                asc(sort_col)
                if sort_direction == "ascending"
                else desc(sort_col)
            )

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_email(self, user_email: str) -> UserORM | None:
        result = await self.db.execute(
            select(UserORM).where(UserORM.email == user_email)
        )
        return result.scalar_one_or_none()

    async def get_by_wallet_id(self, wallet_id: str) -> UserORM | None:
        result = await self.db.execute(
            select(UserORM).where(UserORM.wallet_id == wallet_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_create: UserCreate) -> UserORM:
        db_user = UserORM(**user_create.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(
        self, user_email: str, user_update: UserUpdate
    ) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.email == user_email)
        result = await self.db.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            await self.db.commit()
            await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_email: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.email == user_email)
        result = await self.db.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            await self.db.delete(db_user)
            await self.db.commit()
        return db_user
