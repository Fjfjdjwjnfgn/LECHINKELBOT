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

ADMIN_USERNAME = "clamsurr"

logging.basicConfig(level=logging.DEBUG)

# ============================ ДАННЫЕ ============================
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

# ============================ КАРТЫ ============================
cards = [
    {"name": "Лечинкель Гитлер","rarity": "Легендарный","points": 1000,"coins": 50,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6015.jpg'},
    {"name": "Лечинкель Rollback.Fun","rarity": "Легендарный","points": 1000,"coins": 50,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6010.jpg'},
    {"name": "Лечинкель News Pixel","rarity": "Легендарный","points": 1000,"coins": 50,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6017.jpg'},
    {"name": "Лечинкель пишет сценарий","rarity": "Мифический","points": 10000,"coins": 100,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6018.jpg'},
    {"name": "Лечинкель в магазине","rarity": "Обычный","points": 50,"coins": 5,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6019.jpg'},
    {"name": "Простой Лечинка","rarity": "Обычный","points": 50,"coins": 5,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6020.jpg'},
    {"name": "Яблуко лечинкель","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6022.jpg'},
    {"name": "Лечинкель в бахмуте","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6023.jpg'},
    {"name": "Лечинкель пополняет тетрадь смерти","rarity": "Обычный","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6025.md.jpg'},
    {"name": "Лечинкель с воробьями ","rarity": "Эпический","points": 500,"coins": 25,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6024.jpg'},
    {"name": "Лечинкель Диктатор","rarity": "Мифический","points": 10000,"coins": 100,"image_url": "https://ltdfoto.ru/images/2025/11/25/6026.jpg"},
    {"name": "Лечинкель целует Гарена","rarity": "Мифический","points": 10000,"coins": 100,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6027.jpg'},
    {"name": "Аллах Лечинкель","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6028.jpg'},
    {"name": "Лечинкель Аллах Бабах","rarity": "Эпический","points": 500,"coins": 25,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6029.jpg'},
    {"name": "Бомж Лечинкель","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6030.md.jpg'},
    {"name": "Мало хохол Лечинкель","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6031.jpg'},
    {"name": "Верой Лечинкель","rarity": "Легендарный","points": 1000,"coins": 50,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6032.jpg'},
    {"name": "Культурный ле чинкель","rarity": "Обычный","points": 50,"coins": 5,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6033.jpg'},
    {"name": "Лечинкель с вкусняшкой","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6044.jpg'},
    {"name": "Лечинкель патриот Украины","rarity": "Эпический","points": 500,"coins": 25,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6047.jpg'},
    {"name": "Лечинкель и Тесак!","rarity": "Эпический","points": 500,"coins": 25,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6048.jpg'},
    {"name": "Нацист Лечинкель","rarity": "Редкий","points": 250,"coins": 15,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6051.md.jpg'},
    {"name": "Лечинкель пабло","rarity": "Редкий","points": 500,"coins": 25,"image_url": 'https://ltdfoto.ru/images/2025/11/25/6052.md.jpg'},
]

rarities = {"Эпический": [], "Редкий": [], "Обычный": [], "Мифический": [], "Легендарный": []}
for card in cards:
    r = card['rarity'].strip()
    if r == "Мифическая": r = "Мифический"
    if r in rarities:
        rarities[r].append(card)

rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [1.2, 1.5, 4, 0.1, 0.5]

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ============================ КОМАНДЫ ============================
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
        f"/profile — ваш профиль\n"
        f"/name [ник] — изменить никнейм\n"
        f"/top — топ игроков (только в группах)\n"
        f"Для получения карты отправьте:\n"
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
    if user_id not in bot_data:  
        bot_data[user_id] = {  
            'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name  
        }  
        save_bot_data()

    nickname = bot_data[user_id]['nickname']  
    cards_count = len(bot_data[user_id]['cards'])  
    total_cards = len(cards)    
    points = bot_data[user_id]['points']  
    coins = bot_data[user_id]['coins']  

    profile_text = (  
       f"Профиль «{nickname}»\n\n"  
       f"ID • {user_id}\n"  
       f"Карт • {cards_count} из {total_cards}\n"  
       f"Очки • {points}\n"  
       f"Монеты • {coins}"
    )

    try:  
        profile_photos = bot.get_user_profile_photos(user_id)  
        if profile_photos.total_count > 0:  
            avatar_file_id = profile_photos.photos[0][-1].file_id  
            bot.send_photo(message.chat.id, avatar_file_id, caption=profile_text, reply_to_message_id=message.message_id)  
        else:  
            bot.send_message(message.chat.id, profile_text, reply_to_message_id=message.message_id)  
    except Exception as e:  
        bot.send_message(message.chat.id, f"Не удалось загрузить аватар.\n\n" + profile_text, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['name'])
def set_nickname(message):
    user_id = str(message.from_user.id)
    try:
        nickname = message.text.split(maxsplit=1)[1][:32]
        bot_data[user_id]['nickname'] = nickname  
        save_bot_data()  
        bot.reply_to(message, f"Ваш никнейм изменен на «{nickname}».")  
    except:
        bot.reply_to(message, "Пожалуйста, укажите новый никнейм после команды /name.")

# ============================ ТОП (РАБОЧАЯ ВЕРСИЯ) ============================
@bot.message_handler(commands=['top'])
def show_top_menu(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "Только в группах!")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("По очкам", callback_data="top_points"),
        types.InlineKeyboardButton("По картам", callback_data="top_cards"),
        types.InlineKeyboardButton("По монетам", callback_data="top_coins")
    )
    bot.reply_to(message, "Топ 10 игроков\n\nВыберите по какому значению показать топ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top(call):
    crit = call.data.split('_')[1]
    users = [{'nick': v['nickname'], 'points': v['points'], 'cards': len(v['cards']), 'coins': v['coins']}
             for v in bot_data.values() if isinstance(v, dict)]

    if crit == 'points': users.sort(key=lambda x: x['points'], reverse=True); title = "Топ по очкам"
    if crit == 'cards':  users.sort(key=lambda x: x['cards'], reverse=True);  title = "Топ по картам"
    if crit == 'coins':  users.sort(key=lambda x: x['coins'], reverse=True);  title = "Топ по монетам"

    text = f"{title}\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u[crit if crit != 'cards' else 'cards']}\n"

    try:
        bot.send_message(call.from_user.id, text)
        bot.answer_callback_query(call.id, "Топ отправлен в ЛС")
    except:
        bot.answer_callback_query(call.id, "Открой чат со мной, чтобы получить топ")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# ============================ ВЫДАЧА КАРТЫ ============================
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ['лечинкель', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту'])
def give_card(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name}
        save_bot_data()

    current_time = time.time()
    last_used_time = max((bot_data[user_id]['cards'].get(card_name, {}).get('last_used', 0) for card_name in bot_data[user_id]['cards']), default=0)

    if current_time - last_used_time < 3 * 3600:
        remaining_time = (3 * 3600) - (current_time - last_used_time)
        remaining_hours = int(remaining_time // 3600)
        remaining_minutes = int((remaining_time % 3600) // 60)
        remaining_seconds = int(remaining_time % 60)
        response = (
            "Вы осмотрелись, но не увидели рядом лица Лечинкеля\n\n"
            f"Подождите {remaining_hours}ч. {remaining_minutes}мин. {remaining_seconds}сек., чтобы попробовать снова."
        )
        bot.send_message(message.chat.id, response, reply_to_message_id=message.message_id)
        return

    selected_rarity = random.choices(rarity_order, weights=weights)[0]
    card = random.choice(rarities[selected_rarity])

    bot_data[user_id]['cards'][card["name"]] = {
        "last_used": current_time,
        "rarity": selected_rarity,
        "points_earned": card['points'],
        "coins_earned": card['coins']
    }
    bot_data[user_id]['points'] += card['points']
    bot_data[user_id]['coins'] += card['coins']
    save_bot_data()

    response = (
        f"Карточка «{card['name']}» добавлена.\n\n"
        f"Редкость • {selected_rarity}\n"
        f"Очки • +{card['points']} [{bot_data[user_id]['points']}]\n"
        f"Монеты • +{card['coins']} [{bot_data[user_id]['coins']}]\n\n"
        f"Получите следующую карточку через три часа!"
    )
    bot.send_photo(message.chat.id, card["image_url"], caption=response, reply_to_message_id=message.message_id)

# ============================ АДМИНКА ============================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.reply_to(message, "Ты не @clamsurr. Иди нахуй.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Создать промокод", callback_data="create_promo"),
        types.InlineKeyboardButton("Список промокодов", callback_data="list_promos"),
        types.InlineKeyboardButton("Рассылка", callback_data="admin_broadcast")
    )
    bot.send_message(message.chat.id, "Админ-панель @clamsurr\n\nВыбирай:", reply_markup=markup)

# Промокоды и рассылка — без изменений (всё работает)
@bot.callback_query_handler(func=lambda call: call.data == "create_promo")
def choose_rarity(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    markup = types.InlineKeyboardMarkup(row_width=2)
    for r in rarity_order:
        markup.add(types.InlineKeyboardButton(r, callback_data=f"rar_{r}"))
    bot.edit_message_text("Редкость карты:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rar_"))
def choose_duration(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    rarity = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for text, days in [("1 день",1),("3 дня",3),("7 дней",7),("30 дней",30),("Навсегда",0)]:
        markup.add(types.InlineKeyboardButton(text, callback_data=f"dur_{days}_{rarity}"))
    bot.edit_message_text(f"Редкость: {rarity}\n\nДлительность:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dur_"))
def choose_uses(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    parts = call.data.split("_")
    days = parts[1]
    rarity = parts[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for text, uses in [("1 раз",1),("5 раз",5),("10 раз",10),("50 раз",50),("Без лимита",0)]:
        markup.add(types.InlineKeyboardButton(text, callback_data=f"uses_{uses}_{days}_{rarity}"))
    bot.edit_message_text(f"Редкость: {rarity}\nДлительность: {'Навсегда' if days=='0' else f'{days} дн.'}\n\nАктиваций:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("uses_"))
def create_final(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        return
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
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
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

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def start_broadcast(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.answer_callback_query(call.id, "Нет доступа")
        return
    bot.send_message(call.from_user.id, "Пришли сообщение для рассылки (текст, фото, видео — всё подойдёт):")
    bot.register_next_step_handler(call.message, do_broadcast)

def do_broadcast(message):
    if str(message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        return
    sent = 0
    for uid in list(bot_data.keys()):
        try:
            bot.forward_message(int(uid), message.chat.id, message.message_id)
            sent += 1
            time.sleep(0.033)
        except:
            pass
    bot.reply_to(message, f"Рассылка завершена. Отправлено: {sent}")

@bot.message_handler(commands=['promo'])
def activate_promo(message):
    try:
        code = message.text.split()[1].upper()
    except:
        bot.reply_to(message, "Пиши: /promo КОД")
        return

    if code not in bot_data.get('promocodes', {}):
        bot.reply_to(message, "Такого промокода нет.")
        return

    p = bot_data['promocodes'][code]
    uid = str(message.from_user.id)

    if p['expires'] != 0 and p['expires'] < time.time():
        bot.reply_to(message, "Промокод просрочен.")
        return
    if p['max_uses'] != 0 and len(p['used_by']) >= p['max_uses']:
        bot.reply_to(message, "Лимит активаций исчерпан.")
        return
    if uid in p['used_by']:
        bot.reply_to(message, "Ты уже использовал этот промокод.")
        return

    card = random.choice(rarities[p['rarity']])
    if uid not in bot_data:
        bot_data[uid] = {'cards':{}, 'points':0, 'coins':0, 'nickname': message.from_user.first_name}

    bot_data[uid]['cards'][card['name']] = {"last_used": time.time(), "rarity": p['rarity']}
    bot_data[uid]['points'] += card['points']
    bot_data[uid]['coins'] += card['coins']
    p['used_by'].append(uid)
    save_bot_data()

    bot.send_photo(message.chat.id, card['image_url'],
                   caption=f"Промокод активирован!\n\n"
                           f"«{card['name']}»\n"
                           f"Редкость: {p['rarity']}\n"
                           f"+{card['points']} очков • +{card['coins']} монет",
                   reply_to_message_id=message.message_id)

# Автопромо в каналах
@bot.message_handler(func=lambda m: m.sender_chat and m.sender_chat.type == 'channel' and m.chat.type == 'supergroup')
def handle_new_channel_post_in_group(message):
    phrases = [
        "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
        "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
        "Получи свою карточку! Просто напиши «Лечинкель»"
    ]
    bot.reply_to(message, random.choice(phrases))

if __name__ == '__main__':
    print("Бот запущен. @clamsurr — бог.")
    bot.infinity_polling()
