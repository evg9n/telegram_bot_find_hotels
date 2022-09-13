from loader import bot
from telebot.types import Message
from database.write_database import write_chat, get_history, add_user
from keyboards.reply.history import dates_history
from keyboards.inline.history import info_hotel
from states.state_history import StateHistory
from sqlite3 import OperationalError


@bot.message_handler(func=lambda message: message.text == 'История \U0001F4D7' or message.text == '/history')
def history(message: Message):
    try:
        result = get_history(user_id=str(message.from_user.id))

    except OperationalError:
        add_user(str(message.from_user.id))
        result = get_history(user_id=str(message.from_user.id))

    if result:

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data['history'] = result

        bot.send_message(chat_id=message.from_user.id,
                         text='Выбери за какой день показать историю поиска',
                         reply_markup=dates_history(info=result))
        bot.set_state(user_id=message.from_user.id, state=StateHistory.date, chat_id=message.chat.id)

    else:
        bot.send_message(chat_id=message.from_user.id,
                         text='История пустая')

    try:
        write_chat(
            user_id=str(message.from_user.id),
            username=message.from_user.username,
            message=message.text
        )
    except OperationalError:
        add_user(str(message.from_user.id))
        write_chat(
            user_id=str(message.from_user.id),
            username=message.from_user.username,
            message=message.text
        )

@bot.message_handler(state=StateHistory.date)
def show_history(message: Message):
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        list_history = data['history'][message.text]

    for element in list_history:
        time, check_in, check_out, info, url, photo, coordinate_lat, coordinate_lon = element
        bot.send_photo(chat_id=message.from_user.id,
                       photo=photo,
                       caption=f'Время поиска: {time}\n'
                              f'Дата заезда: {check_in}\n'
                              f'Дата выезда: {check_out}\n{info}',
                       reply_markup=info_hotel(coordinate_lat=coordinate_lat,
                                               coordinate_lon=coordinate_lon,
                                               url=url))

    bot.send_message(chat_id=message.from_user.id, text=f'За {message.text} просмотрено отелей: {len(list_history)}')

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
