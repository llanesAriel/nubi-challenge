import os


class Settings:
    REPOSITORY_TYPE = os.getenv("REPOSITORY_TYPE", "db")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    ENV = os.getenv("ENV", "development")


settings = Settings()
