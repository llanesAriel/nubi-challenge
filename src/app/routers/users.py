from fastapi import APIRouter, Depends
from typing import List
from app.models.user import User, UserCreate, UserUpdate
from app.models.query_params import UserQueryParams
from app.core.security.auth import get_current_user
from app.services.user_service import UserService
from app.dependencies.query_params import (
    get_user_query_params,
    get_user_service,
)
import logging


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[User])
async def list_users(
    params: UserQueryParams = Depends(get_user_query_params),
    service: UserService = Depends(get_user_service),
):
    return await service.list_users(params)


@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(user)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
