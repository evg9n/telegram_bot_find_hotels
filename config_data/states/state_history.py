from telebot.handler_backends import State, StatesGroup


class StateHistory(StatesGroup):
    date = State()
