import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('lowprice', 'Вывод самых дешёвых отелей в городе'),
    ('highprice', 'Вывод самых дорогих отелей в городе'),
    ('bestdeal', 'Поиск отелей по установленным фильтрам'),
    ('history', 'История поиска'),
    ('settings', 'Настройки'),
    ('favorites', 'Избранные отели'),
    ('help', "Вывести справку")
)
