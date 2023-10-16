import datetime

from peewee import *
from datetime import date
import os

db_filename = 'bot_history.db'
db = SqliteDatabase(db_filename)


class Person(Model):
    name = CharField()
#    id = int()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Command(Model):
    owner = ForeignKeyField(Person, backref='user_id')
    date_time = CharField()
#    owner = ForeignKeyField(Person, backref='Commands')
    name = CharField()
    selected_command = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Command])

user1 = Person.create(name='Alice')
# user2 = Person.create(name='Bob',   id=234234)
# user3 = Person.create(name='Peter', id=345345)


#bob_kitty = Command.create(owner=user2, name='Kitty', selected_command='cat')
# user1_kitty = Command.create(owner=user1, name='Kitty2', selected_command='cat')
user1_command1 = Command.create(date_time=str(datetime.date) + str(datetime.time), name="Alise", selected_command="highprice")
#user3_fido = Command.create(owner=user3, name='Fido', selected_command='dog')
#user3_mittens = Command.create(owner=user3, name='Mittens', selected_command='cat')
#user3_mittens_jr = Command.create(owner=user3, name='Mittens Jr', selected_command='cat')


# query = Person.select().order_by(Person.name).prefetch(Command)
query = Person.select()

for attr in Command.owner:
#    if not attr.startswith('__'):
    print(str(attr) + ' value= ' + Command.name)
    print(attr)
    print(type(attr))

'''for person in query:
    print('person.name=', person.name)
    for Command in person.Commands:
        print('  *', Command.name)
'''
db.close()
if os.path.isfile(db_filename):
    os.remove(db_filename)
