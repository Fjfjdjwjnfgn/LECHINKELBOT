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

ADMIN_USERNAME = 'clamsurr'  # Только ты

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

# ==================== КАРТЫ ====================
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

rarities = {
    "Эпический": [], "Редкий": [], "Обычный": [], "Мифический": [], "Легендарный": []
}

for card in cards:
    rarity = card['rarity'].strip()
    if rarity == "Мифическая":
        rarity = "Мифический"
    if rarity in rarities:
        rarities[rarity].append(card)

rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [1.2, 1.5, 4, 0.1, 0.5]

# ==================== ПРОМОКОДЫ (ТВОЯ АДМИНКА) ====================
def generate_promo_code(length=8):
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    while code in bot_data.get('promocodes', {}):
        code = ''.join(random.choice(chars) for _ in range(length))
    return code

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
    bot_data['promocodes'][promo_code] = {'rarity': selected_rarity, 'used_by': []}
    save_bot_data()
    bot.answer_callback_query(call.id, f"Промокод создан: {promo_code} ({selected_rarity})")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(commands=['promo'])
def activate_promo(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Использование: /promo <код>")
        return
    code = args[1].upper()
    if code not in bot_data['promocodes']:
        bot.reply_to(message, "Неверный промокод.")
        return
    promo = bot_data['promocodes'][code]
    if user_id in promo['used_by']:
        bot.reply_to(message, "Вы уже использовали этот промокод.")
        return
    card = random.choice(rarities[promo['rarity']])
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}
    bot_data[user_id]['cards'][card['name']] = {"last_used": time.time(), "rarity": promo['rarity']}
    bot_data[user_id]['points'] += card['points']
    bot_data[user_id]['coins'] += card['coins']
    promo['used_by'].append(user_id)
    save_bot_data()
    bot.send_photo(message.chat.id, card['image_url'],
                   caption=f"Промокод активирован! Карточка «{card['name']}» добавлена.\n\n"
                           f"Редкость • {promo['rarity']}\n"
                           f"Очки • +{card['points']} [{bot_data[user_id]['points']}]\n"
                           f"Монеты • +{card['coins']} [{bot_data[user_id]['coins']}]\n",
                   reply_to_message_id=message.message_id)

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
        text += f"{code} — {data['rarity']} (использовано: {len(data['used_by'])})\n"
    bot.reply_to(message, text)

# ==================== ОСНОВНЫЕ КОМАНДЫ ====================
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

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,
                     "Что это за бот?\nТут ты можешь собирать карточки лица Лечинкеля и соревноваться с другими игроками.\n\n"
                     "Команды:\n/profile — ваш профиль\n/name [ник] — изменить никнейм\n\n"
                     "Для получения карты:\nлечинкель\nкарту, сэр\nкарту сэр\nкарту, сэр.\nполучить карту",
                     reply_to_message_id=message.message_id)

@bot.message_handler(commands=['profile'])
def send_profile(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}
        save_bot_data()
    nick = bot_data[user_id]['nickname']
    cards_cnt = len(bot_data[user_id]['cards'])
    text = f"Профиль «{nick}»\n\nID • {user_id}\nКарт • {cards_cnt} из {len(cards)}\nОчки • {bot_data[user_id]['points']}\nМонеты • {bot_data[user_id]['coins']}"
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
        bot.reply_to(message, f"Ваш никнейм изменен на «{nick}».")
    except:
        bot.reply_to(message, "Пожалуйста, укажите новый никнейм после команды /name.")

# ==================== РАБОЧИЙ ТОП ====================
@bot.message_handler(commands=['top'])
def show_top_menu(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "Эта команда доступна только в группах.")
        return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("По очкам", callback_data='top_points'),
        types.InlineKeyboardButton("По картам", callback_data='top_cards'),
        types.InlineKeyboardButton("По монетам", callback_data='top_coins')
    )
    bot.reply_to(message, "Топ 10 игроков этой группы\n\nВыберите по какому значению показать топ", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top_callback(call):
    criteria = call.data.split('_')[1]
    users = []
    for uid, data in bot_data.items():
        if uid.isdigit():
            users.append({
                'nickname': data.get('nickname', 'Без ника'),
                'points': data.get('points', 0),
                'cards_count': len(data.get('cards', {})),
                'coins': data.get('coins', 0)
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

    top_text = f"{title}\n\n"
    for i, user in enumerate(users[:10], 1):
        top_text += f"{i}. {user['nickname']} — {user[value_key]}\n"

    try:
        bot.send_message(call.from_user.id, top_text)
        bot.answer_callback_query(call.id, "Топ отправлен вам в личные сообщения.")
    except:
        bot.answer_callback_query(call.id, "Не удалось отправить топ в личку — откройте чат со мной.")

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# ==================== ВЫДАЧА КАРТЫ ====================
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ['лечинкель', 'карту, сэр', 'карту сэр', 'карту, сэр.', 'получить карту'])
def give_card(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {'balance': 0, 'cards': {}, 'points': 0, 'coins': 0,
                            'nickname': message.from_user.username or message.from_user.first_name}

    now = time.time()
    last = max((bot_data[user_id]['cards'].get(c, {}).get('last_used', 0) for c in bot_data[user_id]['cards']), default=0)

    if now - last < 10800:
        remain = 10800 - (now - last)
        h, r = divmod(int(remain), 3600)
        m, s = divmod(r, 60)
        bot.send_message(message.chat.id,
                         f"Вы осмотрелись, но не увидели рядом лица Лечинкеля\n\n"
                         f"Подождите {h}ч. {m}мин. {s}сек., чтобы попробовать снова.",
                         reply_to_message_id=message.message_id)
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

# ==================== АВТООТВЕТ В КАНАЛАХ ====================
@bot.message_handler(func=lambda m: m.sender_chat and m.sender_chat.type == 'channel' and m.chat.type == 'supergroup')
def handle_new_channel_post_in_group(message):
    phrases = [
        "Напиши «Лечинкель», чтобы открыть свою уникальную карточку!",
        "Ждёшь свою карточку? Напиши «Лечинкель» прямо сейчас!",
        "Получи свою карточку! Просто напиши «Лечинкель»"
    ]
    bot.reply_to(message, random.choice(phrases))

if __name__ == '__main__':
    print("Бот запущен — @clamsurr царь")
    bot.infinity_polling()
