import os
#import datetime
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку")
)


#import datetime
#MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
#MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')
#time_offset = datetime.timezone(datetime.timedelta(hours=3))

DEFAULT_COMMANDS = (
    ('help', "Вывести справку"),
    ('start', "Поздороваться"),
    ('lowprice',  'Узнать топ самых дешёвых отелей в городе'),
    ('highprice', 'Узнать топ самых дорогих отелей в городе'),
    ('bestdeal',  'Узнать топ отелей, наиболее подходящих по цене и расположению от центра (самые дешёвые и находятся ближе всего к центру)'),
    ('history',   'Узнать историю поиска отелей')
)
#time_offset = datetime.timezone(datetime.timedelta(hours=3))

#Для команд lowprice, highprice
# 1. Город, где будет проводиться поиск.
# 2. Количество отелей, которые необходимо вывести в результате (не больше заранее определённого максимума).
# 3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
#   a. При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
