import telebot
from telebot import types
import random
import logging
import json
import time
import string
import threading

TOKEN = "8501222332:AAG4yM_GDfB3TpJ-uikLTL5fE8FJsuqxD8g"
bot = telebot.TeleBot(TOKEN)

# Только ты — админ
ADMIN_USERNAME = "clamsurr"   # ← здесь твой ник, больше нигде менять не надо

logging.basicConfig(level=logging.DEBUG)

# ============================ ДАННЫЕ ============================
def load_bot_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка JSON: {e}")
        return {}

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as file:
        json.dump(bot_data, file, ensure_ascii=False, indent=4)

bot_data = load_bot_data()

# ============================ КАРТЫ ============================
cards = [
    {"name": "Лечинкель Гитлер", "rarity": "Легендарный", "points": 1000, "coins": 50, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6015.jpg'},
    {"name": "Лечинкель Rollback.Fun", "rarity": "Легендарный", "points": 1000, "coins": 50, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6010.jpg'},
    {"name": "Лечинкель News Pixel", "rarity": "Легендарный", "points": 1000, "coins": 50, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6017.jpg'},
    {"name": "Лечинкель пишет сценарий", "rarity": "Мифический", "points": 10000, "coins": 100, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6018.jpg'},
    {"name": "Лечинкель в магазине", "rarity": "Обычный", "points": 50, "coins": 5, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6019.jpg'},
    {"name": "Простой Лечинка", "rarity": "Обычный", "points": 50, "coins": 5, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6020.jpg'},
    {"name": "Яблуко лечинкель", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6022.jpg'},
    {"name": "Лечинкель в бахмуте", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6023.jpg'},
    {"name": "Лечинкель пополняет тетрадь смерти", "rarity": "Обычный", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6025.md.jpg'},
    {"name": "Лечинкель с воробьями ", "rarity": "Эпический", "points": 500, "coins": 25, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6024.jpg'},
    {"name": "Лечинкель Диктатор", "rarity": "Мифический", "points": 10000, "coins": 100, "image_url": "https://ltdfoto.ru/images/2025/11/25/6026.jpg"},
    {"name": "Лечинкель целует Гарена", "rarity": "Мифический", "points": 10000, "coins": 100, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6027.jpg'},
    {"name": "Аллах Лечинкель", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6028.jpg'},
    {"name": "Лечинкель Аллах Бабах", "rarity": "Эпический", "points": 500, "coins": 25, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6029.jpg'},
    {"name": "Бомж Лечинкель", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6030.md.jpg'},
    {"name": "Мало хохол Лечинкель", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6031.jpg'},
    {"name": "Верой Лечинкель", "rarity": "Легендарный", "points": 1000, "coins": 50, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6032.jpg'},
    {"name": "Культурный ле чинкель", "rarity": "Обычный", "points": 50, "coins": 5, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6033.jpg'},
    {"name": "Лечинкель с вкусняшкой", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6044.jpg'},
    {"name": "Лечинкель патриот Украины", "rarity": "Эпический", "points": 500, "coins": 25, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6047.jpg'},
    {"name": "Лечинкель и Тесак!", "rarity": "Эпический", "points": 500, "coins": 25, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6048.jpg'},
    {"name": "Нацист Лечинкель", "rarity": "Редкий", "points": 250, "coins": 15, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6051.md.jpg'},
    {"name": "Лечинкель пабло", "rarity": "Редкий", "points": 500, "coins": 25, "image_url": 'https://ltdfoto.ru/images/2025/11/25/6052.md.jpg'},
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
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ============================ АДМИН-ПАНЕЛЬ ============================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if (message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.reply_to(message, "Ты не @clamsurr")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Рассылка", callback_data="admin_broadcast"))
    markup.add(types.InlineKeyboardButton("Статистика", callback_data="admin_stats"))
    markup.add(types.InlineKeyboardButton("Сброс промо", callback_data="admin_reset"))
    bot.reply_to(message, "Админка @clamsurr", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def admin_handler(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.answer_callback_query(call.id, "Нет доступа")
        return

    if call.data == "admin_stats":
        bot.answer_callback_query(call.id, f"Пользователей: {len(bot_data)}\nКарт выдано: {sum(len(u['cards']) for u in bot_data.values())}", show_alert=True)
    if call.data == "admin_reset":
        processed_posts.clear()
        bot.answer_callback_query(call.id, "Промо сброшен", show_alert=True)
    if call.data == "admin_broadcast":
        bot.send_message(call.from_user.id, "Пришли сообщение для рассылки:")
        bot.register_next_step_handler(call.message, do_broadcast)

def do_broadcast(message):
    if (message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        return
    sent = 0
    for uid in bot_data:
        try:
            bot.forward_message(int(uid), message.chat.id, message.message_id)
            sent += 1
            time.sleep(0.03)
        except: pass
    bot.reply_to(message, f"Рассылка завершена. Отправлено: {sent}")

# ============================ ПРОМОКОДЫ ============================
@bot.callback_query_handler(func=lambda call: call.data == "create_promo")
def choose_rarity(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    markup = types.InlineKeyboardMarkup(row_width=2)
    for r in rarity_order:
        markup.add(types.InlineKeyboardButton(r, callback_data=f"rar_{r}"))
    bot.edit_message_text("Редкость карты:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rar_"))
def choose_duration(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    rarity = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for text, days in [("1 день",1),("3 дня",3),("7 дней",7),("30 дней",30),("Навсегда",0)]:
        markup.add(types.InlineKeyboardButton(text, callback_data=f"dur_{days}_{rarity}"))
    bot.edit_message_text(f"Редкость: {rarity}\n\nДлительность:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dur_"))
def choose_uses(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    parts = call.data.split("_")
    days = parts[1]
    rarity = parts[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for text, uses in [("1 раз",1),("5 раз",5),("10 раз",10),("50 раз",50),("Без лимита",0)]:
        markup.add(types.InlineKeyboardButton(text, callback_data=f"uses_{uses}_{days}_{rarity}"))
    bot.edit_message_text(f"Редкость: {rarity}\nДлительность: {'Навсегда' if days=='0' else f'{days} дн.'}\n\nАктиваций:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("uses_"))
def create_final(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    parts = call.data.split("_")
    uses = 0 if parts[1] == "0" else int(parts[1])
    days = int(parts[2])
    rarity = parts[3]
    code = generate_code()
    expires = 0 if days == 0 else time.time() + days*86400

    bot_data.setdefault('promocodes', {})[code] = {  
        "rarity": rarity,  
        "expires": expires,  
        "max_uses": uses,  
        "used_by": []  
    }  
    save_bot_data()  

    bot.edit_message_text(  
        f"ГОТОВО!\n\n"  
        f"Код: `{code}`\n"  
        f"Редкость: {rarity}\n"  
        f"Действует: {'Навсегда' if days==0 else f'{days} дн.'}\n"  
        f"Активаций: {'Без лимита' if uses==0 else uses}",  
        call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "list_promos")
def show_list(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    if not bot_data.get('promocodes'):
        bot.edit_message_text("Промокодов нет.", call.message.chat.id, call.message.message_id)
        return
    text = "Активные промокоды:\n\n"
    for code, d in bot_data['promocodes'].items():
        used = len(d['used_by'])
        maxu = "∞" if d['max_uses'] == 0 else d['max_uses']
        exp = "Истёк" if d['expires'] != 0 and d['expires'] < time.time() else ("Навсегда" if d['expires']==0 else f"Ещё {(d['expires']-time.time())//86400} дн.")
        text += f"{code} — {d['rarity']} — {used}/{maxu} — {exp}\n"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

# ============================ ОСНОВНЫЕ КОМАНДЫ ============================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
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
        f"Привет, {bot_data[user_id]['nickname']}! Я бот, в котором ты можешь собирать уникальные карточки и соревноваться с другими игроками.\n\n"  
        f"Чтобы начать, добавь меня в группу, нажав на кнопку ниже."  
    )  
    keyboard = types.InlineKeyboardMarkup()  
    keyboard.add(types.InlineKeyboardButton("Добавить бота в чат", url='https://t.me/Lechinkelcards_bot?startgroup=new'))  
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
        f"лечинкель\n"
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

    try:
        bot.send_message(call.from_user.id, top_text)
        bot.answer_callback_query(call.id, "Топ отправлен вам в личные сообщения.")
    except Exception as e:
        logging.error(f"Error sending top to user {call.from_user.id}: {e}")
        bot.answer_callback_query(call.id, "Не удалось отправить топ в личку. Попробуйте позже.")

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
