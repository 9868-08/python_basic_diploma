***

![image](header_image.png) 

# Roman Ermolaev diploma

## What does the bot do?

***

+ **находит отели по всему миру**
+ **показывает фотографии отелей**
+ **определяет расположение отелей**
+ **гибкая система поиска отелей**
+ **сохраняет историю поиска пользователя в базу**

### [Test the bot](https://t.me/python_basic_final_bot "Go to Telegram")


## Commands

***

+ /help

> *показать команды бота*

+ /lowprice

> *Запрашивает город, дату заезда/выезда и находит отели в городе от самых дешёвых к более дорогим

+ /highprice

> *Запрашивает город, дату заезда/выезда и находит отели в городе от самых дорогих в более дешёвым

+ /bestdeal

> *Запрашивает город, дату заезда/выезда, минималььное и максимальное расстояние от центра и находит отели в городе

+ /history

> *выводи историю поиска пользователя  

## Requirements

***

+ python-dotenv==0.21.1
+ telebot~=0.0.4
+ requests~=2.28.2
+ peewee
+ loguru
+ jsonpickle
+ python-telegram-bot
+ python-telegram-bot-calendar


## Preparation and Launch

***

1. Create your bot using the bot [@BotFather](https://t.me/BotFather ) and save your token
2. Register in the cloud service [MongoDB Atlas](https://www.mongodb.com/atlas/database)

> *For users from Russia, registration is possible using a VPN.  
You can add Russian IP addresses to the list of IP addresses that have access to the database.*

3. Create a file.env in the program directory and fill it in according to .env.template

> *In the environment variables RAPID_API_KEY and ANOTHER_RAPID_API_KEY, two different keys should be specified for operation with the Hotels API (Or leave only RAPID_API_KEY, if you are sure that 500 requests per month will be enough).  
The REQUESTS_LIMIT_REACHED parameter is "False" by default, there is no need to change it.  
These parameters are created to change the API key when the request limit is used up*

4. If you need to add your own exceptions, in which the user returns to the main menu, use the functions from the
   file [work_with_errors.py ](/utils/misc/work_with_errors.py )
5. Messages sent using commands contain photos for decoration.  
   ![message_with_photo_example](message_with_photo_template.png)

> *For convenience, photos are stored in Telegram. Sending is possible by the file_id of the photo. You can change photos to your own in the file [photos_in_telegram.py ](/photos/main_menu.png)  
To get the file_id of your photo, use the following script:*


> *The file id of the photo you sent to the bot will be output to the console. Now you can use the photo by its file id, storing it in Telegram.*
