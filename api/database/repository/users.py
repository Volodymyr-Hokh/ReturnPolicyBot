from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models import User
from schemas import UserCreate, UserUpdate


async def add_user(db: AsyncSession, user: UserCreate) -> User:
    user = User(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()


async def get_all_users(
    db: AsyncSession,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> list[User]:
    query = select(User)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession) -> User:
    user_db = await get_user_by_id(db, user_id)
    for field, value in user.model_dump().items():
        if value is not None:
            setattr(user_db, field, value)
    await db.commit()
    await db.refresh(user_db)
    return user_db


async def change_password(user_id: int, password: str, db: AsyncSession) -> User:
    user = await get_user_by_id(db, user_id)
    user.password = password
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> None:
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
