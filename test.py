from database.bot_database import *
from peewee import *


db_filename = 'database/bot_history.db'
db = SqliteDatabase(db_filename)
my_flag = "True"
while my_flag == "True":
    result = list()
    query = Command.select()
    for i in query:
        result_tmp = (str(i.my_datetime), i.owner.name, i.owner.telegram_id, i.selected_command, i.result)
        print('date_time=', str(i.my_datetime), 'name=', i.owner.name, 'relegram_id=', i.owner.telegram_id,
              'owner_id', i.owner_id, 'selected_command', 'owner_id', i,
              'selected_command', i.selected_command, 'searching_result=', i.result)
        result.append(result_tmp)
        if i.owner.telegram_id == 418832166:
            my_flag = "False"
db.close()
