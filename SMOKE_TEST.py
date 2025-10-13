"""
🧪 RULETTT - Тест существующей системы (smoke test)
===================================================

Быстрая проверка работоспособности основных компонентов
"""

import sys
import os
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("=" * 80)
print("🧪 RULETTT - SMOKE TEST (Быстрая проверка)")
print("=" * 80)
print()

passed = 0
failed = 0

# Тест 1: Импорты
print("1️⃣ Тест импортов...")
try:
    from utils import RouletteUtils
    print("   ✅ utils.RouletteUtils")
    passed += 1
except Exception as e:
    print(f"   ❌ utils: {e}")
    failed += 1

try:
    from data_collector import DataCollector
    print("   ✅ data_collector.DataCollector")
    passed += 1
except Exception as e:
    print(f"   ❌ data_collector: {e}")
    failed += 1

try:
    import game_analyzer
    print("   ✅ game_analyzer")
    passed += 1
except Exception as e:
    print(f"   ❌ game_analyzer: {e}")
    failed += 1

print()

# Тест 2: Утилиты рулетки
print("2️⃣ Тест утилит рулетки...")
try:
    from utils import RouletteUtils
    
    # Тест определения цвета
    assert RouletteUtils.get_color(0) == "green", "0 должен быть зелёным"
    assert RouletteUtils.get_color(1) == "red", "1 должен быть красным"
    assert RouletteUtils.get_color(2) == "black", "2 должен быть чёрным"
    print("   ✅ Определение цвета работает")
    passed += 1
    
    # Тест дюжин
    assert RouletteUtils.get_dozen(5) == 1, "5 в первой дюжине"
    assert RouletteUtils.get_dozen(15) == 2, "15 во второй дюжине"
    assert RouletteUtils.get_dozen(30) == 3, "30 в третьей дюжине"
    print("   ✅ Определение дюжин работает")
    passed += 1
    
except Exception as e:
    print(f"   ❌ Ошибка утилит: {e}")
    failed += 2

print()

# Тест 3: База данных
print("3️⃣ Тест базы данных...")
try:
    import sqlite3
    from pathlib import Path
    
    db_path = Path('data/rulettt_cloud.db')
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"   ✅ БД найдена: {len(tables)} таблиц")
        passed += 1
        
        # Пробуем прочитать данные
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} записей")
            except:
                pass
        
        conn.close()
        passed += 1
    else:
        print("   ⚠️  БД не найдена")
        failed += 2
        
except Exception as e:
    print(f"   ❌ Ошибка БД: {e}")
    failed += 2

print()

# Тест 4: API
print("4️⃣ Тест API...")
try:
    import urllib.request
    import json
    
    response = urllib.request.urlopen('http://localhost:5000/api/health', timeout=2)
    data = json.loads(response.read().decode('utf-8'))
    
    if data.get('status') == 'healthy':
        print(f"   ✅ API работает: {data.get('service')}")
        passed += 1
    else:
        print(f"   ⚠️  API вернул неожиданный статус")
        failed += 1
        
except Exception as e:
    print(f"   ❌ API недоступен: {e}")
    failed += 1

print()

# Тест 5: Логирование
print("5️⃣ Тест логирования...")
try:
    import logging
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger('smoke_test')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('logs/smoke_test.log', encoding='utf-8')
    logger.addHandler(handler)
    
    logger.info("✅ Smoke test logging works")
    
    if (log_dir / 'smoke_test.log').exists():
        print("   ✅ Логирование работает")
        passed += 1
    else:
        print("   ❌ Файл лога не создан")
        failed += 1
        
except Exception as e:
    print(f"   ❌ Ошибка логирования: {e}")
    failed += 1

print()

# Итоги
print("=" * 80)
print("📊 ИТОГИ SMOKE TEST")
print("=" * 80)
total = passed + failed
success_rate = (passed / total * 100) if total > 0 else 0

print(f"✅ Пройдено: {passed}/{total}")
print(f"❌ Провалено: {failed}/{total}")
print(f"📈 Успешность: {success_rate:.1f}%")
print()

if failed == 0:
    print("🎉 ВСЕ БАЗОВЫЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
    print("✅ Система готова к работе")
elif success_rate >= 70:
    print("⚠️  Система в основном работоспособна")
    print("💡 Некоторые компоненты требуют внимания")
else:
    print("❌ Обнаружены серьёзные проблемы")
    print("🔧 Требуется диагностика")

print("=" * 80)
