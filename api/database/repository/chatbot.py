from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models import Assistant, Thread, Query
from api.database.repository.users import get_user_by_telegram_id

from schemas import (
    AssistantCreate,
    ThreadCreate,
    ThreadResponse,
    QueryCreate,
)


async def add_assistant(db: AsyncSession, assistant: AssistantCreate) -> Assistant:
    assistant = Assistant(**assistant.model_dump())
    db.add(assistant)
    await db.commit()
    await db.refresh(assistant)
    return assistant


async def get_assistant_by_id(db: AsyncSession, assistant_id: int) -> Assistant:
    result = await db.execute(select(Assistant).where(Assistant.id == assistant_id))
    return result.scalars().first()


async def add_thread(db: AsyncSession, thread: ThreadCreate) -> Thread:
    thread = Thread(**thread.model_dump())
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


async def get_thread_by_id(db: AsyncSession, thread_id: int) -> Thread:
    result = await db.execute(select(Thread).where(Thread.id == thread_id))
    return result.scalars().first()


async def get_thread_by_user_telegram_id(
    db: AsyncSession, user_telegram_id: int
) -> Thread:
    user = await get_user_by_telegram_id(db, user_telegram_id)
    result = await db.execute(select(Thread).where(Thread.user_id == user.id))
    return result.scalars().first()


async def get_thread_by_remote_id(db: AsyncSession, remote_id: str) -> Thread:
    result = await db.execute(select(Thread).where(Thread.remote_id == remote_id))
    return result.scalars().first()


async def delete_thread(thread_id: int, db: AsyncSession) -> None:
    thread = await get_thread_by_id(db, thread_id)
    await db.delete(thread)
    await db.commit()


async def delete_all_user_threads(db: AsyncSession, user_telegram_id: int) -> None:
    user = await get_user_by_telegram_id(db, user_telegram_id)
    result = await db.execute(select(Thread).where(Thread.user_id == user.id))
    threads = result.scalars().all()
    for thread in threads:
        await db.delete(thread)
    await db.commit()


async def add_query(db: AsyncSession, query: QueryCreate) -> Query:
    query = Query(**query.model_dump())
    db.add(query)
    await db.commit()
    await db.refresh(query)
    return query


async def get_users_threads(db: AsyncSession, user_id: int) -> list[ThreadResponse]:
    result = await db.execute(select(Thread).where(Thread.user_id == user_id))
    return result.scalars().all()
