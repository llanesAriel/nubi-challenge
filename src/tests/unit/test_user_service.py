import pytest
from app.models.query_params import SortDirection, UserQueryParams
from app.repositories.in_memory import InMemoryUserRepository
from app.services.user_service import UserService
from tests.factories.user_factory import UserFactory


@pytest.fixture
def default_user_query_params():
    return UserQueryParams(
        page=1,
        limit=10,
        sortBy=None,
        sortDirection=SortDirection.ascending,
        match={},
    )


@pytest.fixture
async def service_with_users():
    repo = InMemoryUserRepository()
    users = UserFactory.create_users(3)
    for user in users:
        await repo.create_user(user)
    return UserService(repository=repo)


@pytest.mark.asyncio
async def test_list_users_returns_all_created_users(
    service_with_users,
    default_user_query_params,
):
    result = await service_with_users.list_users(default_user_query_params)
    assert len(result) == 3


@pytest.mark.asyncio
async def test_filter_users_by_email_returns_exact_match(
    service_with_users,
    default_user_query_params,
):
    users = await service_with_users.list_users(default_user_query_params)
    target_user = users[0]
    filtered_params = default_user_query_params.model_copy(
        update={"match": {"email": target_user.email}}
    )

    filtered_users = await service_with_users.list_users(filtered_params)
    assert len(filtered_users) == 1
    assert filtered_users[0].email == target_user.email
