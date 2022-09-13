from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Dict


def dates_history(info: Dict) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [KeyboardButton(date) for date in info.keys()]
    buttons.append(KeyboardButton('Отмена'))

    return markup.add(*buttons)

