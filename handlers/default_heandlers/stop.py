from telebot.types import Message
from loader import bot
from database.write_database import write_chat, add_user
from sqlite3 import OperationalError


@bot.message_handler(commands=['stop'])
def button_stop(message: Message):
    if message.chat.id == 471736540 and message.chat.username == 'evg_9n':
        bot.send_message(message.chat.id, 'Бот остановлен!')
        bot.stop_bot()

    else:
        bot.send_message(message.chat.id, 'Недостаточно прав для этой команды!')

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
