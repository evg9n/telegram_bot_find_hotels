from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.misc.url import currency_dict, dict_sort, dict_guest_rating, dict_stars
from typing import Optional


def currency() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=key, callback_data=value) for key, value in currency_dict.items()]
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))
    return markup.add(*buttons)


def list_sort() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in dict_sort.items()]
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))
    return markup.add(*buttons)


def list_guest_rating() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = [
        InlineKeyboardButton(text=value, callback_data='guest' + key)
        for key, value in dict_guest_rating.items() if key != '0']
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))
    return markup.add(*buttons)


def list_stars() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=value, callback_data='stars' + key)
        for key, value in dict_stars.items()]
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))
    return markup.add(*buttons)

def distance(min_distance: Optional[float], max_distance: Optional[float])  -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = list()
    for elem_one in range(11):
        for elem_two in [0, 0.2, 0.4, 0.6, 0.8]:
            number = float(elem_one) + elem_two
            if min_distance:
                if number < min_distance:
                    continue
            if max_distance:
                if number > max_distance:
                    break

            buttons.append(InlineKeyboardButton(text=f'{number} км', callback_data=str(number)))

    buttons.append(InlineKeyboardButton(text='Не установлено', callback_data='-'))
    buttons.append(InlineKeyboardButton(text='Закрыть❌', callback_data='close'))

    return markup.add(*buttons)