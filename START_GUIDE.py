#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 RULETTT - Интерактивное руководство по использованию
======================================================

Пошаговый гайд для начала работы с системой
"""

import os
import sys
from pathlib import Path
import time

# Исправление кодировки для Windows PowerShell
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Красивый заголовок"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def print_step(number, text):
    """Шаг инструкции"""
    print(f"\n{'='*80}")
    print(f"📍 ШАГ {number}: {text}")
    print(f"{'='*80}\n")

def wait_for_user():
    """Ожидание нажатия Enter"""
    input("\n⏎ Нажмите ENTER для продолжения...")

# Начало
clear_screen()
print_header("🎲 ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ RULETTT!")

print("""
Это интерактивное руководство поможет вам:

✅ Запустить все сервисы
✅ Открыть Dashboard для мониторинга
✅ Начать сбор данных рулетки
✅ Анализировать результаты
✅ Тестировать стратегии

Приготовьтесь к захватывающему путешествию! 🚀
""")

wait_for_user()

# ШАГ 1: Проверка системы
print_step(1, "ПРОВЕРКА СИСТЕМЫ")

print("🔍 Проверяем готовность системы...\n")

# Проверка файлов
files_to_check = [
    ('api_server.py', 'API сервер'),
    ('webapp/dashboard.html', 'Главная страница'),
    ('webapp/logs_dashboard.html', 'Dashboard логов'),
    ('src/logger.py', 'Система логирования'),
    ('src/error_tracker.py', 'Трекер ошибок')
]

all_ok = True
for file, name in files_to_check:
    if Path(file).exists():
        print(f"   ✅ {name}")
    else:
        print(f"   ❌ {name} - НЕ НАЙДЕН")
        all_ok = False

if all_ok:
    print("\n🎉 Все компоненты на месте! Можем продолжать.")
else:
    print("\n⚠️  Некоторые файлы отсутствуют. Проверьте установку.")
    sys.exit(1)

wait_for_user()

# ШАГ 2: Запуск сервисов
print_step(2, "ЗАПУСК СЕРВИСОВ")

print("""
Нам нужно запустить 2 сервиса:

1️⃣  API сервер (порт 5000) - обрабатывает данные
2️⃣  Веб-сервер (порт 8080) - показывает интерфейс

🎯 ВАРИАНТЫ ЗАПУСКА:
""")

print("""
Вариант A: Автоматический (рекомендуется)
   Запустите файл: START_RULETTT.bat
   Он автоматически запустит оба сервиса

Вариант B: Ручной (для опытных)
   Терминал 1: py api_server.py
   Терминал 2: cd webapp && py -m http.server 8080

Вариант C: VS Code задачи
   Ctrl+Shift+P → "Tasks: Run Task"
   → "🎲 Запустить все сервисы RULETTT"
""")

choice = input("Выберите вариант (A/B/C) или Enter для продолжения: ").upper()

if choice == 'A':
    print("\n🚀 Запускаю START_RULETTT.bat...")
    os.system('START_RULETTT.bat')
    time.sleep(5)
elif choice == 'B':
    print("""
    \n📝 Откройте 2 терминала PowerShell:
    
    Терминал 1:
    py api_server.py
    
    Терминал 2:
    cd webapp
    py -m http.server 8080
    """)
    wait_for_user()

print("\n✅ Сервисы должны быть запущены!")

wait_for_user()

# ШАГ 3: Проверка работы
print_step(3, "ПРОВЕРКА РАБОТЫ СЕРВИСОВ")

print("🔍 Проверяем доступность сервисов...\n")

import urllib.request
import json

services = [
    ('http://localhost:5000/api/health', 'API сервер'),
    ('http://localhost:8080/dashboard.html', 'Веб-сервер'),
]

for url, name in services:
    try:
        response = urllib.request.urlopen(url, timeout=3)
        print(f"   ✅ {name} - РАБОТАЕТ")
    except Exception as e:
        print(f"   ❌ {name} - НЕ ДОСТУПЕН")
        print(f"      Ошибка: {e}")

wait_for_user()

# ШАГ 4: Открытие Dashboard
print_step(4, "ОТКРЫВАЕМ DASHBOARD")

print("""
🎯 Сейчас откроется Dashboard для мониторинга системы.

На Dashboard вы увидите:
   📊 Логи в реальном времени
   🚨 Отслеживание ошибок
   📈 Статистику производительности
   🔍 События пользователей

Готовы? 🚀
""")

wait_for_user()

print("\n🌐 Открываю Dashboard...")
os.system('start http://localhost:8080/logs_dashboard.html')
time.sleep(2)

print("""
✅ Dashboard открыт в браузере!

