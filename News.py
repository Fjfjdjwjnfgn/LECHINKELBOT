import telebot
from telebot import types
import random
import logging
import json
import time

TOKEN = '8501222332:AAG4yM_GDfB3TpJ-uikLTL5fE8FJsuqxD8g'
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.DEBUG)

def load_bot_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON: {e}")
        return {}

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as file:
        json.dump(bot_data, file, ensure_ascii=False, indent=4)

bot_data = load_bot_data()

cards = [
    {
        "name": "NerestPC", #софт
        "rarity": "Редкий", #редкость
        "points": 1000, #очки
        "coins": 5, # монеты
        "image_url": 'https://yt3.googleusercontent.com/xoxhBaTHrDunGdL55gTRrikV6dL8yCI2re4oYwCJry-3W2h7HjcuEsVC0qYZ8YczOI5MQWhGSQ=s900-c-k-c0x00ffffff-no-rj', # ссылка на фото 
    },
    {
        "name": "Plutonium",
        "rarity": "Эпический",
        "points": 3000,
        "coins": 10,
        "image_url": 'https://imgur.com/a/zvA1gd1',
    },
    {
        "name": "Ezteam",
        "rarity": "Редкий",
        "points": 1000,
        "coins": 5,
        "image_url": 'https://imgur.com/a/cl4WKfG',
    },
    {
        "name": "MainPC",
        "rarity": "Обычный",
        "points": 500,
        "coins": 3,
        "image_url": 'https://imgur.com/a/wbCWT5q',
    },
    {
        "name": "HellPC",
        "rarity": "Редкий",
        "points": 1000,
        "coins": 5,
        "image_url": 'https://imgur.com/a/Zjq5Up2',
    },
    {
        "name": "BrutalPC",
        "rarity": "Обычный",
        "points": 500,
        "coins": 3,
        "image_url": 'https://imgur.com/a/BjfsXnF',
    },
    {
        "name": "NerestExternal",
        "rarity": "Редкий",
        "points": 1000,
        "coins": 5,
        "image_url": 'https://imgur.com/a/8UOD14T',
    },
    {
        "name": "A4Hook",
        "rarity": "Редкий",
        "points": 1000,
        "coins": 5,
        "image_url": 'https://imgur.com/a/MqHhIeX',
    },
    {
        "name": "Astral",
        "rarity": "Обычный",
        "points": 500,
        "coins": 3,
        "image_url": 'https://imgur.com/a/uMQKuNg',
    },
    {
        "name": "Omniscient",
        "rarity": "Эпический",
        "points": 3000,
        "coins": 10,
        "image_url": 'https://imgur.com/a/HgYLcCk',
    },
    {
        "name": "Lunacy",
        "rarity": "Легендарный",
        "points": 10000,
        "coins": 30,
        "image_url": 'hhttps://imgur.com/a/o724qLg',
    },
    {
        "name": "AntiLose",
        "rarity": "Легендарный",
        "points": 10000,
        "coins": 30,
        "image_url": 'https://imgur.com/a/fS7yDe5',
    },
    {
        "name": "NeworkPC",
        "rarity": "Эпический",
        "points": 3000,
        "coins": 10,
        "image_url": 'https://imgur.com/a/ltZ6fUH',
    },
    {
        "name": "GrapeCrack",
        "rarity": "Легендарный",
        "points": 10000,
        "coins": 30,
        "image_url": 'https://imgur.com/a/ksCVVez',
    },
    {
        "name": "Elixir",
        "rarity": "Мифический",
        "points": 5000,
        "coins": 15,
        "image_url": 'https://imgur.com/a/d9JlC3f',
    },
    {
        "name": "G.T.R Win Project",
        "rarity": "Мифический",
        "points": 5000,
        "coins": 15,
        "image_url": 'https://imgur.com/a/1qiosGF',
    },
    {
        "name": "Waithware",
        "rarity": "Эпический",
        "points": 3000,
        "coins": 10,
        "image_url": 'https://imgur.com/a/bHrvZQs',
    },
    {
        "name": "BloodPC",
        "rarity": "Редкий",
        "points": 1000,
        "coins": 5,
        "image_url": 'https://imgur.com/a/qwvUGc7',
    },
    {
        "name": "Nearby|Infinity team #N1",
        "rarity": "Эпическая",
        "points": 3000,
        "coins": 10,
        "image_url": 'https://imgur.com/a/Mstx6h9',
    },
    {
        "name": "GroovyTeam",
        "rarity": "Легендарный",
        "points": 10000,
        "coins": 30,
        "image_url": 'https://imgur.com/a/bCyqm7M',
    },
    {
        "name": "AmyrSoftf",
        "rarity": "Обычный",
        "points": 500,
        "coins": 3,
        "image_url": 'https://imgur.com/a/oLM2HHn', 
    }
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    logging.debug(f"User {user_id} started bot")

    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name
        }
        save_bot_data()

    welcome_message = (
        f"👋 Привет, {bot_data[user_id]['nickname']}! Я бот, в котором ты можешь собирать уникальные карточки и соревноваться с другими игроками.\n\n"
        f"Чтобы начать, добавь меня в группу, нажав на кнопку ниже."
    )
    
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("➕ Добавить бота в чат", url='https://t.me/SoftCardsBot?startgroup=new') #тут менять ссылку на бота 
    keyboard.add(button)

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        f"Что это за бот?\n"
        f"Тут ты можешь собирать карточки софтов и соревноваться с другими игроками.\n\n"
        f"Команды:\n"
        f"👤 /profile — ваш профиль\n"
        f"✨ /name [ник] — изменить никнейм\n"
        f"Для получения карты отправьте любую из команды:\n"
        f"софт\n" # сюда всякие хелп команды
        f"карту, сэр\n"
        f"карту сэр\n"
        f"карту, сэр.\n"
        f"получить карту"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['profile'])
