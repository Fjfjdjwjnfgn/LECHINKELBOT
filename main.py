import telebot
from telebot import types
import random
import logging
import json
import time
import threading
import string
import os
import sys
import atexit

TOKEN = "8501222332:AAG4yM_GDfB3TpJ-uikLTL5fE8FJsuqxD8g"
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

def load_promo_data():
    try:
        with open('promo_data.json', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования promo JSON: {e}")
        return []

def save_promo_data():
    with open('promo_data.json', 'w', encoding='utf-8') as file:
        json.dump(promo_data, file, ensure_ascii=False, indent=4)

def load_cards():
    try:
        with open('cards.json', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования cards JSON: {e}")
        return []

def save_cards():
    with open('cards.json', 'w', encoding='utf-8') as file:
        json.dump(cards, file, ensure_ascii=False, indent=4)

bot_data = load_bot_data()
promo_data = load_promo_data()
cards = load_cards()

def periodic_save():
    while True:
        time.sleep(60)
        try:
            save_bot_data()
            logging.debug("Periodic save completed")
        except Exception as e:
            logging.error(f"Error in periodic save: {e}")

threading.Thread(target=periodic_save, daemon=True).start()

def check_single_instance():
    # Commented out for development/testing
    # pid_file = 'bot.pid'
    # if os.path.exists(pid_file):
    #     logging.error("Another instance is running (PID file exists). Exiting.")
    #     sys.exit(1)
    # with open(pid_file, 'w') as f:
    #     f.write(str(os.getpid()))
    # atexit.register(lambda: os.remove(pid_file) if os.path.exists(pid_file) else None)
    pass
# Группировка карт по редкостям (с нормализацией названий)
rarities = {
    "Эпический": [],
    "Редкий": [],
    "Обычный": [],
    "Мифический": [],
    "Легендарный": [],
}

for card in cards:
    rarity = card['rarity'].strip()
    if rarity == "Мифическая":
        rarity = "Мифический"
    if rarity in rarities:
        rarities[rarity].append(card)

# Порядок редкостей и веса
rarity_order = ["Эпический", "Редкий", "Обычный", "Мифический", "Легендарный"]
weights = [3, 6, 10, 1, 2]

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
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
            'inventory': {'luck_booster': 0, 'time_booster': 0},
            'active_luck': False
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
        f"🎰 /lottery [ставка] — лотерея (по умолчанию 20 монет)\n"
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
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
            'inventory': {'luck_booster': 0, 'time_booster': 0},
            'active_luck': False
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

    keyboard = types.InlineKeyboardMarkup()
    button_inventory = types.InlineKeyboardButton("🎒 Инвентарь", callback_data=f"profile_inventory_{user_id}")
    button_cards = types.InlineKeyboardButton("🃏 Мои карты", callback_data=f"profile_cards_{user_id}")
    keyboard.add(button_inventory)
    keyboard.add(button_cards)

    try:
        profile_photos = bot.get_user_profile_photos(user_id)

        avatar_file_id = None
        if profile_photos.total_count > 0:
            avatar_file_id = profile_photos.photos[0][-1].file_id

        if avatar_file_id:
            bot.send_photo(message.chat.id, avatar_file_id, caption=profile_text, reply_markup=keyboard, reply_to_message_id=message.message_id)
            logging.debug(f"User {user_id} profile with photo sent")
        else:
            bot.send_message(message.chat.id, profile_text, reply_markup=keyboard, reply_to_message_id=message.message_id)
            logging.debug(f"User {user_id} profile sent")

    except Exception as e:
        logging.error(f"User {user_id} error sending profile: {e}")
        bot.send_message(message.chat.id, profile_text, reply_markup=keyboard, reply_to_message_id=message.message_id)
        logging.debug(f"User {user_id} profile sent on error")

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
def send_top(message):
    user_id = str(message.from_user.id)
    logging.debug(f"User {user_id} requested top")

    text = "🏆 Топ 10 игроков этой группы\n\n> Выберите по какому значению показать топ"

    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("По очкам", callback_data=f"top_points_{user_id}")
    button2 = types.InlineKeyboardButton("По картам", callback_data=f"top_cards_{user_id}")
    button3 = types.InlineKeyboardButton("По монетам", callback_data=f"top_coins_{user_id}")
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    bot.send_message(message.chat.id, text, reply_markup=keyboard, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['my_cards'])
def show_my_cards(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot.send_message(message.chat.id, "У вас нет карт.", reply_to_message_id=message.message_id)
        return
    user_cards = bot_data[user_id]['cards']
    if not user_cards:
        bot.send_message(message.chat.id, "У вас нет карт.", reply_to_message_id=message.message_id)
        return
    text = "Ваши карты:\n\n"
    for card_name, data in user_cards.items():
        rarity = data['rarity']
        points = data['points_earned']
        text += f"🃏 {card_name}\n💎 {rarity}\n✨ +{points}\n\n"
    bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['shop'])
def send_shop(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
            'inventory': {'luck_booster': 0, 'time_booster': 0},
            'active_luck': False
        }
        save_bot_data()
    keyboard = types.InlineKeyboardMarkup()
    button_luck = types.InlineKeyboardButton("🍀 Удача", callback_data=f"shop_luck_{user_id}")
    button_time = types.InlineKeyboardButton("⚡ Ускоритель времени", callback_data=f"shop_time_{user_id}")
    keyboard.add(button_luck)
    keyboard.add(button_time)
    bot.send_message(message.chat.id, "⚡️ Бустеры\nВыберите нужный бустер", reply_markup=keyboard, reply_to_message_id=message.message_id)

@bot.message_handler(commands=['promo'])
def redeem_promo(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
            'inventory': {'luck_booster': 0, 'time_booster': 0},
            'active_luck': False
        }
        save_bot_data()
    code = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not code:
        bot.send_message(message.chat.id, "Укажите код промокода после /promo", reply_to_message_id=message.message_id)
        return
    promo = next((p for p in promo_data if p['code'] == code.upper()), None)
    if not promo:
        bot.send_message(message.chat.id, "Промокод не найден.", reply_to_message_id=message.message_id)
        return
    if 'created' in promo and time.time() - promo['created'] > promo['duration'] * 86400:
        bot.send_message(message.chat.id, "Промокод истек.", reply_to_message_id=message.message_id)
        return
    if promo['used'] >= promo['activations']:
        bot.send_message(message.chat.id, "Промокод исчерпан.", reply_to_message_id=message.message_id)
        return
    rarity = promo['rarity']
    if rarity not in rarities or not rarities[rarity]:
        bot.send_message(message.chat.id, "Ошибка редкости.", reply_to_message_id=message.message_id)
        return
    card = random.choice(rarities[rarity])
    points = card['points']
    coins = card['coins']
    bot_data[user_id]['cards'][card["name"]] = {
        "last_used": 0,  # No cooldown for promo
        "rarity": rarity,
        "points_earned": points,
        "coins_earned": coins
    }
    bot_data[user_id]['points'] += points
    bot_data[user_id]['coins'] += coins
    promo['used'] += 1
    save_bot_data()
    save_promo_data()
    response = f"Промокод активирован!\n\n🃏 {card['name']}\n💎 {rarity}\n✨ +{points}\n💰 +{coins}"
    bot.send_photo(message.chat.id, card["image_url"], caption=response, reply_to_message_id=message.message_id)

admin_state = {}

@bot.message_handler(commands=['admin'])
def send_admin(message):
    if message.from_user.username and message.from_user.username.lower() not in ['clamsurr', 'kamarkahetman']:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.", reply_to_message_id=message.message_id)
        return
    keyboard = types.InlineKeyboardMarkup()
    button_mailing = types.InlineKeyboardButton("Рассылка", callback_data="admin_mailing")
    button_stats = types.InlineKeyboardButton("Статистика", callback_data="admin_stats")
    button_create_promo = types.InlineKeyboardButton("Создание промокода", callback_data="admin_create_duration")
    button_list_promo = types.InlineKeyboardButton("Список промокодов", callback_data="admin_list_promo")
    button_add_card = types.InlineKeyboardButton("Добавить Новую Карточку", callback_data="admin_add_card")
    button_delete_card = types.InlineKeyboardButton("Удалить Карточку", callback_data="admin_delete_card")
    keyboard.add(button_mailing)
    keyboard.add(button_stats)
    keyboard.add(button_create_promo)
    keyboard.add(button_list_promo)
    keyboard.add(button_add_card)
    keyboard.add(button_delete_card)
    bot.send_message(message.chat.id, "Админ панель:", reply_markup=keyboard)

@bot.message_handler(commands=['lottery'])
def play_lottery(message):
    user_id = str(message.from_user.id)
    if user_id not in bot_data:
        bot_data[user_id] = {
            'balance': 0,
            'cards': {},
            'points': 0,
            'coins': 0,
            'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
            'inventory': {'luck_booster': 0, 'time_booster': 0},
            'active_luck': False
        }
        save_bot_data()
    if 'inventory' not in bot_data[user_id]:
        bot_data[user_id]['inventory'] = {'luck_booster': 0, 'time_booster': 0}
    if 'active_luck' not in bot_data[user_id]:
        bot_data[user_id]['active_luck'] = False

    # Parse bet amount
    parts = message.text.split()
    if len(parts) > 1:
        try:
            bet = int(parts[1])
            if bet < 1:
                bot.send_message(message.chat.id, "Ставка должна быть положительным числом.", reply_to_message_id=message.message_id)
                return
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат ставки. Используйте /lottery <число>", reply_to_message_id=message.message_id)
            return
    else:
        bet = 20  # default

    if bot_data[user_id]['coins'] < bet:
        bot.send_message(message.chat.id, f"💰 У вас недостаточно монет для лотереи (нужно {bet} монет).", reply_to_message_id=message.message_id)
        return
    bot_data[user_id]['coins'] -= bet

    # Scale rewards and chances based on bet
    multiplier = bet // 20  # for bet 20, multiplier 1, for 40, 2, etc.
    if multiplier < 1:
        multiplier = 1

    # Casino-like chances: mostly lose, small chance to win coins
    weights = [95, 5]  # 5% win chance

    # Rewards: 0: nothing, 1: coins (variable)
    reward = random.choices([0, 1], weights=weights)[0]
    if reward == 0:
        text = "😔 К сожалению, вы ничего не выиграли. Попробуйте ещё раз!"
    elif reward == 1:
        coins_won = random.randint(bet, bet * 3)  # profit
        bot_data[user_id]['coins'] += coins_won
        text = f"🎉 Поздравляем! Вы выиграли {coins_won} монет!"

    save_bot_data()
    bot.send_message(message.chat.id, f"🎰 Вы сыграли в лотерею (ставка {bet} монет)!\n\n{text}\n\n💰 Осталось монет: {bot_data[user_id]['coins']}", reply_to_message_id=message.message_id)

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
           'nickname': message.from_user.username if message.from_user.username else message.from_user.first_name,
           'inventory': {'luck_booster': 0, 'time_booster': 0},
           'active_luck': False
       }
   if 'inventory' not in bot_data[user_id]:
       bot_data[user_id]['inventory'] = {'luck_booster': 0, 'time_booster': 0}
   if 'active_luck' not in bot_data[user_id]:
       bot_data[user_id]['active_luck'] = False

   current_time = time.time()

   # Check for pending card from previous error
   if 'pending_card' in bot_data[user_id]:
       pending = bot_data[user_id]['pending_card']
       card = pending['card']
       selected_rarity = pending['rarity']
       logging.info(f"Giving pending card {card['name']} to user {user_id}")

       points_earned = card['points']
       coins_earned = card['coins']

       bot_data[user_id]['cards'][card["name"]] = {
           "last_used": current_time,
           "rarity": selected_rarity,
           "points_earned": points_earned,
           "coins_earned": coins_earned
       }
       bot_data[user_id]['last_card'] = card["name"]

       bot_data[user_id]['points'] += points_earned
       bot_data[user_id]['coins'] += coins_earned
       save_bot_data()

       del bot_data[user_id]['pending_card']

       response = (
           f"🃏 Карточка «{card['name']}» добавлена (повтор после ошибки).\n\n"
           f"💎 Редкость • {selected_rarity}\n"
           f"✨ Очки • +{points_earned} [{bot_data[user_id]['points']}]\n"
           f"💰 Монеты • +{coins_earned} [{bot_data[user_id]['coins']}]\n\n"
           f"🎁 Получите следующую карточку через три часа!"
       )

       bot.send_photo(message.chat.id, card["image_url"], caption=response, reply_to_message_id=message.message_id)
       return

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

   try:
       # Выбор редкости с весами
       current_weights = weights
       if bot_data[user_id]['active_luck']:
           # Increase rare and mythic chances
           current_weights = [4, 8, 8, 4, 2]  # Boost rare and mythic
           bot_data[user_id]['active_luck'] = False
       selected_rarity = random.choices(rarity_order, weights=current_weights)[0]
       owned_cards = set(bot_data[user_id]['cards'].keys())
       available_cards = [c for c in rarities[selected_rarity] if c["name"] not in owned_cards and c["name"] != bot_data[user_id].get('last_card')]
       if not available_cards:
           available_cards = [c for c in rarities[selected_rarity] if c["name"] not in owned_cards]
       if not available_cards:
           available_cards = rarities[selected_rarity]  # If all owned, allow duplicate
       card = random.choice(available_cards)

       points_earned = card['points']
       coins_earned = card['coins']

       # Store pending in case of error
       bot_data[user_id]['pending_card'] = {'card': card, 'rarity': selected_rarity}

       bot_data[user_id]['cards'][card["name"]] = {
           "last_used": current_time,
           "rarity": selected_rarity,
           "points_earned": points_earned,
           "coins_earned": coins_earned
       }
       bot_data[user_id]['last_card'] = card["name"]

       bot_data[user_id]['points'] += points_earned
       bot_data[user_id]['coins'] += coins_earned
       save_bot_data()

       del bot_data[user_id]['pending_card']

       logging.info(f"Giving card {card['name']} to user {user_id}")

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
       # Pending card is stored, no cooldown applied
       bot.send_message(message.chat.id, "Произошла ошибка при получении карточки. Попробуйте еще раз (без cooldown).", reply_to_message_id=message.message_id)

@bot.message_handler(func=lambda message: admin_state.get('mailing') and message.from_user.username and message.from_user.username.lower() in ['clamsurr', 'kamarkahetman'] and message.chat.type == 'private')
def handle_admin_mailing(message):
    logging.debug(f"Admin mailing: {message.text}")
    admin_state['mailing'] = False
    sent_count = 0
    for user_id in bot_data.keys():
        try:
            bot.send_message(int(user_id), message.text)
            sent_count += 1
        except Exception as e:
            logging.error(f"Failed to send to {user_id}: {e}")
    bot.send_message(message.chat.id, f"Рассылка завершена. Отправлено: {sent_count}")

@bot.message_handler(func=lambda message: admin_state.get('add_card') and message.from_user.username and message.from_user.username.lower() in ['clamsurr', 'kamarkahetman'] and message.chat.type == 'private')
def handle_admin_add_card(message):
    state = admin_state['add_card']
    step = state['step']
    if step == 'name':
        state['name'] = message.text
        state['step'] = 'image'
        bot.send_message(message.chat.id, "Введите ссылку на изображение:")
    elif step == 'image':
        state['image_url'] = message.text
        state['step'] = 'rarity'
        keyboard = types.InlineKeyboardMarkup()
        rarities_list = ["Обычный", "Редкий", "Эпический", "Мифический", "Легендарный"]
        for r in rarities_list:
            button = types.InlineKeyboardButton(r, callback_data=f"admin_add_rarity_{r}")
            keyboard.add(button)
        bot.send_message(message.chat.id, "Выберите редкость:", reply_markup=keyboard)
    elif step == 'coins':
        try:
            state['coins'] = int(message.text)
            state['step'] = 'points'
            bot.send_message(message.chat.id, "Введите количество очков:")
        except ValueError:
            bot.send_message(message.chat.id, "Введите число для монет.")
    elif step == 'points':
        try:
            state['points'] = int(message.text)
            # Add the card
            new_card = {
                'name': state['name'],
                'rarity': state['rarity'],
                'points': state['points'],
                'coins': state['coins'],
                'image_url': state['image_url']
            }
            cards.append(new_card)
            save_cards()
            # Update rarities
            rarities[state['rarity']].append(new_card)
            bot.send_message(message.chat.id, "КАРТОЧКА УСПЕШНО ДОБАВЛЕНА")
            del admin_state['add_card']
        except ValueError:
            bot.send_message(message.chat.id, "Введите число для очков.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_top_callback(call):
    parts = call.data.split('_')
    if len(parts) != 3:
        return
    criteria = parts[1]
    initiator_id = parts[2]

    if str(call.from_user.id) != initiator_id:
        bot.answer_callback_query(call.id, "Эта команда доступна только тому, кто её вызвал.", show_alert=True)
        return

    if criteria == 'back':
        text = "🏆 Топ 10 игроков этой группы\n\n> Выберите по какому значению показать топ"
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("По очкам", callback_data=f"top_points_{initiator_id}")
        button2 = types.InlineKeyboardButton("По картам", callback_data=f"top_cards_{initiator_id}")
        button3 = types.InlineKeyboardButton("По монетам", callback_data=f"top_coins_{initiator_id}")
        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)

    # Get top 10
    users = []
    for user_id, data in bot_data.items():
        if criteria == 'points':
            value = data.get('points', 0)
        elif criteria == 'cards':
            value = len(data.get('cards', {}))
        elif criteria == 'coins':
            value = data.get('coins', 0)
        else:
            return
        users.append((user_id, data.get('nickname', 'Unknown'), value))

    # Sort descending
    users.sort(key=lambda x: x[2], reverse=True)
    top_10 = users[:10]

    # Format text
    criteria_name = {'points': 'очкам', 'cards': 'картам', 'coins': 'монетам'}[criteria]
    text = f"🏆 Топ 10 игроков по {criteria_name}\n\n"
    for i, (user_id, nickname, value) in enumerate(top_10, 1):
        text += f"{i}. {nickname} — {value}\n"

    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Назад", callback_data=f"top_back_{initiator_id}")
    keyboard.add(back_button)

    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('profile_'))
