from database.bot_database import db, User, Command

db.create_tables([User, Command])
