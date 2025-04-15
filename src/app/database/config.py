from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.models.user import PGUser as User
from app.core.config import settings
from typing import AsyncGenerator
import logging
import requests


logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")


engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
base = declarative_base()


async def init_db():
    """
    Initializes the database by checking if the 'users' table exists. If it doesn't,
    the table is created and mock user data is imported from an external API.
    """

    # Create the table if it doesn't exist
    engine = create_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    metadata = MetaData()
    metadata.create_all(bind=engine)

    # Check if the 'users' table exists
    with engine.connect() as connection:
        try:
            # Attempt to fetch users from the table to check if it exists
            result = connection.execute(text("SELECT to_regclass('public.users')"))
            if result.fetchone()[0] is None:
                logger.info("The 'users' table does not exist, creating the table...")
                User.metadata.create_all(bind=engine)  # Create the 'users' table

                # Once the table is created, import mock data
                logger.info("Importing mock data...")

                mock_url = "https://nubi-challenge.wiremockapi.cloud/users"
                response = requests.get(mock_url)
                if response.status_code == 200:
                    users_data = response.json()
                    db = SessionLocal()
                    for user_data in users_data:
                        user = User(**user_data)  # Make sure the keys match your User model
                        db.add(user)
                    db.commit()
                    logger.info(f"{len(users_data)} users imported successfully.")
                else:
                    logger.warning(f"Error fetching mock data. Status code: {response.status_code}")
            else:
                logger.info("The 'users' table already exists.")
        except OperationalError as e:
            logger.error(f"Error attempting to access the database: {e}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
