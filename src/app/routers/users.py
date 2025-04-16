import logging
from typing import List

from app.core.security.auth import validate_api_key
from app.dependencies.query_params import (
    get_user_query_params,
    get_user_service,
)
from app.models.query_params import UserQueryParams
from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(validate_api_key)]
)


@router.get("/", response_model=List[User])
async def list_users(
    params: UserQueryParams = Depends(get_user_query_params),
    service: UserService = Depends(get_user_service),
):
    return await service.list_users(params)


@router.post("/", response_model=User)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user(user)


@router.put("/{user_email}", response_model=User)
async def update_user(
    user_email: str,
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user(user_email, user)


@router.delete("/{user_email}")
async def delete_user(
    user_email: str,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.delete_user(user_email)
    if not user:
        logger.error(f"User with email {user_email} not found.")
        return {"message": "User not found"}
    return {"message": "User deleted successfully"}
