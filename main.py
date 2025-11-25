import telebot
from telebot import types
import random
import logging
import json
import time
import string

TOKEN = "8501222332:AAG4yM_GDfB3TpJ-uikLTL5fE8FJsuqxD8g" 
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.DEBUG)

ADMIN_USERNAME = 'clamsurr'  # Админ юзернейм

def load_bot_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return {'promocodes': {}, 'users': {}}
            data = json.loads(content)
            if 'promocodes' not in data:
                data['promocodes'] = {}
            return data
    except FileNotFoundError:
        return {'promocodes': {}, 'users': {}}
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON: {e}")
        return {'promocodes': {}, 'users': {}}

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as file:
        json.dump(bot_data, file, ensure_ascii=False, indent=4)

bot_data = load_bot_data()

cards = [
    {
        "name": "Лечинкель Гитлер", #софт
        "rarity": "Легендарный", #редкость
        "points": 1000, #очки
        "coins": 50, # монеты
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6015.jpg', # ссылка на фото 
    },
    {
        "name": "Лечинкель Rollback.Fun",
        "rarity": "Легендарный",
        "points": 1000,
        "coins": 50,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6010.jpg',
    },
    {
        "name": "Лечинкель News Pixel",
        "rarity": "Легендарный",
        "points": 1000,
        "coins": 50,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6017.jpg',
    },
    {
        "name": "Лечинкель пишет сценарий",
        "rarity": "Мифический",
        "points": 10000,
        "coins": 100,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6018.jpg',
    },
    {
        "name": "Лечинкель в магазине",
        "rarity": "Обычный",
        "points": 50,
        "coins": 5,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6019.jpg',
    },
    {
        "name": "Простой Лечинка",
        "rarity": "Обычный",
        "points": 50,
        "coins": 5,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6020.jpg',
    },
    {
        "name": "Яблуко лечинкель",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6022.jpg',
    },
    {
        "name": "Лечинкель в бахмуте",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6023.jpg',
    },
    {
        "name": "Лечинкель пополняет тетрадь смерти",
        "rarity": "Обычный",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6025.md.jpg',
    },
    {
        "name": "Лечинкель с воробьями ",
        "rarity": "Эпический",
        "points": 500,
        "coins": 25,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6024.jpg',
    },
    {
        "name": "Лечинкель Диктатор",
        "rarity": "Мифический",
        "points": 10000,
        "coins": 100,
        "image_url": "https://ltdfoto.ru/images/2025/11/25/6026.jpg",
    },
    {
        "name": "Лечинкель целует Гарена",
        "rarity": "Мифический",
        "points": 10000,
        "coins": 100,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6027.jpg',
    },
    {
        "name": "Аллах Лечинкель",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6028.jpg',
    },
    {
        "name": "Лечинкель Аллах Бабах",
        "rarity": "Эпический",
        "points": 500,
        "coins": 25,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6029.jpg',
    },
    {
        "name": "Бомж Лечинкель",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6030.md.jpg',
    },
    {
        "name": "Мало хохол Лечинкель",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6031.jpg',
    },
    {
        "name": "Верой Лечинкель",
        "rarity": "Легендарный",
        "points": 1000,
        "coins": 50,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6032.jpg',
    },
    {
        "name": "Культурный ле чинкель",
        "rarity": "Обычный",
        "points": 50,
        "coins": 5,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6033.jpg',
    },
    {
        "name": "Лечинкель с вкусняшкой",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6044.jpg',
    },
    {
        "name": "Лечинкель патриот Украины",
        "rarity": "Эпический",
        "points": 500,
        "coins": 25,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6047.jpg',
    },
    {
        "name": "Лечинкель и Тесак!",
        "rarity": "Эпический",
        "points": 500,
        "coins": 25,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6048.jpg',
    },
    {
        "name": "Нацист Лечинкель",
        "rarity": "Редкий",
        "points": 250,
        "coins": 15,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6051.md.jpg',
    },
        {
        "name": "Лечинкель пабло",
        "rarity": "Редкий",
        "points": 500,
        "coins": 25,
        "image_url": 'https://ltdfoto.ru/images/2025/11/25/6052.md.jpg',
    },
]

# Группировка карт по редкостям (с нормализацией названий)
rarities = {
    "Эпический": [],
    "Редкий": [],
    "Обычный": [],
    "Мифический": [],
    "Легендарный": [],
}

for card in cards:
    rarity = card['rarity'].strip()  # Убираем пробелы
    if rarity == "Мифическая":
        rarity = "Мифический"  # Унифицируем
    if rarity in rarities:
        rarities[rarity].append(card)

# Порядок редкостей и веса
rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [1.2, 1.5, 4, 0.1, 0.5]

