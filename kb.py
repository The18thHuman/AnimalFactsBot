""" Модуль клавиатур AnimalFactsBot"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from text import CAT_FACT_BUTTON, DOG_FACT_BUTTON, CAT_FACT_BUTTON_EN, DOG_FACT_BUTTON_EN

# Кнопки на русском
buttons = [
        KeyboardButton(text=DOG_FACT_BUTTON, callback_data="get_d"),
        KeyboardButton(text=CAT_FACT_BUTTON, callback_data="get_cat_fact"),
]
# Кнопки на английском
en_buttons = [
        KeyboardButton(text=DOG_FACT_BUTTON_EN, callback_data="get_dog_fact"),
        KeyboardButton(text=CAT_FACT_BUTTON_EN, callback_data="get_cat_fact"),
]
ru_keyboard = ReplyKeyboardMarkup(keyboard=[buttons],
                                  resize_keyboard=True,
                                  one_time_keyboard=False,
                                  selective=True)
en_keyboard = ReplyKeyboardMarkup(keyboard=[en_buttons],
                                  resize_keyboard=True,
                                  one_time_keyboard=False,
                                  selective=True)
