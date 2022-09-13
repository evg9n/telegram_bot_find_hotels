from telebot.types import Message, InputMediaPhoto, InputMedia
from loader import bot
from database.write_database import write_chat, add_user
from sqlite3 import OperationalError


@bot.message_handler(content_types=['text', 'sticker', 'audio'])
def bot_echo(message: Message):
    bot.send_message(chat_id=message.chat.id, text='Че?')

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
