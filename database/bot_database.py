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
    result = (
        Command
        .select()
        .join(User)
        .where(User.telegram_id == telegram_id)
    ).get_or_none()
    db.close()
    if result:
        return result.id
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


def history_list(user_telegram_id):
    print("selected history_list with params:", user_telegram_id)
    user_id = check_user_in_db(user_telegram_id)
    result_lst = list()
    query = Command.select()
    result = (
        Command
        .select()
        .join(User)
        .where(User.telegram_id == user_telegram_id)
    ).get()
    for i in query:
        result_tmp = (i.selected_command, str(i.my_datetime), i.result)
        result_lst.append(result_tmp)
    db.close()
    return result_lst

# if os.path.isfile(db_filename):
#    os.remove(db_filename)