# Генерация уникального промокода
def generate_promo_code(length=8):
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    while code in bot_data['promocodes']:
        code = ''.join(random.choice(chars) for _ in range(length))
    return code

# Админ-панель: команда для создания промокода
@bot.message_handler(commands=['create_promo'])
def create_promo(message):
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "Вы не администратор.")
        return

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for rarity in rarity_order:
        keyboard.add(types.InlineKeyboardButton(rarity, callback_data=f'promo_rarity_{rarity}'))

    bot.reply_to(message, "Выберите редкость карты для промокода:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('promo_rarity_'))
def handle_promo_rarity(call):
    if call.from_user.username != ADMIN_USERNAME:
        bot.answer_callback_query(call.id, "Вы не администратор.")
        return

    selected_rarity = call.data.split('_')[2]
    promo_code = generate_promo_code()

    # Сохраняем промокод: редкость и список использовавших юзеров (для предотвращения повторного использования)
    bot_data['promocodes'][promo_code] = {
        'rarity': selected_rarity,
        'used_by': []
    }
    save_bot_data()

    bot.answer_callback_query(call.id, f"Промокод создан: {promo_code} (редкость: {selected_rarity})")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# Команда для активации промокода /promo <код>
@bot.message_handler(commands=['promo'])
def activate_promo(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Использование: /promo <код>")
        return

    promo_code = args[1].upper()
    if promo_code not in bot_data['promocodes']:
        bot.reply_to(message, "Неверный промокод.")
        return

    promo = bot_data['promocodes'][promo_code]
    if user_id in promo['used_by']:
        bot.reply_to(message, "Вы уже использовали этот промокод.")
        return

    # Выдача карты выбранной редкости
    selected_rarity = promo['rarity']
    if not rarities.get(selected_rarity):
        bot.reply_to(message, "Ошибка: нет карт этой редкости.")
        return

    card = random.choice(rarities[selected_rarity])
    current_time = time.time()

    points_earned = card['points']
    coins_earned = card['coins']

    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name
        }

    bot_data[user_id]['cards'][card["name"]] = {
        "last_used": current_time,
        "rarity": selected_rarity,
        "points_earned": points_earned,
        "coins_earned": coins_earned
    }

    bot_data[user_id]['points'] += points_earned
    bot_data[user_id]['coins'] += coins_earned

    # Отмечаем использование
    promo['used_by'].append(user_id)
    save_bot_data()

    response = (
        f"🃏 Промокод активирован! Карточка «{card['name']}» добавлена.\n\n"
        f"💎 Редкость • {selected_rarity}\n"
        f"✨ Очки • +{points_earned} [{bot_data[user_id]['points']}]\n"
        f"💰 Монеты • +{coins_earned} [{bot_data[user_id]['coins']}]\n"
    )

    bot.send_photo(message.chat.id, card["image_url"], caption=response, reply_to_message_id=message.message_id)

# Админ-панель: команда для просмотра всех промокодов
@bot.message_handler(commands=['admin_promos'])
def list_promos(message):
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "Вы не администратор.")
        return

    if not bot_data['promocodes']:
        bot.reply_to(message, "Нет активных промокодов.")
        return

    text = "Список промокодов:\n\n"
    for code, data in bot_data['promocodes'].items():
        used_count = len(data['used_by'])
        text += f"{code} — {data['rarity']} (использовано: {used_count})\n"

    bot.reply_to(message, text)

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
    button = types.InlineKeyboardButton("➕ Добавить бота в чат", url='https://t.me/Lechinkelcards_bot?startgroup=new') #тут менять ссылку на бота 
    keyboard.add(button)

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        f"Что это за бот?\n"
        f"Тут ты можешь собирать карточки лица Лечинкеля и соревноваться с другими игроками.\n\n"
        f"Команды:\n"
        f"👤 /profile — ваш профиль\n"
        f"✨ /name [ник] — изменить никнейм\n"
        f"Для получения карты отправьте любую из команды:\n"
        f"лечинкель\n" # сюда всякие хелп команды
        f"карту, сэр\n"
        f"карту сэр\n"
        f"карту, сэр.\n"
        f"получить карту"
    )
    bot.send_message(message.chat.id, help_text, reply_to_message_id=message.message_id)

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
            bot.send_photo(message.chat.id, avatar_file_id, caption=profile_text, reply_to_message_id=message.message_id)
            logging.debug(f"User {user_id} profile with photo and caption sent")
        else:
            bot.send_message(message.chat.id, profile_text, reply_to_message_id=message.message_id)
            logging.debug(f"User {user_id} profile without photo sent")

    except Exception as e:
        logging.error(f"User {user_id} error sending profile: {e}")
        bot.send_message(message.chat.id, f"Не удалось загрузить аватар. Ошибка: {e}\n\n" + profile_text, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['name'])
