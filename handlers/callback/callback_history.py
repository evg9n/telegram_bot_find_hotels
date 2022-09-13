from loader import bot
from telebot.types import CallbackQuery
from states.state_history import StateHistory
from database.write_database import add_user, write_chat
from sqlite3 import OperationalError


@bot.callback_query_handler(state=StateHistory.date,
                            func=lambda call: 'coordinates' == call.data[0:11])
def coordinates(call: CallbackQuery):
    lat, lon = call.data[11:].split('|')
    bot.send_location(chat_id=call.from_user.id,
                      latitude=lat,
                      longitude=lon)

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
