from loader import bot
from telebot.types import Message
from database.write_database import add_user, get_favorite
from states.state_favorites import StateFavorites
from keyboards.reply.favorites import list_favorites
from keyboards.reply.menu import button_menu
from keyboards.inline.favorites import favorite_hotel
from sqlite3 import OperationalError


@bot.message_handler(func=lambda message: message.text == '/favorites' or message.text == 'Избранные ♥')
def favorites(message: Message) -> None:
    try:

        all_favorites = get_favorite(user_id=message.from_user.id)

    except OperationalError:
        add_user(user_id=str(message.from_user.id))
        all_favorites = get_favorite(user_id=message.from_user.id)

    if not all_favorites:
        bot.send_message(chat_id=message.from_user.id, text='Избранных нет')

    else:
        bot.set_state(user_id=message.from_user.id,
                      state=StateFavorites.favorites,
                      chat_id=message.chat.id)
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data['favorites'] = all_favorites
            list_name = [name['name'] for name in all_favorites]
            data['list_names_favorites'] = list_name
            bot.send_message(chat_id=message.from_user.id,
                             text='Веберите:',
                             reply_markup=list_favorites(name_favorites=list_name))


@bot.message_handler(state=StateFavorites.favorites)
def show_favorite(message: Message):
    if message.text == 'Главное меню':
        bot.set_state(user_id=message.from_user.id,
                      state=None,
                      chat_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Главное меню',
                         reply_markup=button_menu())
    else:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            for favorite in data['favorites']:
                if message.text in favorite['name']:
                    hotel_id = favorite['hotel_id']
                    info = favorite['info']
                    url = favorite['url']
                    photo = favorite['photo']
                    coordinate = favorite['coordinate']
                    bot.send_photo(chat_id=message.from_user.id,
                                   photo=photo,
                                   caption=info,
                                   reply_markup=favorite_hotel(hotel_id=hotel_id, url=url,
                                                               lat=coordinate['lat'], lon=coordinate['lon']))
