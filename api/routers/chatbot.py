from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException

from api.openai_requests import (
    create_and_fill_vector_storage,
    create_assistant,
    create_thread,
    delete_thread,
    create_message,
    get_messages,
    get_messages_by_remote_id,
)
from api.database.db import get_db
from api.database.repository.chatbot import (
    add_assistant,
    get_assistant_by_id,
    add_thread,
    delete_thread as delete_thread_db,
    add_query,
    get_users_threads,
    delete_all_user_threads,
    get_thread_by_user_telegram_id,
)
from api.database.repository.users import get_user_by_telegram_id
from schemas import (
    AssistantCreate,
    AssistantResponse,
    ThreadCreate,
    ThreadResponse,
    MessageCreate,
    MessageResponse,
    QueryResponse,
)

router = APIRouter(prefix="/chat", tags=["chatbot"])


@router.post(
    "/assistant", response_model=AssistantResponse, status_code=status.HTTP_201_CREATED
)
async def create_assistant_route(db=Depends(get_db)) -> AssistantResponse:
    """
    Create a new assistant.

    Args:
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        AssistantResponse: The created assistant data.
    """
    try:
        assistant_exists = await get_assistant_by_id(db, 1)
        if assistant_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assistant already exists.",
            )
        vector_store = await create_and_fill_vector_storage()
        assistant = await create_assistant(vector_store)
        assistant_model = AssistantCreate(
            name=assistant.name,
            instructions=assistant.instructions,
            remote_id=assistant.id,
            vector_storage_id=vector_store.id,
        )
        assistant_db = await add_assistant(db, assistant_model)
        return assistant_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.get("/assistant/{assistant_id}", response_model=AssistantResponse)
async def read_assistant(assistant_id: int, db=Depends(get_db)) -> AssistantResponse:
    """
    Get an assistant by ID.

    Args:
        assistant_id (int): The assistant ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        AssistantResponse: The assistant data.
    """
    try:
        assistant = await get_assistant_by_id(db, assistant_id)
        return assistant
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.post(
    "/thread", response_model=ThreadResponse, status_code=status.HTTP_201_CREATED
)
async def create_thread_route(
    telegram_id: int,
    name: Optional[str] = None,
    db=Depends(get_db),
) -> ThreadResponse:
    """
    Create a new thread.

    Args:
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        ThreadResponse: The created thread data.
    """
    try:
        user = await get_user_by_telegram_id(db, telegram_id)
        assistant = await get_assistant_by_id(db, 1)
        thread = await create_thread()
        thread_model = ThreadCreate(
            name=name,
            remote_id=thread.id,
            assistant_id=assistant.id,
            user_id=user.id,
        )
        thread_db = await add_thread(db, thread_model)
        return thread_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.get("/thread/{telegram_id}", response_model=ThreadResponse)
async def read_thread(telegram_id: int, db=Depends(get_db)) -> ThreadResponse:
    """
    Get a thread by user ID.

    Args:
        telegram_id (int): The user ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        ThreadResponse: The thread data.
    """
    try:
        user = await get_user_by_telegram_id(db, telegram_id)
        thread = await get_thread_by_user_telegram_id(db, user.telegram_id)
        return thread
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.delete(
    "/thread/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_thread_route(thread_id: int, db=Depends(get_db)):
    """
    Delete a thread by ID.

    Args:
        thread_id (int): The thread ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        None
    """
    try:
        await delete_thread(db, thread_id)
        await delete_thread_db(db=db, thread_id=thread_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.delete(
    "/threads/{telegram_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_all_user_threads_route(telegram_id: int, db=Depends(get_db)):
    """
    Delete all threads by user ID.

    Args:
        telegram_id (int): The user ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        None
    """
    try:
        await delete_all_user_threads(db, telegram_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.post(
    "/message/",
    response_model=QueryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message_route(
    message: MessageCreate,
    db=Depends(get_db),
) -> QueryResponse:
    """
    Create a new message.

    Args:
        message (MessageCreate): The message data.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        QueryResponse: The created query data.
    """
    try:
        message = await create_message(
            db=db, thread_id=message.thread_id, content=message.content
        )
        query = await add_query(db, message)
        return query
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.get("/messages/", response_model=List[MessageResponse])
async def read_messages(thread_id: str, db=Depends(get_db)) -> List[MessageResponse]:
    """
    Get messages by thread ID.

    Args:
        thread_id (int): The thread ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        List[MessageResponse]: The messages data.
    """
    try:
        messages = await get_messages(db, thread_id)
        return messages or []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.get("/threads/", response_model=List[ThreadResponse])
async def read_threads(telegram_id: int, db=Depends(get_db)) -> List[ThreadResponse]:
    """
    Get threads by user ID.

    Args:
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        List[ThreadResponse]: The threads data.
    """
    try:
        user = await get_user_by_telegram_id(db, telegram_id)
        threads = await get_users_threads(db, user.id)
        return threads
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )
