from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def favorite_hotel(hotel_id: str, url: str, lat: str, lon: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    coordinates = lat + '|' + lon
    buttons = [
        InlineKeyboardButton(text='На карте', callback_data=f'coordinates{coordinates}'),
        InlineKeyboardButton(text='Ссылка на сайт', url=url),
        InlineKeyboardButton(text='Удалить из избранных', callback_data=f'delete{hotel_id}'),
        InlineKeyboardButton(text='Закрыть❌', callback_data='close')
    ]

    return markup.add(*buttons)