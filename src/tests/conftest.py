import pytest
import pytest_asyncio
from app.core.config import settings
from app.database.config import base
from app.repositories.postgresql import PostgresqlUserRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest_asyncio.fixture
async def postgresql_repo(db_session):
    return PostgresqlUserRepository(db_session)


@pytest.fixture(autouse=True)
async def prepare_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def clean_users_table(db_session):
    yield
    try:
        await db_session.execute(
            text("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
        )
        await db_session.commit()
    except Exception:
        await db_session.rollback()
