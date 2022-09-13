from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [
        KeyboardButton('ТОП дешевых'),
        KeyboardButton('Поиск 🔎'),
        KeyboardButton('ТОП дорогих'),
        KeyboardButton('История \U0001F4D7'),
        KeyboardButton('Избранные ♥'),
        KeyboardButton('Фильтр поиска \U00002699')
    ]

    return markup.add(*buttons)
