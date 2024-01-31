from database.bot_database import db, User, Command


# создает пустую базу данных
db.create_tables([User, Command])
