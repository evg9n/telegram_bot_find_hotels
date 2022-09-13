from loader import bot
from telebot.types import CallbackQuery
from states.state_favorites import StateFavorites
from database.write_database import add_user, write_chat, delet_favorite, get_favorite
from keyboards.reply.favorites import list_favorites
from keyboards.reply.menu import button_menu
from sqlite3 import OperationalError


@bot.callback_query_handler(state=StateFavorites.favorites,
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


@bot.callback_query_handler(state=StateFavorites.favorites,
                            func=lambda call: 'delete' == call.data[:6])
def delete(call: CallbackQuery):
    hotel_id = call.data[6:]
    delet_favorite(user_id=call.from_user.id, hotel_id=hotel_id)
    bot.answer_callback_query(call.id, "Удаленно из избранных", cache_time=3)
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


    all_favorites = get_favorite(user_id=call.from_user.id)
    if not all_favorites:
        bot.send_message(chat_id=call.from_user.id, text='Избранных нет', reply_markup=button_menu())

    else:
        with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
            data['favorites'] = all_favorites
            print(all_favorites)
            list_name = [name['name'] for name in all_favorites]
            data['list_names_favorites'] = list_name
            bot.send_message(chat_id=call.from_user.id,
                             text='Веберите:',
                             reply_markup=list_favorites(name_favorites=list_name))

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

@bot.callback_query_handler(state=StateFavorites.favorites,
                            func=lambda call: 'close' == call.data)
def close(call: CallbackQuery):
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

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