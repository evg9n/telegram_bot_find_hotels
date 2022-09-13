from telebot.types import ReplyKeyboardMarkup


def button_close() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена')
