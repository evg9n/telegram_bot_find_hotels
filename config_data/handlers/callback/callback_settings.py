from loader import bot
from telebot.types import CallbackQuery
from states.state_settings import StateSettings
from utils.misc.url import currency_dict, dict_sort
from database.write_database import update_settings, write_chat, add_user
from sqlite3 import OperationalError
from keyboards.reply.settings import buttons_settings
from database.write_database import get_settings


@bot.callback_query_handler(state=StateSettings.settings, func=lambda call: call.data in currency_dict.values())
def currency(call: CallbackQuery):
    bot.set_state(user_id=call.from_user.id,
                  state=None,
                  chat_id=call.message.chat.id)
    update_settings(user_id=str(call.from_user.id), setting='currency', value=call.data)
    settings = get_settings(user_id=str(call.from_user.id))
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.from_user.id,
                     text='Валюта обновлена🤝',
                     reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.settings, func=lambda call: call.data in dict_sort.keys())
def sort(call: CallbackQuery):
    bot.set_state(user_id=call.from_user.id,
                  state=None,
                  chat_id=call.message.chat.id)
    update_settings(user_id=str(call.from_user.id), setting='sort', value=call.data)
    settings = get_settings(user_id=str(call.from_user.id))
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.from_user.id,
                     text='Сортировка обновлена👌',
                     reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.settings, func=lambda call: 'guest' in call.data)
def sort(call: CallbackQuery):
    bot.set_state(user_id=call.from_user.id,
                  state=None,
                  chat_id=call.message.chat.id)
    update_settings(user_id=str(call.from_user.id), setting='min_guest_rating', value=call.data[5:])
    settings = get_settings(user_id=str(call.from_user.id))
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.from_user.id,
                     text='Минимальный гостевой рейтинг обновлен👍',
                     reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.settings, func=lambda call: 'stars' in call.data)
def sort(call: CallbackQuery):
    bot.set_state(user_id=call.from_user.id,
                  state=None,
                  chat_id=call.message.chat.id)
    update_settings(user_id=str(call.from_user.id), setting='star_rating', value=call.data[5:])
    settings = get_settings(user_id=str(call.from_user.id))
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.from_user.id,
                     text='Количество звезд обновлен👍',
                     reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.min_distance, func=lambda call: call.data)
def min_distance(call: CallbackQuery):
    if call.data == 'close':
        bot.set_state(user_id=call.from_user.id,
                      state=None,
                      chat_id=call.message.chat.id)
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    else:
        update_settings(user_id=str(call.from_user.id),
                        setting='min_distance',
                        value=call.data)
        settings = get_settings(user_id=str(call.from_user.id))
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id,
                         text='Минимальная дистанция обновлена👍',
                         reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.max_distance, func=lambda call: call.data)
def max_distance(call: CallbackQuery):
    if call.data == 'close':
        bot.set_state(user_id=call.from_user.id,
                      state=None,
                      chat_id=call.message.chat.id)
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    else:
        update_settings(user_id=str(call.from_user.id),
                        setting='max_distance',
                        value=call.data)
        settings = get_settings(user_id=str(call.from_user.id))
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id,
                         text='Максимальная дистанция обновлена👍',
                         reply_markup=buttons_settings(settings=settings))

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )


@bot.callback_query_handler(state=StateSettings.settings, func=lambda call: call.data == 'close')
def callback_photos(call: CallbackQuery):
    bot.set_state(user_id=call.from_user.id,
                  state=None,
                  chat_id=call.message.chat.id)
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    try:
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
    except OperationalError:
        add_user(user_id=str(call.from_user.id))
        write_chat(
            user_id=str(call.from_user.id),
            username=call.from_user.username,
            message=call.data
        )
