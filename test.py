from peewee import *
from datetime import date

db = SqliteDatabase('database/bot_history.db')


class Command(Model):
    command = CharField()
    date = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.

'''    def __int__(self):
        db.create_tables(['command_history'])

    def create(self, command_name, date_time=(1960, 1, 15)):
        print("adding: " + str(date_time) + ": " + str(command_name))
        pass

    def select(self):
        print("searching")
        return ()'''


# current_student = Student()
my_command = Command("1")  # экземпляр класса Student
# current_command = Command(name='/highprice', birthday=date(1960, 1, 15))
# current_command.save()     # bob is now stored in the database
Command.create("", '/highprice', date(2023, 9, 16))
Command.create("", '/lowprice', date(1923, 9, 10))

for Command in Command.select(""):
    print(Command.name)