Что вы видите:
   🔵 Вкладка "Логи" - все логи системы
   🔴 Вкладка "Ошибки" - детали ошибок
   🟢 Вкладка "События" - действия пользователей
   🟡 Вкладка "Статистика" - общая статистика
""")

wait_for_user()

# ШАГ 5: Тестирование логирования
print_step(5, "ТЕСТИРОВАНИЕ СИСТЕМЫ ЛОГИРОВАНИЯ")

print("""
🧪 Сейчас мы запустим тест, который:
   ✅ Создаст тестовые логи
   ✅ Запишет их в файлы
   ✅ Отправит события на API
   ✅ Покажет производительность

Логи появятся в Dashboard в реальном времени!
""")

wait_for_user()

print("\n🚀 Запускаю тест логирования...\n")
os.system('py test_logging.py')

print("""
\n✅ Тест завершён!

📊 Проверьте Dashboard:
   1. Обновите вкладку "Логи"
   2. Посмотрите сгенерированные записи
   3. Проверьте фильтры

""")

wait_for_user()

# ШАГ 6: Сбор данных рулетки
print_step(6, "НАЧАЛО СБОРА ДАННЫХ РУЛЕТКИ")

print("""
🎰 СБОР ДАННЫХ С РЕАЛЬНОЙ РУЛЕТКИ

Есть 2 способа:

Способ 1: Автоматический сборщик (JavaScript в браузере)
   1. Откройте сайт казино (например, PragmaticPlay)
   2. Нажмите F12 (откроется консоль)
   3. Скопируйте код из auto_collector_console_code.js
   4. Вставьте в консоль и нажмите Enter
   5. Данные собираются автоматически каждые 30 секунд!

Способ 2: Ручной ввод через API
   Отправьте POST запрос:
   
   curl -X POST http://localhost:5000/api/spins \\
        -H "Content-Type: application/json" \\
        -d '{"number": 17, "color": "black", "casino_name": "test"}'

Способ 3: Генератор тестовых данных
   Запустите: py src/main.py
   Выберите: "1. Управление данными" → "2. Генерация тестовых данных"
""")

choice = input("\nКакой способ хотите использовать? (1/2/3) или Enter для пропуска: ")

if choice == '1':
    print("""
    \n📋 ИНСТРУКЦИЯ:
    
    1. Откройте новую вкладку браузера
    2. Перейдите на сайт с рулеткой
    3. Нажмите F12 (консоль разработчика)
    4. Файл auto_collector_console_code.js уже готов
    5. Скопируйте его содержимое в консоль
    6. Данные начнут собираться автоматически!
    
    💡 Совет: Используйте Opera для лучшей совместимости
    """)
    
elif choice == '2':
    print("""
    \n📝 Пример API запроса:
    
    PowerShell:
    curl -X POST http://localhost:5000/api/spins -H "Content-Type: application/json" -d '{"number": 23, "color": "red", "casino_name": "pragmatic"}'
    
    Python:
    import requests
    requests.post('http://localhost:5000/api/spins', 
        json={"number": 23, "color": "red", "casino_name": "pragmatic"})
    """)
    
elif choice == '3':
    print("\n🚀 Запускаю генератор тестовых данных...")
    print("\nВыполните команду:")
    print("   py src/main.py")
    print("\nЗатем выберите:")
    print("   1. Управление данными")
    print("   2. Генерация тестовых данных")

wait_for_user()

# ШАГ 7: Анализ данных
print_step(7, "АНАЛИЗ СОБРАННЫХ ДАННЫХ")

print("""
📊 ПРОСМОТР И АНАЛИЗ ДАННЫХ

1️⃣  Через Web Dashboard:
   http://localhost:8080/dashboard.html
   
   Здесь вы увидите:
   • Статистику по цветам
   • График последних спинов
   • Анализ серий
   • Горячие и холодные числа

2️⃣  Через API:
   GET http://localhost:5000/api/statistics
   GET http://localhost:5000/api/spins?limit=100

3️⃣  Через Python CLI:
   py src/main.py
   
   Выберите:
   • "1. Управление данными" → "3. Просмотр статистики"
   • "2. Анализ стратегий" → Тестирование различных стратегий
   • "3. AI Ассистент" → Умный анализ паттернов
""")

choice = input("\nОткрыть главный Dashboard? (Y/n): ").upper()

if choice != 'N':
    print("\n🌐 Открываю Dashboard...")
    os.system('start http://localhost:8080/dashboard.html')
    time.sleep(2)

wait_for_user()

# ШАГ 8: Тестирование стратегий
print_step(8, "ТЕСТИРОВАНИЕ СТРАТЕГИЙ")

print("""
🎯 ПРОВЕРКА ИГРОВЫХ СТРАТЕГИЙ

