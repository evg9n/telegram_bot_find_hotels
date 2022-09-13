from loader import bot
from telebot.types import Message
from database.write_database import write_chat, get_settings, update_settings, add_user
from states.state_settings import StateSettings
from keyboards.reply.settings import buttons_settings
from keyboards.inline.settings import currency, list_sort, list_guest_rating, list_stars, distance
from sqlite3 import OperationalError


@bot.message_handler(func=lambda message: message.text == 'Фильтр поиска \U00002699' or message.text == '/settings')
def list_settings(message: Message):

    try:
        settings = get_settings(user_id=str(message.from_user.id))
        if not settings:
            add_user(str(message.from_user.id))
            settings = get_settings(user_id=str(message.from_user.id))
    except OperationalError:
        add_user(user_id=str(message.from_user.id))
        settings = get_settings(user_id=str(message.from_user.id))

    bot.send_message(chat_id=message.from_user.id,
                     text='Настройки поиска:',
                     reply_markup=buttons_settings(settings=settings))

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


@bot.message_handler(state=StateSettings.adulst, content_types=['text'])
def count_adulst(message: Message):
    if message.text.isdigit():
        bot.set_state(user_id=message.from_user.id,
                      state=None,
                      chat_id=message.chat.id)
        update_settings(user_id=str(message.from_user.id), setting='adults', value=message.text)
        settings = get_settings(user_id=str(message.from_user.id))
        bot.send_message(chat_id=message.from_user.id,
                         text='Количество взрослых обновлено🤟',
                         reply_markup=buttons_settings(settings=settings))

    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Ну не бывает столько {message.text} людей🤦\n'
                              'Отправь мне еще раз количество взрослых')

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


@bot.message_handler(state=StateSettings.children, content_types=['text'])
def count_children(message: Message):
    if message.text.isdigit():
        bot.set_state(user_id=message.from_user.id,
                      state=None,
                      chat_id=message.chat.id)
        update_settings(user_id=str(message.from_user.id), setting='children', value=message.text)
        settings = get_settings(user_id=str(message.from_user.id))
        bot.send_message(chat_id=message.from_user.id,
                         text='Количество детей обновлено🤟',
                         reply_markup=buttons_settings(settings=settings))

    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Ну не бывает столько {message.text} детей🤦\n'
                              'Отправь мне еще раз количество детей')

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


@bot.message_handler(state=StateSettings.min_price, content_types=['text'])
def min_price(message: Message):
    if message.text.isdigit():
        max_pric = int(get_settings(user_id=message.from_user.id)['max_price'])
        if int(message.text) <= max_pric or max_pric == 0:
            bot.set_state(user_id=message.from_user.id,
                          state=None,
                          chat_id=message.chat.id)
            update_settings(user_id=str(message.from_user.id), setting='min_price',
                            value=message.text)
            settings = get_settings(user_id=message.from_user.id)
            bot.send_message(chat_id=message.from_user.id,
                             text='Минимальная цена за ночь обновлена🤟',
                             reply_markup=buttons_settings(settings=settings))
        else:
            bot.send_message(chat_id=message.from_user.id,
                             text='Минимальная цена не может быть больше максимальной\n'
                                  f'Введи стоимость не более {max_pric}')
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Ну не бывает такой стоимости {message.text}🤦\n'
                              'Попробуй еще раз')

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


@bot.message_handler(state=StateSettings.max_price, content_types=['text'])
def max_price(message: Message):
    if message.text.isdigit():
        min_pric = int(get_settings(user_id=message.from_user.id)['min_price'])
        if int(message.text) >= min_pric or int(message.text) == 0:
            bot.set_state(user_id=message.from_user.id,
                          state=None,
                          chat_id=message.chat.id)
            update_settings(user_id=str(message.from_user.id), setting='max_price',
                            value=message.text)
            settings = get_settings(user_id=message.from_user.id)
            bot.send_message(chat_id=message.from_user.id,
                             text='Максимальная цена за ночь обновлена🤟',
                             reply_markup=buttons_settings(settings=settings))
        else:
            bot.send_message(chat_id=message.from_user.id,
                             text='Максимальная цена не может быть меньше минимальной\n'
                                  f'Введи стоимость не менее {min_pric}')
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Ну не бывает такой стоимости {message.text}🤦\n'
                              'Попробуй еще раз')

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


@bot.message_handler(content_types=['text'])
def edit_settings(message: Message):

    try:
        settings = get_settings(user_id=message.from_user.id)
        if not settings:
            add_user(user_id=message.from_user.id)
            settings = get_settings(user_id=message.from_user.id)
    except OperationalError:
        add_user(user_id=message.from_user.id)
        settings = get_settings(user_id=message.from_user.id)

    min_distance = float(settings['min_distance']) if settings['min_distance'] != '-' else None
    max_distance = float(settings['max_distance']) if settings['max_distance'] != '-' else None

    if 'Валюта:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text='Выберите валюту:',
                         reply_markup=currency())
        bot.set_state(user_id=message.from_user.id, state=StateSettings.settings, chat_id=message.chat.id)

    elif 'Сортировка:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text='Выберите сортировку:',
                         reply_markup=list_sort())
        bot.set_state(user_id=message.from_user.id, state=StateSettings.settings, chat_id=message.chat.id)

    elif 'Минимальный гостевой рейтинг:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text='Выберите минимальный гостевой рейтинг:',
                         reply_markup=list_guest_rating())
        bot.set_state(user_id=message.from_user.id, state=StateSettings.settings, chat_id=message.chat.id)

    elif 'Количество звезд:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text='Выберите количество звезд:',
                         reply_markup=list_stars())
        bot.set_state(user_id=message.from_user.id, state=StateSettings.settings, chat_id=message.chat.id)

    elif 'Минимальная цена за ночь:' in message.text:
        current_currency = get_settings(user_id=str(message.from_user.id))['currency']
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Введи минимальную стоимость в {current_currency}\n'
                              'Отправь "0" чтобы отключить этот фильтр')
        bot.set_state(user_id=message.from_user.id, state=StateSettings.min_price, chat_id=message.chat.id)

    elif 'Максимальная цена за ночь:' in message.text:
        current_currency = get_settings(user_id=str(message.from_user.id))['currency']
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Введи максимальную стоимость в {current_currency}\n'
                              'Отправь "0" чтобы отключить этот фильтр')
        bot.set_state(user_id=message.from_user.id, state=StateSettings.max_price, chat_id=message.chat.id)

    elif 'Количество взрослых:' in message.text:
        bot.set_state(user_id=message.from_user.id,
                      state=StateSettings.adulst,
                      chat_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Отправь мне количество взрослых')

    elif 'Количество детей:' in message.text:
        bot.set_state(user_id=message.from_user.id,
                      state=StateSettings.children,
                      chat_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Отправь мне количество детей')

    elif 'Удобства:' in message.text:
        pass

    elif 'Минимальное расстояние до центра:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Выберите:',
                         reply_markup=distance(min_distance=None,
                                               max_distance=max_distance))
        bot.set_state(user_id=message.from_user.id, state=StateSettings.min_distance, chat_id=message.chat.id)

    elif 'Максимальное расстояние до центра:' in message.text:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Выберите:',
                         reply_markup=distance(min_distance=min_distance,
                                               max_distance=None))
        bot.set_state(user_id=message.from_user.id, state=StateSettings.max_distance, chat_id=message.chat.id)

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
