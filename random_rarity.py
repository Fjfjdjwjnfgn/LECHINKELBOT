# -*- coding: utf-8 -*-
from random import choice

# Список всех редкостей
rarities = [
    "Обычный",
    "Редкий",
    "Эпический",
    "Мифический",
    "Легендарный"
]

# Выбираем случайно
selected = choice(rarities)

# Красивый вывод в консоль
colors = {
    "Обычный":     "\033[97m",  # белый
    "Редкий":      "\033[92m",  # зелёный
    "Эпический":   "\033[94m",  # синий
    "Мифический":  "\033[95m",  # фиолетовый
    "Легендарный": "\033[93m\033[1m"  # жёлтый + жирный
}

reset = "\033[0m"
color = colors.get(selected, "\033[97m")

print(f"{color}+==========================+{reset}")
print(f"{color}|       ВЫПАЛА РЕДКОСТЬ    |{reset}")
print(f"{color}+==========================+{reset}")
print(f"{color}   -> {selected}{reset}")
print(f"{color}==============================={reset}")

# Если хочешь просто получить строку без вывода — используй эту функцию:
def get_random_rarity():
    return choice(rarities)

# Пример использования в боте:
# rarity = get_random_rarity()