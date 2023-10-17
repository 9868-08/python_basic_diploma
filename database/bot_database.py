import datetime

from peewee import *
import os

db_filename = 'bot_history.db'
db = SqliteDatabase(db_filename)


class Person(Model):
    name = CharField()
#    command_id = int()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Command(Model):
    owner = ForeignKeyField(Person, backref='commands')
    date_time = DateTimeField(default=datetime.datetime.utcnow())
    selected_command = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Command])

user1 = Person.create(name='Alice')
user2 = Person.create(name='Bob')

user1_command1 = Command.create(owner=user1, name="Alise", selected_command="highprice")
user1_command2 = Command.create(owner=user1, name="Alise", selected_command="lowhprice")
user2_command1 = Command.create(owner=user2, name="Alise", selected_command="lowhprice")
user2_command2 = Command.create(owner=user2, name="Alise", selected_command="bestdeal")


# query = Person.select().order_by(Person.name).prefetch(Command)
query = Command.select()
for i in query:
    print('date_time=', i.date_time,'owner.name', i.owner.name, end='       ')
    print('selected_command', i.selected_command)

db.close()
if os.path.isfile(db_filename):
    os.remove(db_filename)
