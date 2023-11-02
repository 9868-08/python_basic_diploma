from datetime import datetime
from peewee import *

# import os

db_filename = 'database/bot_history.db'
db = SqliteDatabase(db_filename)


class Person(Model):
    user_id = int()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Command(Model):
    owner = ForeignKeyField(Person, backref='commands')
    date_time = datetime
    selected_command = CharField()
    result = list()

    class Meta:
        database = db  # this model uses the "people.db" database


db.create_tables([Person, Command])


def history_put(user_id, command, result):
    print("selected history_put with params:", user_id, command)
    db.connect()
    db.create_tables([Person, Command])
    print('user1',  user_id, 'datetime=', datetime.now(), 'selected_command=', command, result)
    user1 = Person.create(user_id=user_id, datetime=datetime.now(), selected_command=command)
#   Grandma_kitty = Pet.create(owner='Grandma', name='Kitty2', animal_type='cat')
    command1 = Command.create(owner=user_id, datetime=datetime.now(), command=command, result=result)
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
