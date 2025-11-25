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

# Группировка по редкости
rarities = {"Эпический": [], "Редкий": [], "Обычный": [], "Мифический": [], "Легендарный": []}
for card in cards:
    r = card['rarity'].strip()
    if r in rarities:
        rarities[r].append(card)

rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [1.2, 1.5, 4.0, 0.1, 0.5]

# ============================ ПРОМОКОДЫ ============================
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ============================ КОМАНДЫ ============================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
            'nickname': message.from_user.username or message.from_user.first_name or "Аноним"
        }
        save_bot_data()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Добавить в группу", url="https://t.me/Lechinkelcards_bot?startgroup=new"))
    bot.send_message(message.chat.id,
                     f"Привет, {bot_data[user_id]['nickname']}!\nЯ бот с карточками Лечинкеля\n\nДобавь меня в группу и пиши «лечинкель»",
                     reply_markup=markup)

@bot.message_handler(commands=['profile'])
def send_profile(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot.reply_to(message, "Напиши /start")
        return
    u = bot_data[user_id]
    text = f"Профиль «{u['nickname']}»\n\nID: {user_id}\nКарт: {len(u['cards'])} из {len(cards)}\nОчки: {u['points']}\nМонеты: {u['coins']}"
    bot.reply_to(message, text)

@bot.message_handler(commands=['name'])
def set_nickname(message):
    try:
        new_nick = message.text.split(maxsplit=1)[1][:32]
        bot_data[str(message.from_user.id)]['nickname'] = new_nick
        save_bot_data()
        bot.reply_to(message, f"Ник изменён → «{new_nick}»")
    except:
        bot.reply_to(message, "Напиши: /name НовыйНик")

# ============================ ВЫДАЧА КАРТЫ ============================
@bot.message_handler(func=lambda m: m.text and m.text.lower().strip() in ['лечинкель', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту'])
def give_card(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot.reply_to(message, "Напиши /start")
        return

    last = max((bot_data[user_id]['cards'].get(c, {}).get('last_used', 0) for c in bot_data[user_id]['cards']), default=0)
    if time.time() - last < 10800:
        bot.reply_to(message, "Карты выдаются раз в 3 часа")
        return

    rarity = random.choices(rarity_order, weights=weights)[0]
    card = random.choice(rarities[rarity])

    bot_data[user_id]['cards'][card['name']] = {"last_used": time.time(), "rarity": rarity}
    bot_data[user_id]['points'] += card['points']
    bot_data[user_id]['coins'] += card['coins']
    save_bot_data()

    caption = (f"Карточка «{card['name']}»\n\n"
               f"Редкость • {rarity}\n"
               f"Очки • +{card['points']} [{bot_data[user_id]['points']}]\n"
               f"Монеты • +{card['coins']} [{bot_data[user_id]['coins']}]\n\n"
               f"Следующая карта через 3 часа!")

    bot.send_photo(message.chat.id, card['image_url'], caption=caption, reply_to_message_id=message.message_id)

# ============================ АДМИН-ПАНЕЛЬ (РАССЫЛКА + ПРОМОКОДЫ) ============================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.reply_to(message, "Ты не @clamsurr")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Рассылка", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("Создать промокод", callback_data="create_promo"),
        types.InlineKeyboardButton("Список промокодов", callback_data="list_promos")
    )
    bot.reply_to(message, "Админ-панель @clamsurr", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_') or call.data in ['create_promo', 'list_promos'])
def admin_callbacks(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        bot.answer_callback_query(call.id, "Нет доступа")
        return

    if call.data == "admin_stats":
        total_cards = sum(len(u['cards']) for u in bot_data.values() if isinstance(u, dict))
        bot.answer_callback_query(call.id, f"Пользователей: {len(bot_data)}\nКарт выдано: {total_cards}", show_alert=True)

    elif call.data == "admin_broadcast":
        bot.send_message(call.from_user.id, "Пришли сообщение для рассылки (текст, фото, видео и т.д.):")
        bot.register_next_step_handler_by_chat_id(call.from_user.id, do_broadcast)

    # ---------- промокоды ----------
    elif call.data == "create_promo":
        markup = types.InlineKeyboardMarkup(row_width=2)
        for r in rarity_order:
            markup.add(types.InlineKeyboardButton(r, callback_data=f"rar_{r}"))
        bot.edit_message_text("Выбери редкость промокода:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "list_promos":
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

@bot.callback_query_handler(func=lambda call: call.data.startswith("rar_"))
def choose_duration(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    rarity = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    for text, days in [("1 день",1),("3 дня",3),("7 дней",7),("30 дней",30),("Навсегда",0)]:
        markup.add(types.InlineKeyboardButton(text, callback_data=f"dur_{days}_{rarity}"))
    bot.edit_message_text(f"Редкость: {rarity}\n\nВыбери длительность:", call.message.chat.id, call.message.message_id, reply_markup=markup)

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
def create_promo_final(call):
    if str(call.from_user.username or "").lower() != ADMIN_USERNAME.lower(): return
    parts = call.data.split("_")
    uses = 0 if parts[1] == "0" else int(parts[1])
    days = int(parts[2])
    rarity = parts[3]

    code = generate_code()
    expires = 0 if days == 0 else time.time() + days * 86400

    bot_data.setdefault('promocodes', {})[code] = {
        "rarity": rarity,
        "expires": expires,
        "max_uses": uses,
        "used_by": []
    }
    save_bot_data()

    bot.edit_message_text(
        f"Промокод создан!\n\n"
        f"Код: `{code}`\n"
        f"Редкость: {rarity}\n"
        f"Действует: {'Навсегда' if days==0 else f'{days} дн.'}\n"
        f"Активаций: {'Без лимита' if uses==0 else uses}",
        call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# Рассылка
def do_broadcast(message):
    if str(message.from_user.username or "").lower() != ADMIN_USERNAME.lower():
        return
    sent = 0
    failed = 0
    for uid in list(bot_data.keys()):
        try:
            bot.forward_message(int(uid), message.chat.id, message.message_id)
            sent += 1
            time.sleep(0.033)  # антифлуд
        except:
            failed += 1
    bot.reply_to(message, f"Рассылка завершена!\nОтправлено: {sent}\nНе удалось: {failed}")

# Активация промокода
@bot.message_handler(commands=['promo'])
def activate_promo(message):
    try:
        code = message.text.split()[1].upper()
    except:
        bot.reply_to(message, "Пиши: /promo КОД")
        return

    promos = bot_data.get('promocodes', {})
    if code not in promos:
        bot.reply_to(message, "Такого промокода нет.")
        return

    p = promos[code]
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

# ============================ АВТООТВЕТ В КАНАЛАХ ============================
processed_posts = set()

@bot.message_handler(func=lambda m: getattr(m, 'sender_chat', None) and m.sender_chat.type == 'channel' and m.chat.type in ['group', 'supergroup'])
def channel_promo(message):
    key = f"{message.chat.id}_{message.message_id}"
    if key in processed_posts:
        return
    processed_posts.add(key)

    phrases = [
        "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
        "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
        "Получи свою карточку! Просто напиши «Лечинкель»"
    ]
    try:
        bot.reply_to(message, random.choice(phrases))
    except:
        pass
    finally:
        threading.Timer(600, processed_posts.discard, [key]).start()

# ============================ ЗАПУСК ============================
if __name__ == '__main__':
    print("Бот запущен — владелец @clamsurr")
    bot.infinity_polling(none_stop=True)