def set_nickname(message):
    user_id = str(message.from_user.id)
    nickname = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    logging.debug(f"User {user_id} requested set nickname to {nickname}")

    if nickname:
        bot_data[user_id]['nickname'] = nickname
        save_bot_data()
        bot.send_message(message.chat.id, f"Ваш никнейм изменен на «{nickname}».", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите новый никнейм после команды /name.", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['top'])
def show_top_menu(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "Эта команда доступна только в группах.")
        return

    text = "🏆 Топ 10 игроков этой группы\n\nВыберите по какому значению показать топ"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("По очкам", callback_data='top_points'),
        types.InlineKeyboardButton("По картам", callback_data='top_cards'),
        types.InlineKeyboardButton("По монетам", callback_data='top_coins')
    )

    bot.reply_to(message, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top_callback(call):
    criteria = call.data.split('_')[1]

    # Собрать список пользователей из БД
    users = []
    for user_id, data in bot_data.items():
        if user_id.isdigit():  # Только юзеры, не промокоды и т.д.
            users.append({
                'nickname': data['nickname'],
                'points': data['points'],
                'cards_count': len(data['cards']),
                'coins': data['coins']
            })

    if not users:
        bot.answer_callback_query(call.id, "Нет игроков в базе данных.")
        return

    if criteria == 'points':
        users.sort(key=lambda x: x['points'], reverse=True)
        title = "Топ по очкам"
        value_key = 'points'
    elif criteria == 'cards':
        users.sort(key=lambda x: x['cards_count'], reverse=True)
        title = "Топ по картам"
        value_key = 'cards_count'
    elif criteria == 'coins':
        users.sort(key=lambda x: x['coins'], reverse=True)
        title = "Топ по монетам"
        value_key = 'coins'
    else:
        return

    top_text = f"🏆 {title}\n\n"
    for i, user in enumerate(users[:10], 1):
        top_text += f"{i}. {user['nickname']} — {user[value_key]}\n"

    # Отправляем топ только вызвавшему пользователю в личку
    try:
        bot.send_message(call.from_user.id, top_text)
        bot.answer_callback_query(call.id, "Топ отправлен вам в личные сообщения.")
    except Exception as e:
        logging.error(f"Error sending top to user {call.from_user.id}: {e}")
        bot.answer_callback_query(call.id, "Не удалось отправить топ в личку. Попробуйте позже.")

    # Удаляем кнопки из оригинального сообщения
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda message: message.text.lower() in ['лечинкель', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту']) # команды чтоб дало вам карточки
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
               "Вы осмотрелись, но не увидели рядом лица Лечинкеля 👀\n\n"
               f"⏳ Подождите {int(remaining_hours)}ч. {int(remaining_minutes)}мин. {int(remaining_seconds)}сек., чтобы попробовать снова." # если ты уже использовал карточки
           )
           bot.send_message(message.chat.id, response, reply_to_message_id=message.message_id)
           return

       # Выбор редкости с весами
       selected_rarity = random.choices(rarity_order, weights=weights)[0]
       card = random.choice(rarities[selected_rarity])

       points_earned = card['points']
       coins_earned = card['coins']

       bot_data[user_id]['cards'][card["name"]] = {
           "last_used": current_time,
           "rarity": selected_rarity,
           "points_earned": points_earned,
           "coins_earned": coins_earned
       }
       
       bot_data[user_id]['points'] += points_earned  
       bot_data[user_id]['coins'] += coins_earned  
       save_bot_data()

       response = (
           f"🃏 Карточка «{card['name']}» добавлена.\n\n"
           f"💎 Редкость • {selected_rarity}\n"
           f"✨ Очки • +{points_earned} [{bot_data[user_id]['points']}]\n"
           f"💰 Монеты • +{coins_earned} [{bot_data[user_id]['coins']}]\n\n"
           f"🎁 Получите следующую карточку через три часа!"
       )

       bot.send_photo(message.chat.id, card["image_url"], caption=response, reply_to_message_id=message.message_id)

   except Exception as e:
       logging.error(f"Error giving card to user {user_id}: {e}")
       bot.send_message(message.chat.id, "Произошла ошибка при получении карточки. Попробуйте еще раз.", reply_to_message_id=message.message_id)

# Новый обработчик для постов в канале (через группу обсуждений)
@bot.message_handler(func=lambda m: m.sender_chat and m.sender_chat.type == 'channel' and m.chat.type == 'supergroup')
def handle_new_channel_post_in_group(message):
    phrases = [
        "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
        "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
        "Получи свою карточку! Просто напиши «Лечинкель» 📜"
    ]
    text = random.choice(phrases)
    bot.reply_to(message, text)

if __name__ == '__main__':
   bot.polling(none_stop=True)
