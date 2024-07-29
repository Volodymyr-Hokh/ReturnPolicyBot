from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router

from bot.api_client import create_api_client
from schemas import UserCreate


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    api_client = await create_api_client()
    async with api_client:
        await api_client.create_assistant()
        new_user = UserCreate(
            username=message.from_user.username, telegram_id=message.from_user.id
        )
        await api_client.create_user(new_user)
        await api_client.create_thread(telegram_id=message.from_user.id)
    await message.answer(
        f"Hello, {message.from_user.username}! I`m your assistant. If you have any questions about amazon return policy, feel free to ask me."
    )


@router.message(Command("new_conversation"))
async def command_new_conversation_handler(message: Message) -> None:
    api_client = await create_api_client()
    async with api_client:
        await api_client.delete_all_user_threads(message.from_user.id)
        await api_client.create_thread(telegram_id=message.from_user.id)
    await message.answer("New conversation started!")
