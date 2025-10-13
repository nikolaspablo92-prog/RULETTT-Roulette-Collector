"""
ТЕСТИРОВЩИК ПОДКЛЮЧЕНИЯ К КАЗИНО
===============================

Проверяет работоспособность настроенного подключения к казино.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Добавляем путь к src
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src"))

try:
    from src.live_data_collector import LiveDataCollector
    from src.utils import RouletteUtils
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

class ConnectionTester:
    """Класс для тестирования подключения"""
    
    def __init__(self):
        self.collector = LiveDataCollector()
        self.utils = RouletteUtils()
    
    def run_tests(self):
        """Запуск всех тестов"""
        print("🔍 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К КАЗИНО")
        print("=" * 40)
        
        self.test_config()
        self.test_connection()
        self.test_data_quality()
        self.show_recommendations()
    
    def test_config(self):
        """Тест конфигурации"""
        print("\n📋 ПРОВЕРКА КОНФИГУРАЦИИ")
        print("-" * 30)
        
        config = self.collector.config
        
        print(f"Казино: {config.get('casino_name', 'Не указано')}")
        print(f"Метод подключения: {config.get('connection_method', 'Не указан')}")
        
        if 'betting' in config:
            betting = config['betting']
            print(f"Базовая ставка: {betting.get('base_bet', 'Не указана')}")
            print(f"Банкролл: {betting.get('bankroll', 'Не указан')}")
        
        method = config.get('connection_method', 'mock')
        
        if method == 'api':
            api_config = config.get('api', {})
            if api_config.get('base_url') and api_config.get('api_key'):
                print("✅ API конфигурация настроена")
            else:
                print("⚠️ API конфигурация неполная")
        
        elif method == 'scraping':
            scraping_config = config.get('scraping', {})
            if scraping_config.get('base_url') and scraping_config.get('selectors'):
                print("✅ Конфигурация скрапинга настроена")
            else:
                print("⚠️ Конфигурация скрапинга неполная")
        
        elif method == 'mock':
            print("✅ Используются тестовые данные")
        
        else:
            print(f"⚠️ Неизвестный метод: {method}")
    
    def test_connection(self):
        """Тест подключения"""
        print("\n🔗 ПРОВЕРКА ПОДКЛЮЧЕНИЯ")
        print("-" * 25)
        
        method = self.collector.config.get('connection_method', 'mock')
        
        try:
            # Получаем тестовые данные
            results = self.collector.get_live_results(method, limit=5)
            
            if results:
                print(f"✅ Подключение работает ({len(results)} результатов)")
                
                # Показываем первые результаты
                print("\nПоследние результаты:")
                for i, result in enumerate(results[:3], 1):
                    number = result.get('number', '?')
                    color = result.get('color', '?')
                    timestamp = result.get('timestamp', datetime.now())
                    if isinstance(timestamp, datetime):
                        time_str = timestamp.strftime('%H:%M:%S')
                    else:
                        time_str = str(timestamp)
                    
                    print(f"  {i}. {time_str}: {number} ({color})")
            
            else:
                print("⚠️ Подключение установлено, но данных нет")
        
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
    
    def test_data_quality(self):
        """Тест качества данных"""
        print("\n📊 ПРОВЕРКА КАЧЕСТВА ДАННЫХ")
        print("-" * 30)
        
        try:
            # Получаем больше данных для анализа
            results = self.collector.get_live_results(
                self.collector.config.get('connection_method', 'mock'), 
                limit=50
            )
            
            if not results:
                print("❌ Нет данных для анализа")
                return
            
            # Анализируем данные
            numbers = [r.get('number') for r in results if r.get('number') is not None]
            colors = [r.get('color') for r in results if r.get('color')]
            
            if not numbers:
                print("❌ Некорректные данные (нет чисел)")
                return
            
            # Проверяем валидность чисел
            valid_numbers = [n for n in numbers if 0 <= n <= 36]
            invalid_count = len(numbers) - len(valid_numbers)
            
            if invalid_count > 0:
                print(f"⚠️ Найдено {invalid_count} некорректных чисел")
            else:
                print("✅ Все числа корректны (0-36)")
            
            # Анализ распределения цветов
            if colors:
                color_counts = {}
                for color in colors:
                    color_counts[color] = color_counts.get(color, 0) + 1
                
                print("Распределение цветов:")
                for color, count in color_counts.items():
                    percentage = count / len(colors) * 100
                    print(f"  {color}: {count} ({percentage:.1f}%)")
            
            # Проверка временных меток
            timestamps = [r.get('timestamp') for r in results if r.get('timestamp')]
            if timestamps:
                if all(isinstance(ts, datetime) for ts in timestamps):
                    print("✅ Временные метки корректны")
                else:
                    print("⚠️ Некорректные временные метки")
            
            print(f"✅ Проанализировано {len(results)} результатов")
        
        except Exception as e:
            print(f"❌ Ошибка анализа данных: {e}")
    
    def show_recommendations(self):
        """Показать рекомендации"""
        print("\n💡 РЕКОМЕНДАЦИИ")
        print("-" * 15)
        
        method = self.collector.config.get('connection_method', 'mock')
        
        if method == 'mock':
            print("📚 Вы используете тестовые данные:")
            print("  • Отлично для изучения системы")
            print("  • Безопасно для тестирования стратегий")
            print("  • Настройте реальное подключение для работы")
        
        elif method == 'api':
            print("🚀 API подключение:")
            print("  • Самый надежный способ получения данных")
            print("  • Проверьте лимиты запросов API")
            print("  • Обеспечьте стабильное интернет-соединение")
        
        elif method == 'scraping':
            print("🕷️ Веб-скрапинг:")
            print("  • Убедитесь что скрапинг разрешен")
            print("  • Добавьте задержки между запросами")
            print("  • Обработайте возможные изменения в HTML")
        
        print("\n⚠️ ВАЖНЫЕ НАПОМИНАНИЯ:")
        print("  • Начните с минимальных ставок")
        print("  • Установите лимиты потерь")
        print("  • Помните о преимуществе казино")
        print("  • Используйте систему осознанно")


def main():
    """Главная функция"""
    try:
        tester = ConnectionTester()
        tester.run_tests()
        
        print("\n" + "=" * 40)
        print("Тестирование завершено!")
        print("Запустите python src/main.py для работы с системой")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()