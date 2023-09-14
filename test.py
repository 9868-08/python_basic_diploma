# from peewee import *
from database.bot_database import Command


from datetime import date
# current_command = Command(name='/highprice', birthday=date(1960, 1, 15))
# current_command.save()     # bob is now stored in the database
new_command = Command.create(name='/highprice', birthday=date(1960, 1, 15))

for command in Command.select():
    print(command.name)

