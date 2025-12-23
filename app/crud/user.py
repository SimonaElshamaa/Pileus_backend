from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.db.base import async_session
from app.core.auth import get_password_hash

async def create_user(user: UserCreate):
    async with async_session() as session:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

async def get_user_by_email(email: str):
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(email=email))
        return result.scalars().first()
