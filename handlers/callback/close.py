from loader import bot
from telebot.types import Message
from keyboards.reply.menu import button_menu
from database.write_database import write_chat, add_user
from sqlite3 import OperationalError


@bot.message_handler(func=lambda message: message.text == 'Отмена' or message.text == 'Главное меню')
def close(message: Message):
    bot.set_state(user_id=message.from_user.id,
                  state=None,
                  chat_id=message.chat.id)

    bot.send_message(chat_id=message.from_user.id, text='Главное меню', reply_markup=button_menu())

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