def send_profile(message):
    user_id = str(message.from_user.id)
    logging.debug(f"User {user_id} requested profile")

    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name
         }

    nickname = bot_data[user_id]['nickname']
    cards_count = len(bot_data[user_id]['cards'])
    total_cards = len(cards)  
    points = bot_data[user_id]['points']
    coins = bot_data[user_id]['coins']

    profile_text = (
       f"Профиль «{nickname}»\n\n"
       f"🔎 ID • {user_id}\n"
       f"🃏 Карт • {cards_count} из {total_cards}\n"
       f"✨ Очки • {points}\n"
       f"💰 Монеты • {coins}"
   )
    
    try:
        profile_photos = bot.get_user_profile_photos(user_id)
        
        avatar_file_id = None
        if profile_photos.total_count > 0:
            avatar_file_id = profile_photos.photos[0][-1].file_id

        if avatar_file_id:
            bot.send_photo(message.chat.id, avatar_file_id, caption=profile_text)
            logging.debug(f"User {user_id} profile with photo and caption sent")
        else:
            bot.send_message(message.chat.id, profile_text)
            logging.debug(f"User {user_id} profile without photo sent")

    except Exception as e:
        logging.error(f"User {user_id} error sending profile: {e}")
        bot.send_message(message.chat.id, f"Не удалось загрузить аватар. Ошибка: {e}\n\n" + profile_text)

@bot.message_handler(commands=['name'])
def set_nickname(message):
    user_id = str(message.from_user.id)
    nickname = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    logging.debug(f"User {user_id} requested set nickname to {nickname}")

    if nickname:
        bot_data[user_id]['nickname'] = nickname
        save_bot_data()
        bot.send_message(message.chat.id, f"Ваш никнейм изменен на «{nickname}».")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите новый никнейм после команды /name.")

@bot.message_handler(func=lambda message: message.text.lower() in ['софт', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту']) # команды чтоб дало вам карточки
def give_card(message):
   user_id = str(message.from_user.id)
   logging.debug(f"User {user_id} requested card")

   if user_id not in bot_data:
       bot_data[user_id] = {
           'balance': 0,
           'cards': {},
           'points': 0,
           'coins': 0,
           'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name
       }

   try:
       current_time = time.time()
       
       last_used_time = max(
           (bot_data[user_id]['cards'][card_name]['last_used'] for card_name in bot_data[user_id]['cards']),
           default=0
       )

       if current_time - last_used_time < 3 * 3600:  # типа задержка
           remaining_time = (3 * 3600) - (current_time - last_used_time)
           remaining_hours = remaining_time // 3600
           remaining_minutes = (remaining_time % 3600) // 60
           remaining_seconds = remaining_time % 60
            
           response = (
               "Вы осмотрелись, но не увидели рядом софтов 👀\n\n"
               f"⏳ Подождите {int(remaining_hours)}ч. {int(remaining_minutes)}мин. {int(remaining_seconds)}сек., чтобы попробовать снова." # если ты уже использовал карточки
           )
           bot.send_message(message.chat.id, response)
           return

       card = random.choice(cards)

       points_earned = card['points']
       coins_earned = card['coins']

       bot_data[user_id]['cards'][card["name"]] = {
           "last_used": current_time,
           "rarity": card['rarity'],
           "points_earned": points_earned,
           "coins_earned": coins_earned
       }
       
       bot_data[user_id]['points'] += points_earned  
       bot_data[user_id]['coins'] += coins_earned  
       save_bot_data()

       response = (
           f"🃏 Карточка «{card['name']}» добавлена.\n\n"
           f"💎 Редкость • {card['rarity']}\n"
           f"✨ Очки • +{points_earned} [{bot_data[user_id]['points']}]\n"
           f"💰 Монеты • +{coins_earned} [{bot_data[user_id]['coins']}]\n\n"
           f"🎁 Получите следующую карточку через три часа!"
       )

       bot.send_photo(message.chat.id, card["image_url"], caption=response)

   except Exception as e:
       logging.error(f"Error giving card to user {user_id}: {e}")
       bot.send_message(message.chat.id, "Произошла ошибка при получении карточки. Попробуйте еще раз.")

if __name__ == '__main__':
   bot.polling(none_stop=True)
