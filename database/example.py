from peewee import *
from datetime import date
import os

myfilename = 'bot_history.db'
db = SqliteDatabase(myfilename)


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Pet])

grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
uncle_bob = Person.create(name='Bob', birthday=date(1950, 5, 5))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

# To update a row, modify the model instance and call save() to persist the changes. Here we will change Grandma’s name and then save the changes in the database:
grandma.name = 'Grandma L.'
grandma.save()  # Update grandma's name in the database.

# Now we have stored 3 people in the database. Let’s give them some pets. Grandma doesn’t like animals in the house, so she won’t have any, but Herb is an animal lover:
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
Grandma_kitty = Pet.create(owner='Grandma', name='Kitty2', animal_type='cat')
query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)

# print(Pet)
# print(str(attr) + ' value= ' + getattr(classobject, attr))

herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

# After a long full life, Mittens sickens and dies. We need to remove him from the database:
# herb_mittens.delete_instance() # he had a great life
# The return value of delete_instance() is the number of rows removed from the database.

# Uncle Bob decides that too many animals have been dying at Herb’s house, so he adopts Fido:
herb_fido.owner = 'Grandma'
herb_fido.save()

# Getting single records
# grandma = Person.select().where(Person.name == 'Grandma L.').get()
# We can also use the equivalent shorthand Model.get():
# grandma = Person.get(Person.name == 'Grandma L.')

#query = Person.select().order_by(Person.name).prefetch(Pet)
query = Person.select()
for person in query:
    print('person.name=', person.name)
    for pet in person.pets:
        print('  *', pet.name)


db.close()
if os.path.isfile(myfilename):
    os.remove(myfilename)