Встроенные стратегии:
   • Мартингейл (удвоение ставки)
   • Фибоначчи (последовательность чисел)
   • Д'Аламбер (постепенное увеличение)
   • Flat Bet (фиксированная ставка)
   • Pattern Following (следование за паттернами)

Как тестировать:
   1. Запустите: py src/main.py
   2. Выберите: "2. Анализ стратегий"
   3. Выберите стратегию для тестирования
   4. Получите результаты бэктестинга

💡 Стратегии тестируются на реальных данных!
""")

choice = input("\nЗапустить интерактивный анализатор? (Y/n): ").upper()

if choice != 'N':
    print("\n🚀 Запускаю main.py...")
    os.system('py src/main.py')

wait_for_user()

# ШАГ 9: Мониторинг в реальном времени
print_step(9, "МОНИТОРИНГ В РЕАЛЬНОМ ВРЕМЕНИ")

print("""
📡 REAL-TIME МОНИТОРИНГ

Все компоненты работают вместе:

1️⃣  Browser Collector → собирает спины
2️⃣  API Server → обрабатывает данные
3️⃣  Logger → записывает все события
4️⃣  Error Tracker → отслеживает ошибки
5️⃣  Dashboard → показывает всё в реальном времени

🔥 ГОРЯЧИЕ ССЫЛКИ:

📊 Главный Dashboard:
   http://localhost:8080/dashboard.html

📈 Мониторинг логов:
   http://localhost:8080/logs_dashboard.html

🔍 API Health:
   http://localhost:5000/api/health

📉 Статистика:
   http://localhost:5000/api/statistics

💬 Чат (team collaboration):
   Встроен в главный Dashboard
""")

print("\n🌐 Открываю все ключевые страницы...")
time.sleep(1)

pages = [
    'http://localhost:8080/dashboard.html',
    'http://localhost:8080/logs_dashboard.html',
]

for page in pages:
    os.system(f'start {page}')
    time.sleep(1)

wait_for_user()

# ШАГ 10: Итоги и рекомендации
print_step(10, "ИТОГИ И СЛЕДУЮЩИЕ ШАГИ")

print("""
🎉 ПОЗДРАВЛЯЕМ! ВЫ ОСВОИЛИ СИСТЕМУ RULETTT!

✅ ЧТО ВЫ ТЕПЕРЬ УМЕЕТЕ:

   1. Запускать все сервисы системы
   2. Мониторить логи и ошибки в реальном времени
   3. Собирать данные с реальной рулетки
   4. Анализировать статистику
   5. Тестировать игровые стратегии
   6. Использовать API для автоматизации

📚 ПОЛЕЗНЫЕ ФАЙЛЫ:

   📖 QUICKSTART.md - Быстрый старт
   📖 LOGGING_GUIDE.md - Руководство по логированию
   📖 TEST_REPORT.md - Отчёт о тестировании
   📖 README.md - Общая документация

🛠️ ПОЛЕЗНЫЕ КОМАНДЫ:

   # Запустить всё
   START_RULETTT.bat

   # Тесты
   py RUN_ALL_TESTS.py      # Все тесты
   py SMOKE_TEST.py          # Быстрая проверка
   py test_logging.py        # Тест логирования

   # Работа с системой
   py src/main.py            # Интерактивное меню
   py api_server.py          # API сервер
   py -m http.server 8080    # Веб-сервер

💡 СЛЕДУЮЩИЕ ШАГИ:

   1. Соберите первые реальные данные с казино
   2. Протестируйте разные стратегии
   3. Настройте систему алертов (Task 6)
   4. Интегрируйте с Telegram ботом
   5. Добавьте свои стратегии в user_strategies.py

🔗 LINKS:

   Dashboard:  http://localhost:8080/dashboard.html
   Logs:       http://localhost:8080/logs_dashboard.html
   API:        http://localhost:5000/api/health
   Docs:       https://github.com/nikolaspablo92-prog/RULETTT

⭐ ВАЖНО:

   • Система работает 24/7 в фоновом режиме
   • Все данные сохраняются автоматически
   • Логи ротируются (10MB файлы)
   • Ошибки группируются и отслеживаются
   • Dashboard обновляется каждые 10 секунд

❤️ СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ RULETTT!

Удачи в анализе рулетки! 🎰
""")

print("\n" + "=" * 80)
print("  🎲 СИСТЕМА ГОТОВА К ИСПОЛЬЗОВАНИЮ! 🎲")
print("=" * 80 + "\n")

input("Нажмите ENTER для завершения...")