def handle_profile_callback(call):
    parts = call.data.split('_', 1)
    action = parts[1]
    rest = '' if len(parts) < 2 else parts[1].split('_', 1)[1]
    user_id = rest.split('_')[-1] if rest else ''
    if str(call.from_user.id) != user_id:
        bot.answer_callback_query(call.id, "Это не ваш профиль.", show_alert=True)
        return
    if call.message.photo:
        edit_func = lambda text, markup: bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    else:
        edit_func = lambda text, markup: bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    if action.startswith('inventory'):
        keyboard = types.InlineKeyboardMarkup()
        button_boosters = types.InlineKeyboardButton("⚡️ Бустеры", callback_data=f"profile_boosters_{user_id}")
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"profile_back_{user_id}")
        keyboard.add(button_boosters)
        keyboard.add(back_button)
        edit_func("🎒 Инвентарь\nВыберите тип предмета", keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('cards'):
        keyboard = types.InlineKeyboardMarkup()
        button_common = types.InlineKeyboardButton("🍁 Обычные", callback_data=f"profile_rarity_Обычный_{user_id}")
        button_rare = types.InlineKeyboardButton("🧪 Редкие", callback_data=f"profile_rarity_Редкий_{user_id}")
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"profile_back_{user_id}")
        keyboard.add(button_common)
        keyboard.add(button_rare)
        keyboard.add(back_button)
        edit_func("Выберите редкость карт:", keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('rarity'):
        rarity = rest.split('_')[0]
        user_cards = bot_data[user_id]['cards']
        cards_of_rarity = [name for name, data in user_cards.items() if data['rarity'] == rarity]
        if not cards_of_rarity:
            edit_func(f"У вас нет карт редкости {rarity}", None)
            bot.answer_callback_query(call.id)
            return
        keyboard = types.InlineKeyboardMarkup()
        for i, card_name in enumerate(cards_of_rarity):
            button = types.InlineKeyboardButton(card_name, callback_data=f"profile_card_{i}_{user_id}")
            keyboard.add(button)
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"profile_cards_{user_id}")
        keyboard.add(back_button)
        edit_func(f"Карты редкости {rarity}:", keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('card'):
        card_name = rest.rsplit('_', 1)[0]
        if card_name not in bot_data[user_id]['cards']:
            bot.answer_callback_query(call.id, "Карта не найдена.", show_alert=True)
            return
        card_data = bot_data[user_id]['cards'][card_name]
        rarity = card_data['rarity']
        points = card_data['points_earned']
        global_card = next((c for c in cards if c['name'] == card_name), None)
        if not global_card:
            bot.answer_callback_query(call.id, "Ошибка данных карты.", show_alert=True)
            return
        image_url = global_card['image_url']
        caption = f"{card_name}\n\n💎 Редкость • {rarity}\n✨ Очки • {points}"
        bot.send_photo(call.message.chat.id, image_url, caption=caption, reply_to_message_id=call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action.startswith('back'):
        # Back to profile main
        profile_text = (
           f"Профиль «{bot_data[user_id]['nickname']}»\n\n"
           f"🔎 ID • {user_id}\n"
           f"🃏 Карт • {len(bot_data[user_id]['cards'])} из {len(cards)}\n"
           f"✨ Очки • {bot_data[user_id]['points']}\n"
           f"💰 Монеты • {bot_data[user_id]['coins']}"
        )
        keyboard = types.InlineKeyboardMarkup()
        button_inventory = types.InlineKeyboardButton("🎒 Инвентарь", callback_data=f"profile_inventory_{user_id}")
        button_cards = types.InlineKeyboardButton("🃏 Мои карты", callback_data=f"profile_cards_{user_id}")
        keyboard.add(button_inventory)
        keyboard.add(button_cards)
        edit_func(profile_text, keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('boosters'):
        inventory = bot_data[user_id]['inventory']
        if inventory['luck_booster'] == 0 and inventory['time_booster'] == 0:
            edit_func("У вас нет бустеров.", None)
            bot.answer_callback_query(call.id)
            return
        keyboard = types.InlineKeyboardMarkup()
        if inventory['luck_booster'] > 0:
            button_luck = types.InlineKeyboardButton(f"🍀 Удача [{inventory['luck_booster']} шт]", callback_data=f"profile_activate_luck_{user_id}")
            keyboard.add(button_luck)
        if inventory['time_booster'] > 0:
            button_time = types.InlineKeyboardButton(f"⚡ Ускоритель [{inventory['time_booster']} шт]", callback_data=f"profile_activate_time_{user_id}")
            keyboard.add(button_time)
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"profile_inventory_{user_id}")
        keyboard.add(back_button)
        edit_func("⚡️ Бустеры", keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('activate'):
        booster = rest.split('_')[0]
        if booster == 'luck':
            if bot_data[user_id]['inventory']['luck_booster'] > 0:
                bot_data[user_id]['inventory']['luck_booster'] -= 1
                bot_data[user_id]['active_luck'] = True
                save_bot_data()
                edit_func("🍀 Бустер удачи активирован!", None)
            else:
                edit_func("У вас нет бустера удачи.", None)
        elif booster == 'time':
            if bot_data[user_id]['inventory']['time_booster'] > 0:
                bot_data[user_id]['inventory']['time_booster'] -= 1
                # Reduce cooldown by 1 hour
                max_last = max((data['last_used'] for data in bot_data[user_id]['cards'].values()), default=0)
                if max_last > 0:
                    new_last = max(0, max_last - 3600)
                    for card_data in bot_data[user_id]['cards'].values():
                        if card_data['last_used'] == max_last:
                            card_data['last_used'] = new_last
                    save_bot_data()
                edit_func("⚡ Бустер ускорителя активирован!", None)
            else:
                edit_func("У вас нет бустера ускорителя.", None)
        bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('shop_'))
def handle_shop_callback(call):
    parts = call.data.split('_', 1)
    booster = parts[1].split('_')[0]
    user_id = parts[1].split('_')[1]
    # Allow anyone to view, but check for buy
    if booster == 'luck':
        text = "🍀 Бустер «удача»\n\nУвеличивает вероятность выпадения редких и мифических карт\n\n💰 Цена • 40 монет\n⌚️ Время действия • однократное использование"
        keyboard = types.InlineKeyboardMarkup()
        buy_button = types.InlineKeyboardButton("Купить", callback_data=f"shop_buy_luck_{user_id}")
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"shop_back_{user_id}")
        keyboard.add(buy_button)
        keyboard.add(back_button)
    elif booster == 'time':
        text = "⚡ Бустер «ускоритель времени»\n\nСокращает время ожидания получения карточки на 1 час\n\n💰 Цена • 70 монет\n⌚️ Время действия • однократное использование"
        keyboard = types.InlineKeyboardMarkup()
        buy_button = types.InlineKeyboardButton("Купить", callback_data=f"shop_buy_time_{user_id}")
        back_button = types.InlineKeyboardButton("Назад", callback_data=f"shop_back_{user_id}")
        keyboard.add(buy_button)
        keyboard.add(back_button)
    elif booster == 'back':
        keyboard = types.InlineKeyboardMarkup()
        button_luck = types.InlineKeyboardButton("🍀 Удача", callback_data=f"shop_luck_{user_id}")
        button_time = types.InlineKeyboardButton("⚡ Ускоритель времени", callback_data=f"shop_time_{user_id}")
        keyboard.add(button_luck)
        keyboard.add(button_time)
        bot.edit_message_text("⚡️ Бустеры\nВыберите нужный бустер", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
        return
    elif booster == 'buy':
        buyer_id = str(call.from_user.id)
        if buyer_id not in bot_data:
            bot_data[buyer_id] = {
                'balance': 0,
                'cards': {},
                'points': 0,
                'coins': 0,
                'nickname': call.from_user.username or 'Unknown',
                'inventory': {'luck_booster': 0, 'time_booster': 0},
                'active_luck': False
            }
            save_bot_data()
        if 'inventory' not in bot_data[buyer_id]:
            bot_data[buyer_id]['inventory'] = {'luck_booster': 0, 'time_booster': 0}
        if 'active_luck' not in bot_data[buyer_id]:
            bot_data[buyer_id]['active_luck'] = False
        save_bot_data()
        item = parts[1].split('_')[1]
        if item == 'luck':
            price = 40
            item_name = 'luck_booster'
        elif item == 'time':
            price = 70
            item_name = 'time_booster'
        else:
            return
        current_time = time.time()
        last_buy = bot_data[buyer_id].get('last_shop_buy', 0)
        if current_time - last_buy < 3 * 3600:
            remaining = 3 * 3600 - (current_time - last_buy)
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            bot.answer_callback_query(call.id, f"Подождите {hours}ч. {minutes}мин. перед следующей покупкой.", show_alert=True)
            return
        if bot_data[buyer_id]['coins'] < price:
            bot.answer_callback_query(call.id, "💰 У вас недостаточно монет", show_alert=True)
            return
        bot_data[buyer_id]['coins'] -= price
        bot_data[buyer_id]['inventory'][item_name] += 1
        bot_data[buyer_id]['last_shop_buy'] = current_time
        save_bot_data()
        bot.answer_callback_query(call.id, f"Куплено! Осталось монет: {bot_data[buyer_id]['coins']}", show_alert=True)
        return
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_callback(call):
    logging.debug(f"Admin callback: {call.data} from {call.from_user.username}")
    if call.from_user.username and call.from_user.username.lower() not in ['clamsurr', 'kamarkahetman']:
        bot.answer_callback_query(call.id, "Нет доступа.", show_alert=True)
        return
    parts = call.data.split('_', 1)
    action = parts[1]
    logging.debug(f"Admin action: {action}")
    if action == 'mailing':
        admin_state['mailing'] = True
        bot.edit_message_text("Отправьте сообщение для рассылки:", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'stats':
        total_users = len(bot_data)
        total_cards = sum(len(data.get('cards', {})) for data in bot_data.values())
        total_points = sum(data.get('points', 0) for data in bot_data.values())
        total_coins = sum(data.get('coins', 0) for data in bot_data.values())
        stats_text = f"Статистика:\nПользователей: {total_users}\nВсего карт: {total_cards}\nВсего очков: {total_points}\nВсего монет: {total_coins}"
        bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'list_promo':
        if not promo_data:
            text = "Нет промокодов."
        else:
            text = "Промокоды:\n"
            for p in promo_data:
                text += f"{p['code']} - {p['rarity']} - {p['used']}/{p['activations']}\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'create_duration':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("1 день", callback_data="admin_create_activations_1")
        button7 = types.InlineKeyboardButton("7 дней", callback_data="admin_create_activations_7")
        button30 = types.InlineKeyboardButton("30 дней", callback_data="admin_create_activations_30")
        keyboard.add(button1)
        keyboard.add(button7)
        keyboard.add(button30)
        bot.edit_message_text("Выберите длительность промокода:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('create_activations_'):
        duration = int(action.split('_')[-1])
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("1 активация", callback_data=f"admin_create_rarity_{duration}_1")
        button5 = types.InlineKeyboardButton("5 активаций", callback_data=f"admin_create_rarity_{duration}_5")
        button10 = types.InlineKeyboardButton("10 активаций", callback_data=f"admin_create_rarity_{duration}_10")
        button100 = types.InlineKeyboardButton("100 активаций", callback_data=f"admin_create_rarity_{duration}_100")
        keyboard.add(button1)
        keyboard.add(button5)
        keyboard.add(button10)
        keyboard.add(button100)
        bot.edit_message_text("Выберите количество активаций:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('create_rarity_'):
        parts2 = action.split('_')
        duration = int(parts2[2])
        activations = int(parts2[3])
        keyboard = types.InlineKeyboardMarkup()
        rarities_list = ["Обычный", "Редкий", "Эпический", "Мифический", "Легендарный"]
        for r in rarities_list:
            button = types.InlineKeyboardButton(r, callback_data=f"admin_create_final_{duration}_{activations}_{r}")
            keyboard.add(button)
        bot.edit_message_text("Выберите редкость карты:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('create_final_'):
        parts2 = action.split('_')
        duration = int(parts2[2])
        activations = int(parts2[3])
        rarity = '_'.join(parts2[4:])
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        promo_data.append({
            'code': code,
            'rarity': rarity,
            'duration': duration,
            'activations': activations,
            'used': 0,

            'created': time.time()
        })
        save_promo_data()
        bot.edit_message_text(f"Промокод создан: {code}", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'add_card':
        admin_state['add_card'] = {'step': 'name'}
        bot.edit_message_text("Введите название карточки:", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'delete_card':
        if not cards:
            bot.edit_message_text("Нет карточек для удаления.", call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
            return
        text = "Выберите карточку для удаления:\n\n"
        keyboard = types.InlineKeyboardMarkup()
        for i, card in enumerate(cards):
            text += f"{i+1}. {card['name']}\n"
            button = types.InlineKeyboardButton(card['name'], callback_data=f"admin_delete_select_{i}")
            keyboard.add(button)
        back_button = types.InlineKeyboardButton("Назад", callback_data="admin_back")
        keyboard.add(back_button)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    elif action.startswith('delete_select_'):
        index = int(action.split('_')[-1])
        if index < len(cards):
            admin_state['delete_card'] = {'index': index}
            keyboard = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton("Удалить Карточку", callback_data=f"admin_delete_confirm_{index}")
            back_button = types.InlineKeyboardButton("Назад", callback_data="admin_delete_card")
            keyboard.add(confirm_button)
            keyboard.add(back_button)
            card = cards[index]
            caption = f"Удалить карточку «{card['name']}»?\n\n💎 Редкость • {card['rarity']}\n✨ Очки • {card['points']}\n💰 Монеты • {card['coins']}"
            bot.send_photo(call.message.chat.id, card['image_url'], caption=caption, reply_markup=keyboard)
            bot.answer_callback_query(call.id)
    elif action.startswith('delete_confirm_'):
        index = int(action.split('_')[-1])
        if index < len(cards):
            deleted_card = cards.pop(index)
            save_cards()
            # Update rarities
            rarities = {k: [] for k in rarities}
            for card in cards:
                rarity = card['rarity'].strip()
                if rarity == "Мифическая":
                    rarity = "Мифический"
                if rarity in rarities:
                    rarities[rarity].append(card)
            bot.edit_message_caption(caption="КАРТОЧКА УСПЕШНО УДАЛЕНА", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id)
    elif action.startswith('add_rarity_'):
        rarity = '_'.join(action.split('_')[2:])
        admin_state['add_card']['rarity'] = rarity
        admin_state['add_card']['step'] = 'coins'
        bot.edit_message_text("Введите количество монет:", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == 'back':
        keyboard = types.InlineKeyboardMarkup()
        button_mailing = types.InlineKeyboardButton("Рассылка", callback_data="admin_mailing")
        button_stats = types.InlineKeyboardButton("Статистика", callback_data="admin_stats")
        button_create_promo = types.InlineKeyboardButton("Создание промокода", callback_data="admin_create_duration")
        button_list_promo = types.InlineKeyboardButton("Список промокодов", callback_data="admin_list_promo")
        button_add_card = types.InlineKeyboardButton("Добавить Новую Карточку", callback_data="admin_add_card")
        button_delete_card = types.InlineKeyboardButton("Удалить Карточку", callback_data="admin_delete_card")
        keyboard.add(button_mailing)
        keyboard.add(button_stats)
        keyboard.add(button_create_promo)
        keyboard.add(button_list_promo)
        keyboard.add(button_add_card)
        keyboard.add(button_delete_card)
        bot.edit_message_text("Админ панель:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id)

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
    check_single_instance()
    while True:
        try:
            bot.delete_webhook()
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Bot crashed: {e}, restarting in 5 seconds...")
            time.sleep(5)
