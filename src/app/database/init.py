import logging

import requests
from app.core.config import settings
from app.models.user import PGUser as User
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


async def init_db():
    """
    Initializes the database by checking if the 'users' table exists.
    If it doesn't, the table is created and mock user data is imported
    from an external API.
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
            result = connection.execute(
                text("SELECT to_regclass('public.users')")
            )
            if result.fetchone()[0] is None:
                logger.info(
                    "The 'users' table does not exist, creating the table..."
                )
                User.metadata.create_all(
                    bind=engine
                )  # Create the 'users' table

                # Once the table is created, import mock data
                logger.info("Importing mock data...")

                mock_url = "https://nubi-challenge.wiremockapi.cloud/users"
                response = requests.get(mock_url)
                if response.status_code == 200:
                    users_data = response.json()
                    db = SessionLocal()
                    for user_data in users_data:
                        user = User(
                            **user_data
                        )  # Make sure the keys match your User model
                        db.add(user)
                    db.commit()
                    logger.info(
                        f"{len(users_data)} users imported successfully."
                    )
                else:
                    logger.warning(
                        "Error fetching mock data."
                        f"Status code: {response.status_code}"
                    )
            else:
                logger.info("The 'users' table already exists.")
        except OperationalError as e:
            logger.error(f"Error attempting to access the database: {e}")
