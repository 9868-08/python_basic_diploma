from peewee import *

db = SqliteDatabase('database/bot_history.db')


class Command(Model):
    command = CharField()
    date = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.
