from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from typing import List


def list_favorites(name_favorites: List) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    buttons = [KeyboardButton(name) for name in name_favorites]
    buttons.append(KeyboardButton('Главное меню'))

    return markup.add(*buttons)

