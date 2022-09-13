from telebot.types import Message
from database.write_database import write_chat, add_user
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from sqlite3 import OperationalError


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text))
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
