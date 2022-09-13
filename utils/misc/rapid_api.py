from requests import get, codes, Response
from requests.exceptions import ReadTimeout
from config_data.config import RAPID_API_KEY
from utils.misc.url import RAPID_API_HOST, URL_API_SEARCH, \
    URL_API_LIST, URL_API_GET_PHOTOS, URL_API_GET_DETAILS, photo_hotel
from re import sub
from typing import Dict, List, Optional, Union


def rapid_api(url: str, querystring: dict) -> Optional[Response]:

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    try:
        responce = get(url, headers=headers, params=querystring, timeout=30)
    except ReadTimeout:
        return None

    if responce.status_code == codes.ok:

        return responce

    elif responce.status_code == 429:
        print(f'Статус  запроса {responce.status_code}\nПревышен лимит запросов')
        return None

    else:
        print(f'Ошибка запроса, статус  запроса {responce.status_code}')
        return None


def find_city(city: str) -> Optional[Dict]:
    parametrs = {
        "query": city,
        "locale": "ru_RU"
    }

    query = rapid_api(url=URL_API_SEARCH, querystring=parametrs)
    if not query:
        return None

    if query.json().get('suggestions')[0].get('entities'):
        city = dict()

        for elem in query.json().get('suggestions')[0].get("entities"):
            if elem.get("name") not in city:
                name = str(elem.get('name'))[0:64]
                destination_id = elem.get('destinationId')
                city[destination_id] = name

        return city

    else:
        return None


def find_hotels(city_id: Union[str, int], check_in: str, check_out: str, sort_order: str,
                currency: str, min_guest_rating: str, amenity: Optional[str], star_rating: str,
                min_price: Optional[str], max_price: Optional[str],
                min_distance: Optional[str]=None, max_distance: Optional[str]=None) -> Optional[List]:

    parametrs = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                 "checkOut": check_out, "adults1": "1", "children1": "4", "starRatings": star_rating,
                 "priceMin": min_price, "priceMax": max_price, "sortOrder": sort_order,
                 "locale": "ru_RU", "currency": currency, "guestRatingMin": min_guest_rating, "amenityIds": amenity
                 }

    query = rapid_api(url=URL_API_LIST, querystring=parametrs)
    if not query:
        return None

    results = list()

    try:
        for element in query.json().get("data").get("body").get("searchResults").get("results"):

            if 'guestReviews' in element and 'ratePlan' in element:
                hotel_id = element.get('id')
                price = element.get('ratePlan').get('price').get('exactCurrent')
                center = element.get('landmarks')[0].get('distance') \
                    if element.get('landmarks')[0].get('label') == 'Центр города' \
                    else 'неизвестно'

                if bool(min_distance or max_distance):

                    if center != 'неизвестно':

                        if min_distance:
                            if float(sub(',', '.', center[:len(center) - 3])) < float(min_distance):
                                continue

                        if max_distance:
                            if float(sub(',', '.', center[:len(center) - 3])) > float(max_distance):
                                continue
                    else:
                        continue

                coordinate = {'lat': element.get('coordinate').get('lat'), 'lon': element.get('coordinate').get('lon')}
                rating = element.get('guestReviews').get('rating')

                hotel = {
                    'id': hotel_id,
                    'price': int(price),
                    'center': center,
                    'rating': rating,
                    'coordinate': coordinate
                }
                results.append(hotel)
    except AttributeError:
        results = None

    return results if results else None


def get_details_hotel(hotel_id: Union[str, int], check_in: str, check_out: str,
                      currency='RUB', locale='ru_RU') -> Optional[Dict]:

    parametrs = {"id": hotel_id, "checkIn": check_in, "checkOut": check_out,
                 "adults1": "1", "currency": currency, "locale": locale}

    query = rapid_api(url=URL_API_GET_DETAILS, querystring=parametrs)
    if not query:
        return None
    element = query.json().get('data').get('body')

    try:
        photos_hotel, photos_rooms = get_photos(hotel_id=hotel_id).values()
    except AttributeError:
        photos_hotel, photos_rooms = None, None

    result = {
        'name': element.get('propertyDescription').get('name'),
        'rating': element.get('propertyDescription').get('starRating'),
        'address': element.get('propertyDescription').get('address').get('fullAddress'),
        'photos_hotel': photos_hotel if photos_hotel else [photos_hotel],
        'photos_rooms': photos_rooms
    }
    return result if result else None


def get_photos(hotel_id: Union[str, int]) -> Optional[Dict]:
    parametrs = {"id": hotel_id}
    query = rapid_api(url=URL_API_GET_PHOTOS, querystring=parametrs)
    if not query:
        return None
    query = query.json()
    result = dict()
    result['hotel'] = list()
    result['rooms'] = list()

    if 'hotelImages' in query:
        try:
            for element in query.get('hotelImages'):
                url = element.get('baseUrl')
                url = sub(pattern=r'{size}', repl=f'{element.get("sizes")[0].get("suffix")}', string=url)
                result['hotel'].append(url)
        except AttributeError:
            result['hotel'].append(photo_hotel)

    if 'roomImages' in query:
        try:
            for room in query.get('roomImages'):
                elements = list()
                for element in room.get('images'):
                    url = element.get('baseUrl')
                    url = sub(pattern=r'{size}', repl=f'{element.get("sizes")[0].get("suffix")}', string=url)
                    elements.append(url)
                result['rooms'].append(elements)
        except AttributeError:
            result['rooms'] = list(photo_hotel)

    if not result['hotel']:
        result['hotel'].append(photo_hotel)

    if not result['rooms']:
        result['rooms'] = list(photo_hotel)
    return result
