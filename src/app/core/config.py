from os import getenv


class Settings:
    REPOSITORY_TYPE = getenv("REPOSITORY_TYPE", "db")
    DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./test.db")
    ENV = getenv("ENV", "development")
    API_KEY = getenv("API_KEY", "SecretNubi")
    API_KEY_NAME = "NUBI-API-KEY"


settings = Settings()
