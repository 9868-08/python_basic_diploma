from peewee import *
import time

db = SqliteDatabase('database/diploma.db')


class Hotel_search(Model):
    machine_time = CharField()
    command = str

    class Meta:
        database = db


def record_append(command_requested: str):
    obj = time.gmtime(0)
    curr_time = round(time.time() * 1000)
    print("Milliseconds since epoch:", curr_time)
    new_db_record = Hotel_search(machine_time=curr_time, command=command_requested)
    new_db_record.save()
    return
