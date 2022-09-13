from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import CallbackQuery
from states.state_find import StateFind
from database.write_database import write_chat, add_user
from datetime import date, timedelta
from utils.misc.send_hotel import send_hotel
from utils.misc.get_calendar import get_calendar
from utils.misc.url import ALL_STEPS
from sqlite3 import OperationalError


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def check_in(call: CallbackQuery):

    today = date.today()
    result, key, step = get_calendar(calendar_id=1,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:

        bot.edit_message_text(f"Выберите {ALL_STEPS[step]} заезда",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = result

            bot.edit_message_text(f"Дата заезда: {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            try:
                write_chat(
                    user_id=str(call.from_user.id),
                    username=call.from_user.username,
                    message=f"Дата заезда: {result}"
                )
            except OperationalError:
                add_user(user_id=str(call.from_user.id))
                write_chat(
                    user_id=str(call.from_user.id),
                    username=call.from_user.username,
                    message=f"Дата заезда: {result}"
                )

            calendar, step = get_calendar(calendar_id=2,
                                          min_date=result + timedelta(days=1),
                                          max_date=result + timedelta(days=365),
                                          locale="ru",
                                          )

            bot.send_message(call.from_user.id,
                             f"Выберите год выезда",
                             reply_markup=calendar)

            bot.set_state(call.from_user.id, StateFind.check_out, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def check_out(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        date_check_in = data['check_in']
    result, key, step = get_calendar(calendar_id=2,
                                     current_date=date_check_in,
                                     min_date=date_check_in + timedelta(days=1),
                                     max_date=date_check_in + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:

        bot.edit_message_text(f"Выберите {ALL_STEPS[step]} выезда",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_out'] = result
            data['nights'] = (result - data['check_in']).days
            data['number'] = -1

            bot.edit_message_text(f"Дата выезда: {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            try:
                write_chat(
                    user_id=str(call.from_user.id),
                    username=call.from_user.username,
                    message=f"Дата выезда: {result}"
                )
            except OperationalError:
                add_user(user_id=str(call.from_user.id))
                write_chat(
                    user_id=str(call.from_user.id),
                    username=call.from_user.username,
                    message=f"Дата выезда: {result}"
                )

            bot.send_sticker(chat_id=call.from_user.id,
                             sticker='CAACAgIAAxkBAAILJmLqUEAAAUGHohzD5uoav-vA9GvIlgACVQADr8ZRGmTn_PAl6RC_KQQ')

        send_hotel(user_id=call.from_user.id,
                   chat_id=call.message.chat.id,
                   back=False,
                   message_id=call.message.message_id + 1)

        bot.set_state(user_id=call.from_user.id,
                      state=StateFind.hotel,
                      chat_id=call.message.chat.id)
