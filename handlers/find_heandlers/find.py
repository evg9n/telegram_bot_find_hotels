from loader import bot
from states.state_find import StateFind
from telebot.types import Message
from database.write_database import write_chat, get_settings, add_user
from utils.misc.rapid_api import find_city
from keyboards.inline.cities import gen_markup
from sqlite3 import OperationalError


@bot.message_handler(state=StateFind.city)
def get_city(message: Message):

    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data['city'] = message.text

        try:
            data['settings'] = get_settings(user_id=str(message.from_user.id))
            if not data['settings']:
                add_user(str(message.from_user.id))
                data['settings'] = get_settings(user_id=str(message.from_user.id))
        except OperationalError:
            add_user(user_id=str(message.from_user.id))
            data['settings'] = get_settings(user_id=str(message.from_user.id))

        try:
            data['dict_cities'] = find_city(city=message.text)

            if data['dict_cities']:
                bot.set_state(user_id=message.from_user.id, state=StateFind.district_city, chat_id=message.chat.id)
                bot.send_message(chat_id=message.from_user.id,
                                 text='Выберите район:',
                                 reply_markup=gen_markup(data['dict_cities']))

            else:
                bot.send_message(chat_id=message.from_user.id,
                                 text=f'Не слышал о таком городе {message.text} 🤔\nПопробуй другой')
        except AttributeError:
            bot.send_message(chat_id=message.from_user.id,
                             text=f'Что-то пошло не так 🤔\nПопробуй еще раз')

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
