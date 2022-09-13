from telebot.handler_backends import State, StatesGroup


class StateFind(StatesGroup):
    city = State()
    get_hotels = State()
    hotel = State()
    check_in = State()
    check_out = State()
    district_city = State()