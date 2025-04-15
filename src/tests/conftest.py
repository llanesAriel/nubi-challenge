from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.config import base
from app.repositories.postgresql import PostgresqlUserRepository
from app.core.config import settings
import pytest
import pytest_asyncio


engine = create_async_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def postgresql_repo(db_session):
    return PostgresqlUserRepository(db_session)


@pytest_asyncio.fixture(autouse=True)
async def clean_users_table(db_session):
    yield
    await db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    await db_session.commit()
