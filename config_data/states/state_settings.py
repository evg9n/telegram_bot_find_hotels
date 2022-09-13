from telebot.handler_backends import State, StatesGroup


class StateSettings(StatesGroup):
    settings = State()
    adulst = State()
    children = State()
    min_price = State()
    max_price = State()
    min_distance = State()
    max_distance = State()
