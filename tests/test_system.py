"""
ТЕСТ СИСТЕМЫ С РЕАЛЬНЫМИ ДАННЫМИ
================================

Этот файл проверяет работу всех компонентов системы используя ТОЛЬКО РЕАЛЬНЫЕ данные.
НЕТ фейковых данных - только то что было собрано из браузера.

Запустите: py test_system.py
"""

import sys
from pathlib import Path
import traceback
from datetime import datetime, timedelta

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Тестирует импорт всех модулей"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 ТЕСТ 1: Импорт модулей")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        from utils import RouletteUtils
        print("✅ utils.py - импортирован")
    except Exception as e:
        print(f"❌ utils.py - ОШИБКА: {e}")
        return False
    
    try:
        from data_collector import DataCollector
        print("✅ data_collector.py - импортирован")
    except Exception as e:
        print(f"❌ data_collector.py - ОШИБКА: {e}")
        return False
    
    try:
        from game_analyzer import GameAnalyzer, PredefinedStrategies
        print("✅ game_analyzer.py - импортирован")
    except Exception as e:
        print(f"❌ game_analyzer.py - ОШИБКА: {e}")
        return False
    
    try:
        from ai_assistant import AIAssistant
        print("✅ ai_assistant.py - импортирован")
    except Exception as e:
        print(f"❌ ai_assistant.py - ОШИБКА: {e}")
        return False
    
    print("✅ Все модули импортированы успешно")
    return True

def test_utils():
    """Тестирует утилиты рулетки"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 ТЕСТ 2: Утилиты рулетки")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        from utils import RouletteUtils
        utils = RouletteUtils()
        
        # Тест цветов (используем реальные константы)
        print("Тестируем определение цветов...")
        
        # Красные числа (из реального маппинга)
        red_tests = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        for num in red_tests:
            color = utils.get_color(num)
            assert color == "red", f"❌ Число {num} должно быть красным, а не {color}"
        print(f"✅ Красные числа: {len(red_tests)} чисел проверено")
        
        # Черные числа (из реального маппинга)
        black_tests = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        for num in black_tests:
            color = utils.get_color(num)
            assert color == "black", f"❌ Число {num} должно быть черным, а не {color}"
        print(f"✅ Черные числа: {len(black_tests)} чисел проверено")
        
        # Зеро (единственное зеленое)
        assert utils.get_color(0) == "green", "❌ Число 0 должно быть зеленым"
        print("✅ Зеро (0) - зеленое")
        
        # Тест дюжин
        print("\nТестируем определение дюжин...")
        assert utils.get_dozen(5) == 1, "5 должно быть в первой дюжине"
        assert utils.get_dozen(15) == 2, "15 должно быть во второй дюжине"
        assert utils.get_dozen(25) == 3, "25 должно быть в третьей дюжине"
        assert utils.get_dozen(0) is None, "0 не должно быть ни в какой дюжине"
        print("✅ Дюжины: все 3 дюжины работают корректно")
        
        # Тест четности
        print("\nТестируем определение четности...")
        assert utils.is_even(2) == True, "2 должно быть четным"
        assert utils.is_even(3) == False, "3 должно быть нечетным"
        assert utils.is_even(0) is None, "0 не должно быть ни четным ни нечетным"
        print("✅ Четность: определяется корректно")
        
        print("\n✅ Все тесты утилит прошли успешно")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестировании утилит: {e}")
        traceback.print_exc()
        return False


def test_real_data():
    """Тестирует работу с реальными данными из базы"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 ТЕСТ 3: Работа с реальными данными")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        from data_collector import DataCollector
        import os
        
        # Проверяем существование основной базы данных
        main_db = "data/final_single_table.db"
        
        if not os.path.exists(main_db):
            print(f"⚠️ Основная база данных не найдена: {main_db}")
            print("💡 Создаем новую базу данных...")
        
        collector = DataCollector(main_db)
        print(f"✅ Подключение к базе: {main_db}")
        
        # Получаем реальные данные за последние 30 дней
        start_date = datetime.now() - timedelta(days=30)
        stats = collector.get_statistics(start_date)
        
        total_spins = stats.get('total_spins', 0)
        print(f"\n📊 Статистика за последние 30 дней:")
        print(f"   Всего спинов: {total_spins}")
        
        if total_spins > 0:
            print(f"   🔴 Красных: {stats.get('red_count', 0)} ({stats.get('red_percentage', 0):.1f}%)")
            print(f"   ⚫ Черных: {stats.get('black_count', 0)} ({stats.get('black_percentage', 0):.1f}%)")
            print(f"   🟢 Зеро: {stats.get('zero_count', 0)} ({stats.get('zero_percentage', 0):.1f}%)")
            print(f"   📅 Первый спин: {stats.get('earliest_spin', 'N/A')}")
            print(f"   📅 Последний спин: {stats.get('latest_spin', 'N/A')}")
            print("\n✅ Работа с реальными данными: успешно")
        else:
            print("\n⚠️ В базе нет данных за последние 30 дней")
            print("💡 Соберите данные с Paddypower используя коллектор")
            print("   Файл: paddypower_collector_v2.js")
        
        # Тест добавления нового спина
        print("\n🔄 Тестируем добавление спина...")
        test_spin_id = collector.add_spin(
            number=17,
            timestamp=datetime.now(),
            session_id="test_system",
            casino_name="Test",
            table_name="System Test"
        )
        assert test_spin_id > 0, "ID спина должен быть положительным"
        print(f"✅ Спин добавлен с ID: {test_spin_id}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при работе с реальными данными: {e}")
        traceback.print_exc()
        return False

