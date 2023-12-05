"""Точка входа для AnimalFactsBot"""
import asyncio
import logging
import os

import aiogram.utils.token
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers import router


async def set_default_commands(bot: Bot) -> None:
    """Создание меню команд бота."""
    commands = [BotCommand(command="start", description="Start"),
                BotCommand(command="help", description="Help message"),
                BotCommand(command="catfact", description="Get a random fact about cats"),
                BotCommand(command="dogfact", description="Get a random fact about dogs")
                ]
    await bot.set_my_commands(commands)


async def main():
    """Точка входа."""
    try:
        # Токен извлекается из переменной окружения token.
        # Чтобы указать токен напрямую, нужно заменить аргумент token= ниже вашим токеном.
        bot = Bot(token=os.environ['token'], parse_mode=ParseMode.HTML)
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)
        await set_default_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except (aiogram.utils.token.TokenValidationError, KeyError):
        print("Environmental variable 'token' is not configured correctly."
              "Please specify a correct token either in docker-compose.yml "
              "or as an environmental variable: token='your token' python ./animalfactsbot.py'")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
