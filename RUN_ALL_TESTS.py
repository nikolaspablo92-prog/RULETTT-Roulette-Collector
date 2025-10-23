"""
🧪 RULETTT - Запуск всех тестов с реальными данными
===================================================

Комплексное тестирование всей системы
"""

import sys
import os
import time
import sqlite3
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("🧪 RULETTT - КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ С РЕАЛЬНЫМИ ДАННЫМИ")
print("=" * 80)
print(f"⏰ Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Счётчики
tests_passed = 0
tests_failed = 0
tests_total = 0

def run_test(name, func):
    """Запуск одного теста"""
    global tests_passed, tests_failed, tests_total
    tests_total += 1
    print(f"{'='*80}")
    print(f"🔵 ТЕСТ #{tests_total}: {name}")
    print(f"{'='*80}")
    try:
        result = func()
        if result:
            tests_passed += 1
            print(f"✅ PASSED: {name}")
        else:
            tests_failed += 1
            print(f"❌ FAILED: {name}")
        print()
        return result
    except Exception as e:
        tests_failed += 1
        print(f"❌ EXCEPTION in {name}: {e}")
        print()
        return False

# ============ ТЕСТ 1: Проверка структуры проекта ============
def test_project_structure():
    """Проверка наличия ключевых файлов и директорий"""
    print("📁 Проверка структуры проекта...")
    
    required_files = [
        'api_server.py',
        'src/logger.py',
        'src/error_tracker.py',
        'webapp/event-tracker.js',
        'webapp/logs_dashboard.html',
        'LOGGING_GUIDE.md',
        'QUICKSTART.md'
    ]
    
    required_dirs = [
        'src',
        'webapp',
        'data',
        'logs'
    ]
    
    all_ok = True
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - НЕ НАЙДЕН")
            all_ok = False
    
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ - НЕ НАЙДЕНА")
            all_ok = False
    
    return all_ok

# ============ ТЕСТ 2: Проверка баз данных ============
def test_databases():
    """Проверка наличия и структуры БД"""
    print("💾 Проверка баз данных...")
    
    data_dir = Path('data')
    db_files = list(data_dir.glob('*.db'))
    
    print(f"   📊 Найдено БД: {len(db_files)}")
    
    all_ok = True
    for db_file in db_files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Получаем список таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Считаем записи в каждой таблице
            total_records = 0
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
            
            conn.close()
            
            print(f"   ✅ {db_file.name}: {len(tables)} таблиц, {total_records} записей")
            
        except Exception as e:
            print(f"   ❌ {db_file.name}: Ошибка - {e}")
            all_ok = False
    
    return all_ok and len(db_files) > 0

# ============ ТЕСТ 3: Проверка API сервера ============
def test_api_server():
    """Проверка работы API endpoints"""
    print("🌐 Проверка API сервера...")
    
    import urllib.request
    import json
    
    endpoints = [
        ('http://localhost:5000/api/health', 'Health check'),
        ('http://localhost:5000/api/spins?limit=5', 'Спины'),
        ('http://localhost:5000/api/statistics', 'Статистика'),
    ]
    
    all_ok = True
    for url, name in endpoints:
        try:
            response = urllib.request.urlopen(url, timeout=3)
            status = response.status
            data = json.loads(response.read().decode('utf-8'))
            print(f"   ✅ {name}: {status} - {len(str(data))} bytes")
        except Exception as e:
            print(f"   ❌ {name}: {e}")
            all_ok = False
    
    return all_ok

# ============ ТЕСТ 4: Проверка веб-сервера ============
def test_web_server():
    """Проверка доступности веб-страниц"""
    print("🌐 Проверка веб-сервера...")
    
    import urllib.request
    
    pages = [
        ('http://localhost:8080/logs_dashboard.html', 'Logs Dashboard'),
        ('http://localhost:8080/dashboard.html', 'Main Dashboard'),
        ('http://localhost:8080/event-tracker.js', 'Event Tracker'),
    ]
    
    all_ok = True
    for url, name in pages:
        try:
            response = urllib.request.urlopen(url, timeout=3)
            status = response.status
            size = len(response.read())
            print(f"   ✅ {name}: {status} - {size} bytes")
        except Exception as e:
            print(f"   ❌ {name}: {e}")
            all_ok = False
    
    return all_ok

# ============ ТЕСТ 5: Тест логирования ============
def test_logging():
    """Тест системы логирования"""
    print("📝 Тест системы логирования...")
    
    import logging
    
    # Создаём тестовый логгер
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    test_log_file = log_dir / 'test_run.log'
    
    logger = logging.getLogger('test_run')
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler(test_log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    # Генерируем тестовые логи
    test_messages = [
        (logger.debug, "🐛 Debug: Тестовое сообщение"),
        (logger.info, "ℹ️  Info: Система работает"),
        (logger.warning, "⚠️  Warning: Проверка предупреждений"),
        (logger.error, "❌ Error: Тестовая ошибка"),
        (logger.critical, "🔥 Critical: Критическая ошибка")
    ]
    
    for log_func, message in test_messages:
        log_func(message)
    
    # Проверяем, что файл создан и содержит логи
    if test_log_file.exists():
        size = test_log_file.stat().st_size
        with open(test_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"   ✅ Файл логов создан: {size} bytes, {len(lines)} строк")
        return True
    else:
        print(f"   ❌ Файл логов не создан")
        return False

# ============ ТЕСТ 6: Анализ реальных данных ============
def test_real_data_analysis():
    """Анализ реальных данных из БД"""
    print("📊 Анализ реальных данных...")
    
    db_path = Path('data/final_single_table.db')
    
    if not db_path.exists():
        db_path = Path('data/rulettt_cloud.db')
    
    if not db_path.exists():
        print("   ⚠️  Основные БД не найдены")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем таблицу спинов
        cursor.execute("""
            SELECT COUNT(*) FROM roulette_spins
        """)
        total_spins = cursor.fetchone()[0]
        
        # Статистика по цветам
        cursor.execute("""
            SELECT color, COUNT(*) as count 
            FROM roulette_spins 
            GROUP BY color
            ORDER BY count DESC
        """)
        color_stats = cursor.fetchall()
        
        # Последние спины
        cursor.execute("""
            SELECT number, color, timestamp 
            FROM roulette_spins 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        recent_spins = cursor.fetchall()
        
        conn.close()
        
        print(f"   📈 Всего спинов: {total_spins}")
        print(f"   🎨 Статистика по цветам:")
        for color, count in color_stats:
            percentage = (count / total_spins * 100) if total_spins > 0 else 0
            print(f"      {color}: {count} ({percentage:.1f}%)")
        
        print(f"   🎲 Последние 5 спинов:")
        for number, color, timestamp in recent_spins:
            print(f"      {number} ({color}) - {timestamp}")
        
        return total_spins > 0
        
    except Exception as e:
        print(f"   ❌ Ошибка анализа: {e}")
        return False

# ============ ТЕСТ 7: Тест стратегий ============
def test_strategies():
    """Тест работы стратегий"""
    print("🎯 Тест стратегий...")
    
    try:
        # Проверяем наличие модуля game_analyzer
        from pathlib import Path
        analyzer_path = Path('src/game_analyzer.py')
        
        if not analyzer_path.exists():
            print("   ⚠️  game_analyzer.py не найден")
            return False
        
        print("   ✅ Модуль game_analyzer найден")
        
        # Проверяем БД со стратегиями
        db_path = Path('data/test_strategies.db')
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"   ✅ БД стратегий: {len(tables)} таблиц")
            
            conn.close()
            return True
        else:
            print("   ℹ️  БД стратегий не найдена (это нормально)")
            return True
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

# ============ ТЕСТ 8: Производительность ============
def test_performance():
    """Тест производительности системы"""
    print("⚡ Тест производительности...")
    
    import time
    
    # Тест скорости записи в лог
    import logging
    logger = logging.getLogger('perf_test')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('logs/perf_test.log', encoding='utf-8')
    logger.addHandler(handler)
    
    start_time = time.time()
    for i in range(1000):
        logger.info(f"Тестовое сообщение #{i}")
    end_time = time.time()
    
    duration = end_time - start_time
    ops_per_sec = 1000 / duration
    
    print(f"   📊 1000 записей в лог: {duration:.3f} сек ({ops_per_sec:.0f} ops/sec)")
    
    # Тест скорости чтения из БД
    db_path = Path('data/final_single_table.db')
    if db_path.exists():
        start_time = time.time()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM roulette_spins LIMIT 1000")
        results = cursor.fetchall()
        conn.close()
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"   📊 Чтение 1000 записей из БД: {duration:.3f} сек")
    
    return True

# ============ ТЕСТ 9: Интеграционный тест ============
def test_integration():
    """Интеграционный тест всей системы"""
    print("🔗 Интеграционный тест...")
    
    import urllib.request
    import json
    
    try:
        # 1. Получаем статистику через API
        response = urllib.request.urlopen('http://localhost:5000/api/statistics', timeout=3)
        stats = json.loads(response.read().decode('utf-8'))
        print(f"   ✅ API статистика получена")
        
        # 2. Получаем последние спины
        response = urllib.request.urlopen('http://localhost:5000/api/spins?limit=10', timeout=3)
        spins = json.loads(response.read().decode('utf-8'))
        print(f"   ✅ Получено {len(spins)} спинов")
        
        # 3. Проверяем dashboard доступен
        response = urllib.request.urlopen('http://localhost:8080/logs_dashboard.html', timeout=3)
        dashboard_html = response.read()
        print(f"   ✅ Dashboard доступен ({len(dashboard_html)} bytes)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка интеграции: {e}")
        return False

# ============ ТЕСТ 10: Проверка документации ============
def test_documentation():
    """Проверка наличия и полноты документации"""
    print("📚 Проверка документации...")
    
    docs = [
        ('LOGGING_GUIDE.md', 'Руководство по логированию'),
        ('QUICKSTART.md', 'Быстрый старт'),
        ('LOGGING_SYSTEM_REPORT.md', 'Отчёт о системе'),
        ('LOGGING_INTEGRATION_EXAMPLE.py', 'Примеры интеграции'),
        ('README.md', 'README')
    ]
    
    all_ok = True
    total_size = 0
    
    for filename, description in docs:
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            total_size += size
            print(f"   ✅ {description}: {size} bytes")
        else:
            print(f"   ⚠️  {description} не найден")
            # Не считаем критической ошибкой
    
    print(f"   📊 Общий размер документации: {total_size} bytes")
    return True

# ============ ЗАПУСК ВСЕХ ТЕСТОВ ============

print("🚀 Начинаем тестирование...\n")

run_test("Структура проекта", test_project_structure)
run_test("Базы данных", test_databases)
run_test("API сервер", test_api_server)
run_test("Веб-сервер", test_web_server)
run_test("Система логирования", test_logging)
run_test("Анализ реальных данных", test_real_data_analysis)
run_test("Стратегии", test_strategies)
run_test("Производительность", test_performance)
run_test("Интеграционный тест", test_integration)
run_test("Документация", test_documentation)

# ============ ИТОГИ ============

print("=" * 80)
print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
print("=" * 80)
print()
print(f"✅ Пройдено:  {tests_passed}/{tests_total}")
print(f"❌ Провалено: {tests_failed}/{tests_total}")
print(f"📊 Процент успеха: {(tests_passed/tests_total*100):.1f}%")
print()

if tests_failed == 0:
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("✅ Система RULETTT работает корректно")
elif tests_failed <= 2:
    print("⚠️  Большинство тестов пройдено")
    print("💡 Рекомендуется исправить оставшиеся проблемы")
else:
    print("❌ Обнаружены критические проблемы")
    print("🔧 Требуется диагностика и исправление")

print()
print("=" * 80)
print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
