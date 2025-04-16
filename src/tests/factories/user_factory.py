from datetime import date, datetime
from uuid import uuid4

from app.models.user import UserCreate, UserORM
from faker import Faker

fake = Faker()


class UserFactory:
    @staticmethod
    def create_pg_user(**overrides) -> UserORM:
        data = {
            "wallet_id": str(uuid4()),
            "email": fake.email(),
            "name": fake.first_name(),
            "last_name": fake.last_name(),
            "sex_type": fake.random_element(elements=("male", "female")),
            "dni": str(fake.random_number(digits=8)),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=100),
            "created_at": date.today(),
        }
        data.update(overrides)
        return UserORM(**data)

    @staticmethod
    def create_user(**overrides) -> UserCreate:
        data = {
            "name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "sex_type": fake.random_element(elements=("male", "female")),
            "dni": str(fake.random_number(digits=8)),
            "birth_date": fake.date_of_birth(
                minimum_age=18, maximum_age=100
            ).isoformat(),
            "created_at": datetime.now(),
            "wallet_id": str(uuid4()),
        }
        data.update(overrides)
        return UserCreate(**data)

    @staticmethod
    def create_users(n: int = 10, **overrides) -> list[UserCreate]:
        return [UserFactory.create_user(**overrides) for _ in range(n)]

    @staticmethod
    def create_pg_users(n: int = 3, **overrides) -> list:
        return [UserFactory.create_pg_user(**overrides) for _ in range(n)]
