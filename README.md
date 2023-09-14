СУБД sqlite через PEEWE ORM (https://docs.peewee-orm.com/en/latest/)

message_handler обрабатывает обычные сообщения (события)
callback_query_handler обрабатывает нажатия на inline кнопки

locations/v3/search - поиск локации по названию  
properties/v2/list - получение списка отелей по региону  
properties/v2/detail - подробнее об отеле - адрес, фотки



src: https://github.com/9868-08

# Roman Ermolaev diploma

***
![image](readme_header_image.png)

## What does the bot do?

***

+ **Finds hotels all over the world**
+ **Finds and sends photos of hotels**
+ **Sends geolocation of hotels**
+ **Enables flexible hotel search**
+ **Records the user's search history in the database**
+ **Allows the user to add the found hotels to the favorites list**

### [Test the bot](https://t.me/BetterThanBookingBot/ "Go to Telegram")

## Features

***

+ The bot is **asynchronous**. From the library for working with Telegram to database queries.
+ Work with the database is carried out through **cloud
  service** [MongoDB Atlas](https://www.mongodb.com/atlas/database ).
+ Work with **two** API keys of [RapidAPI](https://rapidapi.com/apidojo/api/hotels4/) is provided instead of one.
+ Implemented the logic of working with selected hotels. **There are no conflicts** with the work of the search history.
+ A convenient system for returning to the main menu has been created, with the creation of **your own messages** in
  case of errors.
+ The bot uses special **photos** when sending messages. Made exclusively for **decorative** purposes.

## Commands

***

+ /start

> *Used to reset the current state of the bot and return to the main menu*

+ /help

> *Sends the user a help with a description of the commands and work with the bot*

+ /lowprice

> *Requests the city to search for hotels, offers the found options for cities, requests dates of stay.*  
*Sends the found hotels in descending order of price*

+ /highprice

> *Requests the city to search for hotels, offers the found options for cities, requests dates of stay.*  
*Sends the found hotels in ascending order of price*

+ /bestdeal

> *Requests the city to search for hotels, offers the found city options, requests dates of stay, minimum and maximum cost, maximum distance from the city center*  
*Sends the found hotels that match the search conditions*

+ /history

> *Sends the user a history in the format:*  
*The name of the command, the name of the city, the date and time of the command call, the button for viewing the found hotels (if any)*

+ /favorites

> *Sends the hotels added to the favorites to the user*

## Requirements

***

+ Python 3.9 and newer
+ aiogram 2.21
+ aiohttp 3.8.1
+ python-telegram-bot-pagination 0.0.2
+ python-telegram-bot-calendar 1.0.5
+ pymongo 4.2.0
+ motor 3.0.0
+ dnspython 2.2.1
+ python-dotenv 0.19.2

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

```python
from aiogram.types.message import Message
from aiogram.types.photo_size import PhotoSize

from loader import dp


@dp.message_handler(content_types=['photo'])
async def get_photo_id(message: Message):
    photo_sizes: list[PhotoSize] = message.photo

    # Index -1 to get the id of the photo in the maximum resolution
    file_id: str = photo_sizes[-1].file_id
    print(file_id)
```

> *The file id of the photo you sent to the bot will be output to the console. Now you can use the photo by its file id, storing it in Telegram.*
