from telebot.types import Message
from keyboards.reply.menu import button_menu
from loader import bot
from database.write_database import add_user, write_chat


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f'Привет {message.chat.username} 👋', reply_markup=button_menu())

    add_user(str(message.from_user.id))

    write_chat(
        user_id=str(message.from_user.id),
        username=message.from_user.username,
        message=message.text
    )