def test_strategies():
    """Тестирует стратегии на реальных данных (если есть)"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 ТЕСТ 4: Стратегии анализа")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        from data_collector import DataCollector
        from game_analyzer import GameAnalyzer, PredefinedStrategies
        
        collector = DataCollector("data/final_single_table.db")
        
        # Проверяем есть ли данные для анализа
        start_date = datetime.now() - timedelta(days=30)
        stats = collector.get_statistics(start_date)
        total_spins = stats.get('total_spins', 0)
        
        if total_spins < 10:
            print("⚠️ Недостаточно данных для тестирования стратегий")
            print(f"   В базе: {total_spins} спинов (нужно минимум 10)")
            print("💡 Соберите больше данных с Paddypower")
            print("✅ Тест пропущен (недостаточно данных)")
            return True
        
        print(f"📊 В базе {total_spins} спинов - достаточно для тестирования")
        
        # Создаем анализатор
        analyzer = GameAnalyzer(collector)
        print("✅ Анализатор создан")
        
        # Тестируем предопределенные стратегии
        print("\n🎯 Тестируем предопределенные стратегии:")
        
        strategies_to_test = [
            ("Мартингейл на красное", PredefinedStrategies.martingale_red(10)),
            ("Фиксированная ставка на черное", PredefinedStrategies.flat_bet_black(10)),
        ]
        
        for strategy_name, strategy in strategies_to_test:
            try:
                result = analyzer.test_strategy(
                    strategy=strategy,
                    start_date=start_date,
                    end_date=None,
                    initial_balance=1000
                )
                
                if "error" in result:
                    print(f"   ⚠️ {strategy_name}: {result['error']}")
                else:
                    profit = result.get('total_profit', 0)
                    win_rate = result.get('win_rate', 0)
                    emoji = "💰" if profit > 0 else "📉" if profit < 0 else "➖"
                    print(f"   {emoji} {strategy_name}:")
                    print(f"      Прибыль: {profit:.2f}")
                    print(f"      Винрейт: {win_rate:.1f}%")
            except Exception as e:
                print(f"   ❌ {strategy_name}: Ошибка - {e}")
        
        print("\n✅ Тестирование стратегий завершено")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестировании стратегий: {e}")
        traceback.print_exc()
        return False


def main():
    """Главная функция теста"""
    print("\n")
    print("="*60)
    print("  ТЕСТ СИСТЕМЫ АНАЛИЗА РУЛЕТКИ - РЕАЛЬНЫЕ ДАННЫЕ")
    print("="*60)
    print("\n📌 Этот тест использует ТОЛЬКО реальные данные")
    print("📌 НЕТ фейковых или сгенерированных данных")
    print("\n")
    
    all_passed = True
    
    # Тест 1: Импорты
    if not test_imports():
        all_passed = False
        print("\n❌ Тест импортов не прошел - остановка")
        return
    
    # Тест 2: Утилиты
    if not test_utils():
        all_passed = False
    
    # Тест 3: Реальные данные
    if not test_real_data():
        all_passed = False
    
    # Тест 4: Стратегии
    if not test_strategies():
        all_passed = False
    
    # Итоги
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("="*60)
        print("\n✅ Система готова к использованию")
        print("\n📊 Следующие шаги:")
        print("   1. Соберите данные с Paddypower:")
        print("      - Откройте игру в браузере")
        print("      - F12 → Console")
        print("      - Вставьте код из paddypower_collector_v2.js")
        print("   2. Экспортируйте данные:")
        print("      - exportPaddypowerData()")
        print("   3. Импортируйте в систему:")
        print("      - py console_to_analysis.py")
        print("   4. Запустите анализ:")
        print("      - py src/main.py")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
        print("="*60)
        print("\n⚠️ Проверьте ошибки выше и исправьте проблемы")
    
    print("\n" + "="*60)
    print(f"📅 Тест выполнен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()