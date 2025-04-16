from os import getenv

import pytest
from app.dependencies.query_params import get_user_service
from app.main import app
from app.repositories.in_memory import InMemoryUserRepository
from app.services.user_service import UserService
from httpx import ASGITransport, AsyncClient
from tests.factories.user_factory import UserFactory

API_KEY = getenv("API-Key", "secret123")
HEADERS = {"NUBI-API-KEY": API_KEY}


@pytest.fixture(scope="function")
async def client_with_inmemory_users():
    repo = InMemoryUserRepository()

    # Crear 4 usuarios de prueba
    predefined_users = [
        {"name": "John", "last_name": "Doe", "email": "jdoe@example.com"},
        {"name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
        {"name": "Alice", "last_name": "Brown", "email": "alice@example.com"},
        {"name": "Bob", "last_name": "White", "email": "bob@example.com"},
    ]

    for user_data in predefined_users:
        user = UserFactory.create_user(**user_data)
        await repo.create_user(user)  # ✅ await porque ahora es async

    service = UserService(repository=repo)
    app.dependency_overrides[get_user_service] = lambda: service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.integration
async def test_get_users(client_with_inmemory_users):
    response = await client_with_inmemory_users.get("/users/", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.integration
async def test_get_users_pagination(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?page=1&limit=2", headers=HEADERS
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.integration
async def test_get_users_sorting(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?sortBy=name&sortDirection=ascending", headers=HEADERS
    )
    assert response.status_code == 200
    names = [user["name"] for user in response.json()]
    assert names == sorted(names)


@pytest.mark.integration
async def test_get_users_sorting_descending(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?sortBy=name&sortDirection=descending", headers=HEADERS
    )
    assert response.status_code == 200
    names = [user["name"] for user in response.json()]
    assert names == sorted(names, reverse=True)


@pytest.mark.integration
async def test_get_users_filter_by_email(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?match=%7B%22email%22%3A%22jdoe@example.com%22%7D",
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "jdoe@example.com"


@pytest.mark.integration
async def test_get_users_filter_by_name(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?match=%7B%22name%22%3A%22John%22%7D", headers=HEADERS
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "John"


@pytest.mark.integration
async def test_get_users_combined_filter_sort_pagination(
    client_with_inmemory_users,
):
    url = (
        "/users/?page=1&limit=2&sortBy=email&sortDirection=ascending"
        "&match=%7B%22name%22%3A%22Jane%22%7D"
    )
    response = await client_with_inmemory_users.get(url, headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Jane"
    assert response.json()[0]["email"] == "jane@example.com"


@pytest.mark.integration
async def test_get_users_no_results(client_with_inmemory_users):
    response = await client_with_inmemory_users.get(
        "/users/?match=%7B%22email%22%3A%22notfound@example.com%22%7D",
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
