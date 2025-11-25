import telebot
from telebot import types
import random
import logging
import json
import time
import threading

TOKEN = "8501222332:AAG4yM_GDfB3TpJ-uikLTL5fE8FJsuqxD8g"
bot = telebot.TeleBot(TOKEN)

# Только ты — админ
ADMIN_USERNAME = "clamsurr"  # без @

logging.basicConfig(level=logging.INFO)

def load_bot_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except:
        return {}

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as f:
        json.dump(bot_data, f, ensure_ascii=False, indent=4)

bot_data = load_bot_data()

# ТВОЙ ПОЛНЫЙ И ТОЧНЫЙ СПИСОК КАРТ — БЕЗ ЕДИНОЙ ПРАВКИ
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

# Группировка по редкости с нормализацией
rarities = {"Эпический": [], "Редкий": [], "Обычный": [], "Мифический": [], "Легендарный": []}
for card in cards:
    r = card['rarity'].strip()
    if r == "Мифическая": r = "Мифический"
    if r in rarities:
        rarities[r].append(card)

rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [1.2, 1.5, 4.0, 0.1, 0.5]

processed_posts = set()

# === КОМАНДЫ ===
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
    bot.send_message(message.chat.id, f"Привет, {bot_data[user_id]['nickname']}!\nЯ бот с карточками Лечинкеля\n\nДобавь меня в группу и пиши «лечинкель»", reply_markup=markup)

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
    bot.reply_to(message, "Топ 10 игроков этой группы\n\nВыберите по какому значению показать топ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top(call):
    crit = call.data.split('_')[1]
    users = [{'nick': v['nickname'], 'points': v['points'], 'cards': len(v['cards']), 'coins': v['coins']} 
             for v in bot_data.values()]
    
    if crit == 'points': users.sort(key=lambda x: x['points'], reverse=True); title = "Топ по очкам"
    if crit == 'cards':  users.sort(key=lambda x: x['cards'], reverse=True);  title = "Топ по картам"
    if crit == 'coins':  users.sort(key=lambda x: x['coins'], reverse=True);  title = "Топ по монетам"

    text = f"{title}\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u[crit]}\n"

    try:
        bot.send_message(call.from_user.id, text)
        bot.answer_callback_query(call.id, "Топ отправлен в ЛС")
    except:
        bot.answer_callback_query(call.id, "Открой чат со мной, чтобы получить топ")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# === ВЫДАЧА КАРТЫ ===
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

# === АДМИНКА ТОЛЬКО ДЛЯ @clamsurr ===
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if (message.from_user.username or "").lower() != ADMIN_USERNAME:
        bot.reply_to(message, "Ты не @clamsurr")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Рассылка", callback_data="admin_broadcast"))
    markup.add(types.InlineKeyboardButton("Статистика", callback_data="admin_stats"))
    markup.add(types.InlineKeyboardButton("Сброс промо", callback_data="admin_reset"))
    bot.reply_to(message, "Админка @clamsurr", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('admin_'))
def admin_handler(call):
    if (call.from_user.username or "").lower() != ADMIN_USERNAME:
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
    if (message.from_user.username or "").lower() != ADMIN_USERNAME:
        return
    sent = 0
    for uid in bot_data:
        try:
            bot.forward_message(int(uid), message.chat.id, message.message_id)
            sent += 1
            time.sleep(0.03)
        except: pass
    bot.reply_to(message, f"Рассылка завершена. Отправлено: {sent}")

# === БОТ ВСЕГДА ПЕРВЫЙ В КОММЕНТАРИЯХ ===
@bot.message_handler(func=lambda m: getattr(m, 'sender_chat', None) and m.sender_chat.type == 'channel' and m.chat.type in ['group', 'supergroup'])
def channel_promo(message):
    key = f"{message.chat.id}_{message.message_id}"
    if key in processed_posts: return
    processed_posts.add(key)

    try:
        bot.reply_to(message, "Бот уже находится в комментариях")
    except: pass

    def promo():
        phrases = [
            "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
            "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
            "Получи свою карточку! Просто напиши «Лечинкель»"
        ]
        try:
            bot.reply_to(message, random.choice(phrases))
        except: pass
        finally:
            threading.Timer(600, processed_posts.discard, [key]).start()

    threading.Timer(random.uniform(0.9, 1.7), promo).start()

if __name__ == '__main__':
    print("Бот запущен — владелец @clamsurr")
    bot.infinity_polling(none_stop=True)
