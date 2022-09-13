from loader import bot
from states.state_find import StateFind
from telebot.types import Message
from database.write_database import write_chat, add_user, check_hotel_favorite
from keyboards.reply.close import button_close
from sqlite3 import OperationalError


@bot.message_handler(func=lambda message: message.text == 'Поиск 🔎' or message.text == '/bestdeal')
def bestdeal(message: Message) -> None:
    bot.set_state(user_id=message.from_user.id, state=StateFind.city, chat_id=message.chat.id)
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data['sort_top'] = 'free'
    bot.send_message(message.from_user.id, 'В каком городе смотреть отели?', reply_markup=button_close())


    try:
        write_chat(
            user_id=str(message.from_user.id),
            username=message.from_user.username,
            message=message.text
        )
    except OperationalError:
        add_user(user_id=str(message.from_user.id))
        write_chat(
            user_id=str(message.from_user.id),
            username=message.from_user.username,
            message=message.text
        )
