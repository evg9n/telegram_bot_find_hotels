from os.path import join


RAPID_API_HOST = "hotels4.p.rapidapi.com"
URL_API_SEARCH = 'https://hotels4.p.rapidapi.com/locations/v2/search'
URL_API_LIST = "https://hotels4.p.rapidapi.com/properties/list"
URL_API_GET_DETAILS = 'https://hotels4.p.rapidapi.com/properties/get-details'
URL_API_GET_PHOTOS = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
path_base = join('database', 'users.db')
photo_hotel = 'https://lovibiletik.ru/wp-content/uploads/2019/07/Hotels.com3_.jpg'
dict_sort = {
    'BEST_SELLER': 'бестселлер',
    'STAR_RATING_HIGHEST_FIRST': 'звездный рейтинг самый высокий первый',
    'STAR_RATING_LOWEST_FIRST': 'звездный рейтинг самый низкий сначала',
    'DISTANCE_FROM_LANDMARK': 'расстояние от достопримечательности',
    'GUEST_RATING': 'гостевой рейтинг',
    'PRICE_HIGHEST_FIRST': 'цена самая высокая сначала',
    'PRICE': 'цена самая низкая сначала'}
currency_dict = {'Рубль РФ': 'RUB',
                 'Доллар США': 'USD',
                 'Белорусский рубль': 'BYR',
                 'Украинская гривна': 'UAH',
                 'Валюта ЕС': 'EUR'}
dict_guest_rating = {
    '0': 'Не установлено',
    '1': '1+',
    '2': '2+',
    '3': '3+',
    '4': '4+',
    '5': '5+',
    '6': '6+',
    '7': '7+',
    '8': '8+',
    '9': '9+',
    '10': '10',
}
dict_stars = {
    '0': 'Не установлено',
    '1': '⭐',
    '2': '⭐⭐',
    '3': '⭐⭐⭐',
    '4': '⭐⭐⭐⭐',
    '5': '⭐⭐⭐⭐⭐'
}
