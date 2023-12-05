""" Модуль обработчиков AnimalFactsBot."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import kb
import text
from utils import get_cat_fact, get_cat_picture, get_dog_fact, get_dog_picture

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message) -> None:
    """ Обработчик команды /start, отображающий меню."""
    # Если язык пользователя английский, то отображаем меню и приветствие на английском.
    # Иначе на русском.
    if msg.from_user.language_code == "en":
        await msg.answer(text.GREET_EN.format(name=msg.from_user.full_name),
                         reply_markup=kb.en_keyboard)
    else:
        await msg.answer(text.GREET.format(name=msg.from_user.full_name),
                         reply_markup=kb.ru_keyboard)


@router.message(Command("catfact"))
async def catfact_handler(msg: Message) -> None:
    """ Обработчик команды /catfact."""
    await msg.reply_photo(photo=get_cat_picture(),
                          caption=get_cat_fact(msg.from_user.language_code))


@router.message(Command("dogfact"))
async def dogfact_handler(msg: Message) -> None:
    """ Обработчик команды /dogfact."""
    await msg.reply_photo(photo=get_dog_picture(),
                          caption=get_dog_fact(msg.from_user.language_code))


@router.message(Command("help"))
async def message_handler(msg: Message) -> None:
    """ Обработчик команды /help."""
    # Если язык пользователя английский, то отправляем справку на английском.
    # Иначе на русском.
    if msg.from_user.language_code == "en":
        await msg.reply(text.HELP_EN)
    else:
        await msg.reply(text.HELP)


@router.message(F.text == text.DOG_FACT_BUTTON)
@router.message(F.text == text.DOG_FACT_BUTTON_EN)
async def dog_fact_button(msg: Message) -> None:
    """Обработчик кнопки 'Получить факт о собаках'"""
    await msg.reply_photo(photo=get_dog_picture(),
                          caption=get_dog_fact(msg.from_user.language_code))


@router.message(F.text == text.CAT_FACT_BUTTON)
@router.message(F.text == text.CAT_FACT_BUTTON_EN)
async def cat_fact_button(msg: Message) -> None:
    """Обработчик кнопки 'Получить факт о кошках'"""
    await msg.reply_photo(photo=get_cat_picture(),
                          caption=get_cat_fact(msg.from_user.language_code))


@router.message()
async def not_handled(msg: Message) -> None:
    """ Обработчик сообщений, не соответствующих существующим командам."""
    # Если язык пользователя английский, то отправляем сообщение на английском.
    # Иначе на русском.
    if msg.from_user.language_code == "en":
        await msg.reply(text.NOT_HANDLED_EN)
    else:
        await msg.reply(text.NOT_HANDLED)
