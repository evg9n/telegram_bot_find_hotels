from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def gen_murkup(current: int, total: int, url: str, favorite: str) -> InlineKeyboardMarkup:
    murkup = InlineKeyboardMarkup(row_width=3)

    buttons = [
        InlineKeyboardButton(text='На карте', callback_data='coordinate'),
        InlineKeyboardButton(text='Ссылка на сайт',
                             url=url),
        InlineKeyboardButton(text='Фото', callback_data='photos'),
        InlineKeyboardButton(text='Назад', callback_data='back'),
        InlineKeyboardButton(text=f'{current}/{total}', callback_data='None'),
        InlineKeyboardButton(text='Дальше', callback_data='next'),
        InlineKeyboardButton(text='🔎Другой город', callback_data='other_city'),
        InlineKeyboardButton(text=favorite, callback_data='favorite'),
        InlineKeyboardButton(text='Главное меню', callback_data='menu')
    ]

    return murkup.add(*buttons)


def photos(count_rooms: int) -> InlineKeyboardMarkup:
    murkup = InlineKeyboardMarkup(row_width=1)

    buttons = [InlineKeyboardButton(text='Отель', callback_data='hotel')]
    if count_rooms > 0:
        for number in range(count_rooms):
            buttons.append(InlineKeyboardButton(text=f'Комната {number + 1}',
                                                callback_data=f'room{number}'))

    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))

    return murkup.add(*buttons)


def album(count_photo: str, current_album: List, current_photo: int, first_photo_page: int) -> InlineKeyboardMarkup:
    murkup = InlineKeyboardMarkup(row_width=7)
    max_photo = len(current_album) - 1
    buttons = [InlineKeyboardButton(text='<', callback_data='<' if first_photo_page != 0 else 'None')]

    for number in range(first_photo_page, first_photo_page + 5):
        if number <= max_photo:
            buttons.append(InlineKeyboardButton(text=f'{number + 1}⋅' if number == current_photo else f'{number + 1}',
                                                callback_data=str(number)))
        else:
            buttons.append(InlineKeyboardButton(text='', callback_data='None'))
    buttons.append(InlineKeyboardButton(text='>', callback_data='>'))
    buttons.append(InlineKeyboardButton(text='Альбомы', callback_data='photos_and_del'))
    buttons.append(InlineKeyboardButton(text=f"{count_photo}", callback_data='None'))
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))
    return murkup.add(*buttons)

