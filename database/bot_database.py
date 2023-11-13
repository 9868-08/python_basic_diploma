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
    telegram_id = IntegerField()


class Command(BaseModel):
    owner = ForeignKeyField(User, backref='commands')
    #    my_datetime = DateTimeField()
    my_datetime = DateField(default=datetime.now().strftime("%d.%m.%Y"))
    selected_command = CharField()
    result = list()


db.create_tables([User, Command])


def history_put(user_id, full_name, command, result):
    print("selected history_put with params:", user_id, command)
    db.connect(reuse_if_open=True)
    db.create_tables([User, Command])
    print('user1', user_id, 'name=', full_name, 'selected_command=', command, result)
    user1 = User.create(
            name=full_name,
            telegram_id=user_id
        )
    command1 = Command.create(owner=user_id, datetime=datetime.now(), selected_command=command, result=result)
    db.close()
    return ()


def history_list(user_id):
    print("selected history_list with params:", user_id)
    # query = User.select().order_by(User.name).prefetch(Command)
    result = list()
    query = Command.select()
    for i in query:
        result_inside = (str(i.my_datetime), i.owner_id, i.selected_command)
        print('date_time=', str(i.my_datetime), 'owner_id', i.owner_id, 'selected_command', i.selected_command)
        result.append(result_inside)
    db.close()
    return result

# if os.path.isfile(db_filename):
#    os.remove(db_filename)
