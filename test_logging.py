"""
🧪 RULETTT - Простой тест системы логирования
==============================================

Минималистичный тест без внешних зависимостей
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Импорты напрямую из файлов
import logging
from pathlib import Path

print("=" * 60)
print("🧪 RULETTT - Тест системы логирования")
print("=" * 60)
print()

# Тест 1: Создание директории логов
print("1️⃣ Проверка директории логов...")
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
print(f"   ✅ Директория создана: {log_dir.absolute()}")
print()

# Тест 2: Создание БД ошибок
print("2️⃣ Проверка БД ошибок...")
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
db_path = data_dir / 'errors.db'
if db_path.exists():
    print(f"   ✅ БД существует: {db_path}")
else:
    print(f"   ⚠️  БД будет создана при первой ошибке")
print()

# Тест 3: Базовое логирование
print("3️⃣ Тест базового логирования...")
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)

# Файловый хендлер
file_handler = logging.FileHandler('logs/test.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Консольный хендлер
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('   %(levelname)s: %(message)s'))
logger.addHandler(console_handler)

logger.debug("🐛 Debug сообщение")
logger.info("ℹ️  Info сообщение")
logger.warning("⚠️  Warning сообщение")
logger.error("❌ Error сообщение")
logger.critical("🔥 Critical сообщение")
print()

# Тест 4: Отправка события на API
print("4️⃣ Тест отправки события на API...")
try:
    import urllib.request
    import json
    
    event_data = {
        'type': 'test_event',
        'level': 'info',
        'details': {
            'test': True,
            'message': 'Тестовое событие от test_logging.py'
        }
    }
    
    req = urllib.request.Request(
        'http://localhost:5000/api/events',
        data=json.dumps([event_data]).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode('utf-8'))
    print(f"   ✅ Событие отправлено: {result}")
except Exception as e:
    print(f"   ⚠️  Не удалось отправить событие: {e}")
    print(f"   💡 Убедитесь, что API сервер запущен на порту 5000")
print()

# Тест 5: Проверка API endpoints
print("5️⃣ Проверка API endpoints...")
endpoints = [
    ('http://localhost:5000/api/health', 'Health check'),
    ('http://localhost:5000/api/logs/stats', 'Статистика логов'),
    ('http://localhost:8080/logs_dashboard.html', 'Dashboard')
]

for url, name in endpoints:
    try:
        response = urllib.request.urlopen(url, timeout=3)
        status = response.status
        print(f"   ✅ {name}: {status}")
    except Exception as e:
        print(f"   ❌ {name}: {e}")
print()

# Тест 6: Генерация тестовых логов
print("6️⃣ Генерация тестовых логов...")
for i in range(10):
    if i % 3 == 0:
        logger.info(f"✅ Операция {i+1} выполнена успешно")
    elif i % 3 == 1:
        logger.warning(f"⚠️  Предупреждение для операции {i+1}")
    else:
        logger.error(f"❌ Ошибка в операции {i+1}")
print(f"   ✅ Сгенерировано 10 тестовых логов")
print()

# Тест 7: Проверка файлов логов
print("7️⃣ Проверка файлов логов...")
log_files = list(log_dir.glob('*.log'))
if log_files:
    print(f"   ✅ Найдено {len(log_files)} файлов логов:")
    for log_file in log_files[:5]:  # Показываем первые 5
        size = log_file.stat().st_size
        print(f"      - {log_file.name} ({size} bytes)")
else:
    print(f"   ⚠️  Файлы логов не найдены")
print()

# Итоги
print("=" * 60)
print("✅ ТЕСТ ЗАВЕРШЁН")
print("=" * 60)
print()
print("📊 Результаты:")
print(f"   • Директория логов: {log_dir.absolute()}")
print(f"   • Файлов логов: {len(log_files)}")
print(f"   • Директория БД: {data_dir.absolute()}")
print()
print("🌐 Открыть в браузере:")
print(f"   • Dashboard: http://localhost:8080/logs_dashboard.html")
print(f"   • API Health: http://localhost:5000/api/health")
print(f"   • Статистика: http://localhost:5000/api/logs/stats")
print()
print("💡 Следующие шаги:")
print("   1. Откройте Dashboard в браузере")
print("   2. Перейдите на вкладку 'Логи'")
print("   3. Посмотрите сгенерированные тестовые логи")
print()
