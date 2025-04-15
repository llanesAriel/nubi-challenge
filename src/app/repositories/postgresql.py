import logging
from typing import Any, Dict, List

from sqlalchemy import asc, desc
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.user import PGUser, UserCreate, UserUpdate

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
    ) -> List[PGUser]:
        stmt = select(PGUser)

        for field_name, value in filters.items():
            if not hasattr(PGUser, field_name):
                logger.warning(f"Ignorando campo inválido: {field_name}")
                continue
            column = getattr(PGUser, field_name)
            if column is not None:
                stmt = stmt.filter(column.ilike(f"%{value}%"))

        sort_col = getattr(PGUser, sort_field, None)
        if sort_col is not None:
            stmt = stmt.order_by(
                asc(sort_col)
                if sort_direction == "ascending"
                else desc(sort_col)
            )

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    def get_user_by_id(self, user_id: int) -> PGUser | None:
        return self.db.query(PGUser).filter(PGUser.id == user_id).first()

    async def create_user(self, user_create: UserCreate) -> PGUser:
        db_user = PGUser(**user_create.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(
        self, user_id: int, user_update: UserUpdate
    ) -> PGUser | None:
        db_user = self.db.query(PGUser).filter(PGUser.id == user_id).first()
        if db_user:
            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            await self.db.commit()
            await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> PGUser | None:
        db_user = self.db.query(PGUser).filter(PGUser.id == user_id).first()
        if db_user:
            await self.db.delete(db_user)
            await self.db.commit()
        return db_user
