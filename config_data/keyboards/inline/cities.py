from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union


def gen_markup(dict_buttons: Union[dict, list]):
    markup = InlineKeyboardMarkup(row_width=2)

    for key, value in dict_buttons.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
