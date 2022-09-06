import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    RAPID_API_KEY = os.getenv('RAPID_API_KEY')
    DEFAULT_COMMANDS = (
        ('survey', " опрос"),
        ('lowprice', "получить список отелей с сортировкой   - от самых дешёвых"),
        ('highprice', "получить список отелей с сортировкой - от самых дорогих"),
        ('bestdeal', "лучший выбор"),
        ('history', "история запросов"),
        ('help', "Вывести справку")
    )
