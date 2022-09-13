from loader import bot
from telebot.types import CallbackQuery, InputMediaPhoto
from states.state_find import StateFind
from keyboards.reply.menu import button_menu
from keyboards.inline.info_hotel import photos, album, gen_murkup
from utils.misc.url import photo_hotel
from utils.misc.send_hotel import send_hotel
from database.write_database import add_user, write_chat, write_favorite, delet_favorite
from sqlite3 import OperationalError


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data == 'coordinate')
def callback_coordinate(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:
        coordinate = data['list_hotels'][data['number']]['coordinate']
        bot.send_location(chat_id=call.from_user.id,
                          latitude=coordinate['lat'],
                          longitude=coordinate['lon'])

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


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data == 'favorite')
def favorite(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:
        hotel_id = data['list_hotels'][data['number']]['id']
        total = len(data["list_hotels"])
        current = data['number'] + 1
        photo = data['photos_hotel'][0]
        text = data['info']
        url = f'hotels.com/ho{data["list_hotels"][data["number"]]["id"]}'
        coordinate = data['list_hotels'][data['number']]['coordinate']
        if data['favorite']:
            delet_favorite(user_id=call.from_user.id, hotel_id=hotel_id)
            data['favorite'] = False
            bot.answer_callback_query(call.id, "Удаленно из избранных", cache_time=3)
        else:

            try:
                write_favorite(user_id=str(call.from_user.id), hotel_id=hotel_id, info=text, url=url,
                              photo=photo, coordinate_lat=coordinate['lat'], coordinate_lon=coordinate['lon'])
            except OperationalError:
                add_user(str(call.from_user.id))
                write_favorite(user_id=str(call.from_user.id), hotel_id=hotel_id, info=text, url=url,
                               photo=photo, coordinate_lat=coordinate['lat'], coordinate_lon=coordinate['lon'])

            data['favorite'] = True
            bot.answer_callback_query(call.id, "Добавлено в избранные", cache_time=3)
        favorite = data['favorite']

    media = InputMediaPhoto(media=photo,
                            caption=text)
    bot.edit_message_media(media=media, chat_id=call.from_user.id, message_id=call.message.message_id,
                           reply_markup=gen_murkup(
                               current=current,
                               total=total,
                               url=url,
                               favorite='❤' if favorite else '🖤'))


@bot.callback_query_handler(state=StateFind.hotel,
                            func=lambda call: call.data == 'photos' or call.data == 'photos_and_del')
def callback_photos(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:
        count_rooms = len(data['photos_rooms'])
        if call.data == 'photos_and_del':
            media = InputMediaPhoto(media=photo_hotel, caption='Выберите альбом:')
            bot.edit_message_media(media=media, chat_id=call.from_user.id, message_id=call.message.message_id,
                                   reply_markup=photos(count_rooms=count_rooms))
        else:
            bot.send_photo(chat_id=call.from_user.id,
                           photo=photo_hotel,
                           caption='Выберите альбом:',
                           reply_markup=photos(count_rooms=count_rooms))

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


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data == 'hotel' or 'room' in call.data)
def callback_photos(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:

        if call.data == 'hotel':
            data['current_album'] = data['photos_hotel']
            data['name_album'] = 'Отель'
            data['count_photo'] = f'{len(data["current_album"])} фото'
        else:
            data['current_album'] = data['photos_rooms'][int(call.data[4:])]
            data['name_album'] = f'Комната {int(call.data[4:]) + 1}'
            data['count_photo'] = f'{len(data["current_album"])} фото'

        data['first_photo_page'] = data['current_photo'] = 0

        media = InputMediaPhoto(media=data['current_album'][data['current_photo']], caption=data['name_album'])
        bot.edit_message_media(media=media, chat_id=call.from_user.id, message_id=call.message.message_id,
                               reply_markup=album(count_photo=data['count_photo'],
                                                  current_album=data['current_album'],
                                                  first_photo_page=data['first_photo_page'],
                                                  current_photo=data['current_photo']))

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


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data in ['<', '>'] or call.data.isdigit())
def callback_photos(call: CallbackQuery):
    with bot.retrieve_data(user_id=call.from_user.id,
                           chat_id=call.message.chat.id) as data:

        if call.data.isdigit():
            if data['current_photo'] != int(call.data):
                data['current_photo'] = int(call.data)
            else:
                return

        elif call.data == '<':
            if data['first_photo_page'] != 0:
                data['first_photo_page'] -= 5
                data['current_photo'] = data['first_photo_page']
            else:
                return

        elif call.data == '>':
            if data['first_photo_page'] + 5 <= len(data['current_album']) - 1:
                data['first_photo_page'] += 5
                data['current_photo'] = data['first_photo_page']
            else:
                return

        media = InputMediaPhoto(media=data['current_album'][data['current_photo']], caption=data['name_album'])
        bot.edit_message_media(media=media, chat_id=call.from_user.id, message_id=call.message.message_id,
                               reply_markup=album(count_photo=data['count_photo'],
                                                  current_album=data['current_album'],
                                                  first_photo_page=data['first_photo_page'],
                                                  current_photo=data['current_photo']))

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


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data == 'back' or call.data == 'next')
def view_hotels(call: CallbackQuery):
    if call.data == 'back':
        send_hotel(user_id=call.from_user.id,
                   chat_id=call.message.chat.id,
                   back=True,
                   message_id=call.message.message_id)
    elif call.data == 'next':
        send_hotel(user_id=call.from_user.id,
                   chat_id=call.message.chat.id,
                   back=False,
                   message_id=call.message.message_id)

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


@bot.callback_query_handler(state=StateFind.hotel, func=lambda call: call.data in ['close', 'other_city', 'menu'])
def callback_photos(call: CallbackQuery):
    if call.data == 'close':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    elif call.data == 'other_city':
        bot.set_state(user_id=call.from_user.id,
                      state=StateFind.city,
                      chat_id=call.message.chat.id)
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id,
                         text='В каком городе смотреть отели?')

    elif call.data == 'menu':
        bot.set_state(user_id=call.from_user.id,
                      state=None,
                      chat_id=call.message.chat.id)
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id, text='Главное меню', reply_markup=button_menu())

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
