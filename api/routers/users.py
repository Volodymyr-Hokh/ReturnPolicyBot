from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_db
from api.database.repository.users import (
    add_user,
    delete_user,
    get_user_by_telegram_id,
)
from schemas import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.

    Args:
        user (UserCreate): The user data to be created.

    Returns:
        UserResponse: The created user data.
    """
    try:
        user_exists = await get_user_by_telegram_id(db=db, telegram_id=user.telegram_id)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists.",
            )
        return await add_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_db(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a user.

    Args:
        user_id (int): The user ID.
    """
    try:
        user = await get_user_by_telegram_id(db=db, telegram_id=telegram_id)
        await delete_user(user_id=user.id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )
