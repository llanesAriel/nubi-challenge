from fastapi import APIRouter, Depends
from models.user import User, UserCreate, UserUpdate
from repositories.in_memory import InMemoryUserRepository
from services.user_service import UserService
from security.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)
repository = InMemoryUserRepository()
user_service = UserService(repository)


@router.get("/", response_model=list[User])
def get_users():
    return user_service.get_users()


@router.post("/", response_model=User)
def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
