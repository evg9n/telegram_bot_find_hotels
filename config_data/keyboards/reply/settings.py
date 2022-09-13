from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils.misc.url import dict_sort, dict_guest_rating


def buttons_settings(settings: dict) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1)
    currency, sort, min_guest_rating, star_rating, min_price, max_price, adults, children, amenity, min_distance,\
        max_distance = settings.values()
    buttons = [
        KeyboardButton(text=f'Валюта: {currency}'),
        KeyboardButton(text=f'Сортировка: {dict_sort[sort]}'),
        KeyboardButton(text=f'Минимальный гостевой рейтинг: '
                            f'{dict_guest_rating[min_guest_rating]}'),
        KeyboardButton(text=f'Количество звезд: '
                            f'{star_rating if star_rating != "0" else "не установлено"}'),
        KeyboardButton(text=f'Минимальная цена за ночь: '
                            f'{min_price + " " + currency if min_price != "0" else "не установлено"}'),
        KeyboardButton(text=f'Максимальная цена за ночь: '
                            f'{max_price + " " + currency if max_price != "0" else "не установлено"}'),
        KeyboardButton(text=f'Количество взрослых: {settings["adults"]}'),
        KeyboardButton(text=f'Количество детей: {settings["children"]}'),
        # KeyboardButton(text=f'Удобства: {amenity if amenity != "0" else "не установлено"}'),
        KeyboardButton(text='Минимальное расстояние до центра: '
                            f'{min_distance+" км" if min_distance != "-" else "Не установлено"}'),
        KeyboardButton(text='Максимальное расстояние до центра: '
                            f'{max_distance+" км" if max_distance != "-" else "Не установлено"}'),
        KeyboardButton(text=f'Главное меню')
    ]

    return markup.add(*buttons)
