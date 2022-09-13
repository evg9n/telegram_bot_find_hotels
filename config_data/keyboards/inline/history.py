from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def info_hotel(coordinate_lat: str, coordinate_lon: str, url: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    coordinates = coordinate_lat + '|' + coordinate_lon
    buttons = [
        InlineKeyboardButton(text='На карте', callback_data=f'coordinates{coordinates}'),
        InlineKeyboardButton(text='Ссылка на сайт', url=url)
    ]
    return markup.add(*buttons)
