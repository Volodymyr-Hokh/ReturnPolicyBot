from aiogram.types import Message
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender

from bot.api_client import create_api_client
from bot.utils import normalize_text
from schemas import MessageCreate


router = Router()


@router.message(F.text)
async def text_handler(message: Message):
    async with ChatActionSender.typing(chat_id=message.from_user.id, bot=message.bot):
        api_client = await create_api_client()
        async with api_client:
            thread = await api_client.get_thread_by_user_telegram_id(
                message.from_user.id
            )
            new_message = MessageCreate(content=message.text, thread_id=thread.id)
            response = await api_client.create_message(new_message)
            text = normalize_text(str(response))
            await message.answer(text)
