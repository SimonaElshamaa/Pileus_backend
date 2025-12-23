from fastapi import APIRouter
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_new_user(user: UserCreate):
    return await create_user(user)
