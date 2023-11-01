from datetime import datetime
from peewee import *

# import os

db_filename = 'database/bot_history.db'
db = SqliteDatabase(db_filename)


class Person(Model):
    user_id = int()
    datetime = datetime

    class Meta:
        database = db  # This model uses the "people.db" database.


class Command(Model):
    owner = ForeignKeyField(Person, backref='commands')
    date_time = datetime
    selected_command = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.create_tables([Person, Command])


def history_put(user_id, command):
    print("selected history_put with params:", user_id, command)
    db.connect()
    db.create_tables([Person, Command])

    user1 = Person.create(user_id=123456)

    user1_command1 = Command.create(user_id=123456, datetime=datetime.now(), selected_command="/highprice")
    user1_command2 = Command.create(user_id=123456, datetime=datetime.now(), selected_command="/lowhprice")
    user2_command1 = Command.create(user_id=123456, datetime=datetime.now(), selected_command="/lowhprice")
    user2_command2 = Command.create(user_id=123456, datetime=datetime.now(), selected_command="/bestdeal")
    db.close()
    return ()


def history_list(user_id):
    print("selected history_list with params:", user_id)
    # query = Person.select().order_by(Person.name).prefetch(Command)
    query = Command.select()
    for i in query:
        print('date_time=', i.date_time, 'owner.name', i.owner.name, end='       ')
        print('selected_command', i.selected_command)
    db.close()

# if os.path.isfile(db_filename):
#    os.remove(db_filename)
