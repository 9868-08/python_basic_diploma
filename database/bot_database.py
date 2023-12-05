from playhouse.sqlite_ext import JSONField
from datetime import datetime
from peewee import *

# import os

db_filename = 'database/bot_history.db'
db = SqliteDatabase(db_filename)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    # Для каждого поля используется класс из peewee, а не стандартный тип python
    name = CharField()
    telegram_id = IntegerField(unique=True)


class Command(BaseModel):
    owner = ForeignKeyField(User, backref='commands')
    #    my_datetime = DateTimeField()
    my_datetime = DateTimeField()
    selected_command = CharField()
    result = JSONField()


def check_user_in_db(telegram_id):
    print("selected check_user_in_db", telegram_id)
    while True:
        result = list()
        query = Command.select()
        for i in query:
            result_tmp = (str(i.my_datetime), i.owner.name, i.owner.telegram_id, i.selected_command, i.result)
            print('date_time=', str(i.my_datetime), 'name=', i.owner.name, 'relegram_id=', i.owner.telegram_id,
                  'owner_id', i.owner_id, 'selected_command', 'owner_id', i,
                  'selected_command', i.selected_command, 'searching_result=', i.result)
            result.append(result_tmp)
            if i.owner.telegram_id == telegram_id:
                return i.owner.id
        db.close()
        return None


def history_put(telegram_id, full_name, command, result):
    user_id = check_user_in_db(telegram_id)
    if user_id is None:
        user1 = User.create(
            name=full_name,
            telegram_id=telegram_id
        )
        user_id = user1.id
    Command.create(
        owner=user_id,
        my_datetime=datetime.now().strftime("%y.%m.%d %H:%M"),
        selected_command=command,
        result=result)
    return ()


def history_list(user_id):
    print("selected history_list with params:", user_id)
    result = list()
    query = Command.select()
    for i in query:
        if i.owner.telegram_id == user_id:
            result_tmp = (i.selected_command, str(i.my_datetime), i.result)
            result.append(result_tmp)
    db.close()
    return result

# if os.path.isfile(db_filename):
#    os.remove(db_filename)
