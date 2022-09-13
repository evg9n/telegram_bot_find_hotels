from telebot.handler_backends import State, StatesGroup


class StateFavorites(StatesGroup):
    favorites = State()
