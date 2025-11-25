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

ADMIN_USERNAME = 'clamsurr'

def load_bot_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {'promocodes': {}, 'users': {}}
            data = json.loads(content)
            if 'promocodes' not in data:
                data['promocodes'] = {}
            return data
    except FileNotFoundError:
        return {'promocodes': {}, 'users': {}}
    except json.JSONDecodeError as e:
        logging.error(f"JSON error: {e}")
        return {'promocodes': {}, 'users': {}}

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as f:
        json.dump(bot_data, f, ensure_ascii=False, indent=4)

bot_data = load_bot_data()

# ==================== КАРТЫ ====================
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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}
        save_bot_data()

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Добавить бота в чат", url='https://t.me/Lechinkelcards_bot?startgroup=new'))
    bot.send_message(message.chat.id,
        f"Привет, {bot_data[user_id]['nickname']}! Я бот, в котором ты можешь собирать уникальные карточки и соревноваться с другими игроками.\n\n"
        "Чтобы начать, добавь меня в группу, нажав на кнопку ниже.", 
        reply_markup=keyboard, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['profile'])
def send_profile(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}
        save_bot_data()

    nick = bot_data[user_id]['nickname']
    cards_cnt = len(bot_data[user_id]['cards'])
    points = bot_data[user_id]['points']
    coins = bot_data[user_id]['coins']

    text = f"Профиль «{nick}»\n\nID • {user_id}\nКарт • {cards_cnt} из {len(cards)}\nОчки • {points}\nМонеты • {coins}"

    try:
        photos = bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=text, reply_to_message_id=message.message_id)
            return
    except: pass
    bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['name'])
def set_nickname(message):
    user_id = str(message.from_user.id)
    try:
        nick = message.text.split(maxsplit=1)[1][:32]
        bot_data[user_id]['nickname'] = nick
        save_bot_data()
        bot.reply_to(message, f"Никнейм изменён на «{nick}»")
    except:
        bot.reply_to(message, "Укажи ник: /name ТвойНик")

# ТОП — РАБОЧИЙ
@bot.message_handler(commands=['top'])
def show_top_menu(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "Команда /top работает только в группах!")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("По очкам", callback_data="top_points"),
        types.InlineKeyboardButton("По картам", callback_data="top_cards"),
        types.InlineKeyboardButton("По монетам", callback_data="top_coins")
    )
    bot.reply_to(message, "Топ-10 игроков\n\nВыберите категорию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top(call):
    crit = call.data.split('_')[1]
    users = []
    for uid, data in bot_data.items():
        if uid.isdigit() and isinstance(data, dict):
            users.append({
                'nick': data.get('nickname', 'Без ника'),
                'points': data.get('points', 0),
                'cards': len(data.get('cards', {})),
                'coins': data.get('coins', 0)
            })

    if not users:
        bot.answer_callback_query(call.id, "Пока никто не играл")
        return

    if crit == 'points': users.sort(key=lambda x: x['points'], reverse=True); title = "Топ по очкам"
    elif crit == 'cards': users.sort(key=lambda x: x['cards'], reverse=True); title = "Топ по картам"
    else: users.sort(key=lambda x: x['coins'], reverse=True); title = "Топ по монетам"

    text = f"{title}\n\n"
    for i, u in enumerate(users[:10], 1):
        val = u['points'] if crit == 'points' else u['cards'] if crit == 'cards' else u['coins']
        text += f"{i}. {u['nick']} — {val}\n"

    try:
        bot.send_message(call.from_user.id, text)
        bot.answer_callback_query(call.id, "Топ отправлен в ЛС")
    except:
        bot.answer_callback_query(call.id, "Открой чат со мной в ЛС")

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# ВЫДАЧА КАРТЫ — ТЕКСТ КАК У ТЕБЯ БЫЛ
@bot.message_handler(func=lambda m: m.text and m.text.lower() in ['лечинкель', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту'])
def give_card(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}
        save_bot_data()

    now = time.time()
    last = max((bot_data[user_id]['cards'].get(c, {}).get('last_used', 0) for c in bot_data[user_id]['cards']), default=0)

    if now - last < 10800:
        remain = 10800 - (now - last)
        h, r = divmod(int(remain), 3600)
        m, s = divmod(r, 60)
        bot.send_message(message.chat.id,
            f"Вы осмотрелись, но не увидели рядом лица Лечинкеля\n\n"
            f"Подождите {h}ч. {m}мин. {s}сек., чтобы попробовать снова.", reply_to_message_id=message.message_id)
        return

    rarity = random.choices(rarity_order, weights=weights)[0]
    card = random.choice(rarities[rarity])

    bot_data[user_id]['cards'][card['name']] = {"last_used": now, "rarity": rarity}
    bot_data[user_id]['points'] += card['points']
    bot_data[user_id]['coins'] += card['coins']
    save_bot_data()

    bot.send_photo(message.chat.id, card['image_url'],
        caption=f"Карточка «{card['name']}» добавлена.\n\n"
                f"Редкость • {rarity}\n"
                f"Очки • +{card['points']} [{bot_data[user_id]['points']}]\n"
                f"Монеты • +{card['coins']} [{bot_data[user_id]['coins']}]\n\n"
                f"Получите следующую карточку через три часа!",
        reply_to_message_id=message.message_id)

@bot.message_handler(func=lambda m: m.sender_chat and m.sender_chat.type == 'channel' and m.chat.type == 'supergroup')
def autopromo(message):
    bot.reply_to(message, random.choice([
        "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
        "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
        "Получи свою карточку! Просто напиши «Лечинкель»"
    ]))

if __name__ == '__main__':
    print("Бот запущен. @clamsurr — бог.")
    bot.infinity_polling()
