from datetime import datetime
import json
from datetime import datetime


class My_json():
    def __init__(self):
        self.datetime = str()
        self.command = str()

    def __str__(self):
        return str(self.datetime) + "\t\t" + str(self.command)

    def append(self, json_file, str_to_append):
        with open(logfile, 'w') as f:
            json.dump(str_to_append, indent=4)  # сериализация JSON
#            f.write(json.dumps(my_json))
        f.close()


my_json = My_json()
logfile = "diploma_log.json"

str_to_append = dict()

now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#print("date and time:",date_time)

command = "lowprice"

str_to_append = {'08/07/2022, 17:44:03': 'highprice'}


print(str_to_append)

with open(logfile, 'a') as f:
    json.dump(str_to_append, f, indent=4)  # сериализация JSON

f.close()

import telebot, wikipedia, re
# Создаем экземпляр бота
bot = telebot.TeleBot('Здесь впиши токен, полученный от @botfather')
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))
# Запускаем бота
bot.polling(none_stop=True, interval=0)
