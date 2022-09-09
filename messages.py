from utils import TestStates


help_message = "1. Узнать топ самых дешёвых отелей в городе (команда /lowprice). \n2. Узнать топ самых дорогих отелей в городе (команда /highprice). \n3. Узнать топ отелей, наиболее подходящих по цене и расположению от центра (самые дешёвые и находятся ближе всего к центру) (команда /bestdeal).\n4. Узнать историю поиска отелей (команда /history)."

start_message = 'Привет! Это демонстрация работы .\n' + help_message
invalid_key_message = 'Ключ "{key}" не подходит.\n' + help_message
state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'

MESSAGES = {
    'highprice': start_message,
    'help': help_message,
    'invalid_key': invalid_key_message,
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
}
