"""
ПРОСТОЙ ТЕСТ СИСТЕМЫ
===================

Этот файл проверяет работают ли все компоненты системы.
Запустите его чтобы убедиться что все настроено правильно.
"""

import sys
from pathlib import Path
import traceback

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Тестирует импорт всех модулей"""
    print("🔍 Тестируем импорт модулей...")
    
    try:
        from utils import RouletteUtils
        print("✅ utils.py - OK")
    except Exception as e:
        print(f"❌ utils.py - ОШИБКА: {e}")
        return False
    
    try:
        from data_collector import DataCollector
        print("✅ data_collector.py - OK")
    except Exception as e:
        print(f"❌ data_collector.py - ОШИБКА: {e}")
        return False
    
    try:
        from game_analyzer import GameAnalyzer, PredefinedStrategies
        print("✅ game_analyzer.py - OK")
    except Exception as e:
        print(f"❌ game_analyzer.py - ОШИБКА: {e}")
        return False
    
    try:
        from ai_assistant import AIAssistant
        print("✅ ai_assistant.py - OK")
    except Exception as e:
        print(f"❌ ai_assistant.py - ОШИБКА: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Тестирует базовую функциональность"""
    print("\n🔍 Тестируем базовую функциональность...")
    
    try:
        from utils import RouletteUtils
        from data_collector import DataCollector
        from datetime import datetime, timedelta
        
        # Тест утилит
        utils = RouletteUtils()
        
        # Проверяем цвета
        assert utils.get_color(17) == "black", "Число 17 должно быть черным"
        assert utils.get_color(18) == "red", "Число 18 должно быть красным" 
        assert utils.get_color(0) == "green", "Число 0 должно быть зеленым"
        print("✅ Определение цветов работает")
        
        # Проверяем четность
        assert utils.is_even(2) == True, "2 должно быть четным"
        assert utils.is_even(3) == False, "3 должно быть нечетным"
        assert utils.is_even(0) == None, "0 не должно быть ни четным ни нечетным"
        print("✅ Определение четности работает")
        
        # Тест сборщика данных
        collector = DataCollector("data/test_simple.db")
        
        # Добавляем тестовый спин
        spin_id = collector.add_spin(17, datetime.now(), "test_session")
        assert spin_id > 0, "ID спина должен быть положительным"
        print("✅ Добавление спина работает")
        
        # Проверяем статистику
        start_date = datetime.now() - timedelta(days=1)
        stats = collector.get_statistics(start_date)
        assert stats['total_spins'] >= 1, "Должен быть минимум 1 спин"
        print("✅ Получение статистики работает")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в базовой функциональности: {e}")
        traceback.print_exc()
        return False

def test_strategies():
    """Тестирует стратегии"""
    print("\n🔍 Тестируем стратегии...")
    
    try:
        from data_collector import DataCollector
        from game_analyzer import GameAnalyzer, PredefinedStrategies
        from datetime import datetime, timedelta
        
        # Создаем тестовые данные
        collector = DataCollector("data/test_strategies.db")
        start_date = datetime.now() - timedelta(days=2)
        
        # Генерируем немного данных
        collector.generate_random_spins(50, start_date)
        print("✅ Генерация тестовых данных работает")
        
        # Создаем анализатор
        analyzer = GameAnalyzer(collector)
        
        # Тестируем стратегию
        strategy = PredefinedStrategies.martingale_red(10)
        result = analyzer.test_strategy(strategy, start_date, None, 1000)
        
        assert "error" not in result, "Тестирование стратегии не должно выдавать ошибку"
        assert "total_profit" in result, "Результат должен содержать прибыль"
        print("✅ Тестирование стратегий работает")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании стратегий: {e}")
        traceback.print_exc()
        return False

def main():
    """Главная функция теста"""
    print("="*50)
    print("    ТЕСТ СИСТЕМЫ АНАЛИЗА РУЛЕТКИ")
    print("="*50)
    
    all_passed = True
    
    # Тест импортов
    if not test_imports():
        all_passed = False
    
    # Тест базовой функциональности
    if not test_basic_functionality():
        all_passed = False
    
    # Тест стратегий
    if not test_strategies():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✅ Система готова к использованию")
        print("\nЗапустите main.py для начала работы:")
        print("python src/main.py")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
        print("Проверьте ошибки выше и исправьте проблемы")
    
    print("="*50)

if __name__ == "__main__":
    main()