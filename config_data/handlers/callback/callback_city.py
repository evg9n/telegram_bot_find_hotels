from loader import bot
from telebot.types import CallbackQuery
from states.state_find import StateFind
from datetime import date, timedelta
from utils.misc.get_calendar import get_calendar
from database.write_database import write_chat, add_user
from sqlite3 import OperationalError


@bot.callback_query_handler(state=StateFind.district_city, func=None)
def callback_city(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['city'] = data['dict_cities'][str(call.data)]
        data['city_id'] = str(call.data)
        print(data['city_id'])
        bot.edit_message_text(text=f'Район выбран: {data["city"]}',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

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

    today = date.today()
    calendar, step = get_calendar(calendar_id=1,
                                  current_date=today,
                                  min_date=today,
                                  max_date=today + timedelta(365),
                                  locale='ru')

    bot.set_state(user_id=call.from_user.id, state=StateFind.check_in, chat_id=call.message.chat.id)
    bot.send_message(chat_id=call.from_user.id, text=f'Выбери год заезда:', reply_markup=calendar)
