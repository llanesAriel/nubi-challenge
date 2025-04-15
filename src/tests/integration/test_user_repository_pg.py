import pytest
from app.repositories.postgresql import PostgresqlUserRepository
from tests.factories.user_factory import UserFactory


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_user(postgresql_repo):
    user = UserFactory.create_user()
    created = await postgresql_repo.create_user(user)
    assert created.id is not None
    assert created.email == user.email


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_users(postgresql_repo, db_session):
    users = UserFactory.create_pg_users(3)
    db_session.add_all(users)
    await db_session.commit()

    result = await postgresql_repo.get_users(filters={})
    assert len(result) >= 3


@pytest.mark.asyncio
@pytest.mark.integration
async def test_filter_users(postgresql_repo, db_session):
    user = UserFactory.create_pg_user(email="testfilter@example.com", name="TestName")
    db_session.add(user)
    await db_session.commit()

    result = await postgresql_repo.get_users(filters={"email": "testfilter@example.com"})
    assert len(result) == 1
    assert result[0].email == "testfilter@example.com"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_sort_users_ascending(postgresql_repo, db_session):
    db_session.add_all([
        UserFactory.create_pg_user(name="Carlos"),
        UserFactory.create_pg_user(name="Ana"),
        UserFactory.create_pg_user(name="Bruno"),
    ])
    await db_session.commit()

    result = await postgresql_repo.get_users(filters={}, sort_field="name", sort_direction="ascending")
    names = [u.name for u in result]
    assert names == sorted(names)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_sort_users_descending(postgresql_repo, db_session):
    db_session.add_all([
        UserFactory.create_pg_user(name="Carlos"),
        UserFactory.create_pg_user(name="Ana"),
        UserFactory.create_pg_user(name="Bruno"),
    ])
    await db_session.commit()

    result = await postgresql_repo.get_users(filters={}, sort_field="name", sort_direction="descending")
    names = [u.name for u in result]
    assert names == sorted(names, reverse=True)
