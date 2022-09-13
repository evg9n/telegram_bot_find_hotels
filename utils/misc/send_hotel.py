from loader import bot
from utils.misc.rapid_api import get_details_hotel, find_hotels
from keyboards.inline.info_hotel import gen_murkup
from telebot.types import InputMediaPhoto
from states.state_find import StateFind
from database.write_database import write_history, add_user, check_hotel_favorite
from sqlite3 import OperationalError


def send_hotel(user_id: int, chat_id: int, back: bool, message_id=None) -> None:
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:

        if data['number'] == -1:
            if data['sort_top'] != 'free':
                currency = data['settings']['currency']
                data['list_hotels'] = find_hotels(city_id=data['city_id'], check_in=data['check_in'],
                                                  check_out=data['check_out'], sort_order=data['sort_top'],
                                                  currency=currency, min_guest_rating='8',
                                                  amenity='0', star_rating='5', min_price=None, max_price=None,
                                                  min_distance=None, max_distance=None)
            else:
                currency = data['settings']['currency']
                sort_order = data['settings']['sort']
                min_guest_rating = data['settings']['min_guest_rating']
                amenity = data['settings']['amenity']
                star_rating = data['settings']['star_rating']
                min_price = data['settings']['min_price']
                min_price = min_price if min_price != '0' else '1'
                max_price = data['settings']['max_price']
                max_price = max_price if max_price != '0' else None
                min_distance = data['settings']['min_distance']
                min_distance = min_distance if min_distance != '-' else None
                max_distance = data['settings']['max_distance']
                max_distance = max_distance if max_distance != '-' else None
                data['list_hotels'] = find_hotels(city_id=data['city_id'], check_in=data['check_in'],
                                                  check_out=data['check_out'], sort_order=sort_order,
                                                  currency=currency, min_guest_rating=min_guest_rating,
                                                  amenity=amenity, star_rating=star_rating,
                                                  min_price=min_price, max_price=max_price,
                                                  min_distance=min_distance, max_distance=max_distance)
        if data['list_hotels']:

            if back:
                if data['number'] > 0:
                    data['number'] -= 1
                else:
                    return
            else:
                if data['number'] < len(data["list_hotels"]) - 1:
                    data['number'] += 1
                else:
                    return

            result = get_details_hotel(hotel_id=data['list_hotels'][data['number']]['id'],
                                       check_in=data['check_in'],
                                       check_out=data['check_out'])
            if result:
                result['other'] = data['list_hotels'][data['number']]
                data['photos_hotel'] = result['photos_hotel']
                data['photos_rooms'] = result['photos_rooms']

                photo = data['photos_hotel'][0]

                text = f'Отель: {result["name"]} {int(result["rating"]) * "⭐"}\n' \
                       f'Рейтинг: {result["other"]["rating"]}\n' \
                       f'Стоимость за ночь: {result["other"]["price"]} {data["settings"]["currency"]}\n' \
                       f'Общая стоимость: ' \
                       f'{result["other"]["price"] * data["nights"]} {data["settings"]["currency"]}\n' \
                       f'Адрес: {result["address"]}\n' \
                       f'До центра города: {result["other"]["center"]}\n' \
                       f'Ночей: {data["nights"]}'
                coordinate = data['list_hotels'][data['number']]['coordinate']

                try:
                    write_history(user_id=str(user_id), hotel_id=data['list_hotels'][data['number']]['id'],
                                  check_in=data['check_in'], check_out=data['check_out'], info=text,
                                  url=f'hotels.com/ho{data["list_hotels"][data["number"]]["id"]}',
                                  photo=photo, coordinate_lat=coordinate['lat'], coordinate_lon=coordinate['lon'])
                except OperationalError:
                    add_user(user_id=str(user_id))
                    write_history(user_id=str(user_id), hotel_id=data['list_hotels'][data['number']]['id'],
                                  check_in=data['check_in'], check_out=data['check_out'], info=text,
                                  url=f'hotels.com/ho{data["list_hotels"][data["number"]]["id"]}',
                                  photo=photo, coordinate_lat=coordinate['lat'], coordinate_lon=coordinate['lon'])

                try:

                    favorite = check_hotel_favorite(user_id=user_id,
                                                    hotel_id=data["list_hotels"][data["number"]]["id"])
                except OperationalError:
                    add_user(str(user_id))
                    favorite = check_hotel_favorite(user_id=user_id,
                                                    hotel_id=data["list_hotels"][data["number"]]["id"])

                data['favorite'] = favorite
                data['info'] = text
                favorite = '❤' if favorite else '🖤'
                if data['number'] == 0 and not back:

                    bot.delete_message(chat_id=user_id, message_id=message_id)

                    bot.send_message(chat_id=user_id,
                                     text=f'Найдено отелей: {len(data["list_hotels"])}')

                    bot.send_photo(chat_id=user_id,
                                   photo=photo,
                                   caption=text,
                                   reply_markup=gen_murkup(
                                       current=data['number'] + 1,
                                       total=len(data["list_hotels"]),
                                       url=f'hotels.com/ho{data["list_hotels"][data["number"]]["id"]}',
                                       favorite=favorite)
                                   )
                else:
                    media = InputMediaPhoto(media=photo,
                                            caption=text)
                    bot.edit_message_media(media=media, chat_id=user_id, message_id=message_id,
                                           reply_markup=gen_murkup(
                                            current=data['number'] + 1,
                                            total=len(data["list_hotels"]),
                                            url=f'hotels.com/ho{data["list_hotels"][data["number"]]["id"]}',
                                            favorite=favorite))
            else:
                if back:
                    data['number'] += 1
                else:
                    data['number'] -= 1

        else:
            bot.delete_message(chat_id=user_id, message_id=message_id)
            bot.send_message(chat_id=user_id,
                             text=f'Отели в {data["city"]} не нашел 😞\n'
                                  'Попробуйте другой')

            bot.set_state(user_id=user_id,
                          state=StateFind.city,
                          chat_id=chat_id)
