import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, BotCommand, BotCommandScopeDefault

from bot.api_client import create_api_client
from bot.handlers.commands import router as commands_router
from bot.handlers.other import router as other_router
from config import settings

# os.chdir("/root/NewsSite")
TOKEN = settings.telegram_bot_token


async def set_commands():
    commands = [
        BotCommand(command="start", description="Почати роботу"),
        BotCommand(command="new_conversation", description="Почати нову розмову"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    dp.include_router(commands_router)
    dp.include_router(other_router)
    dp.startup.register(set_commands)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
