"""
ГЛАВНЫЙ ФАЙЛ СИСТЕМЫ АНАЛИЗА РУЛЕТКИ
===================================

Этот файл запускает всю систему и предоставляет простой интерфейс для работы.

Простыми словами:
- Запускает все компоненты системы
- Предоставляет меню для выбора действий
- Связывает все модули вместе
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем текущую папку в путь поиска модулей
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from data_collector import DataCollector
    from game_analyzer import GameAnalyzer, PredefinedStrategies
    from ai_assistant import AIAssistant
    from utils import RouletteUtils, print_roulette_info
    from user_strategies import UserStrategies, get_all_user_strategies
    from live_data_collector import LiveDataCollector
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь что все файлы находятся в папке src/")
    sys.exit(1)


class RouletteAnalysisSystem:
    """Главный класс системы анализа рулетки"""
    
    def __init__(self):
        """Инициализация системы"""
        print("=== СИСТЕМА АНАЛИЗА РУЛЕТКИ ===")
        print("Инициализация компонентов...")
        
        # Инициализируем компоненты
        self.data_collector = DataCollector("../data/roulette_history.db")
        self.game_analyzer = GameAnalyzer(self.data_collector)
        self.ai_assistant = AIAssistant(self.data_collector, self.game_analyzer)
        self.utils = RouletteUtils()
        self.live_collector = LiveDataCollector()
        
        print("Система готова к работе!")
    
    def show_menu(self):
        """Показывает главное меню"""
        print("\n" + "="*50)
        print("            ГЛАВНОЕ МЕНЮ")
        print("="*50)
        print("1. Управление данными")
        print("2. Анализ стратегий")
        print("3. ИИ-ассистент")
        print("4. Статистика и отчеты")
        print("5. Утилиты")
        print("0. Выход")
        print("="*50)
    
    def show_data_menu(self):
        """Меню управления данными"""
        while True:
            print("\n--- УПРАВЛЕНИЕ ДАННЫМИ ---")
            print("1. Добавить результат спина")
            print("2. Генерировать тестовые данные")
            print("3. Получить реальные данные")
            print("4. Мониторинг в реальном времени")
            print("5. Просмотр статистики")
            print("6. Экспорт данных")
            print("7. Очистить данные")
            print("0. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.add_single_spin()
            elif choice == "2":
                self.generate_test_data()
            elif choice == "3":
                self.get_live_data()
            elif choice == "4":
                self.start_live_monitoring()
            elif choice == "5":
                self.show_statistics()
            elif choice == "6":
                self.export_data()
            elif choice == "7":
                self.clear_data()
            elif choice == "0":
                break
    
    def show_strategy_menu(self):
        """Меню анализа стратегий"""
        while True:
            print("\n--- АНАЛИЗ СТРАТЕГИЙ ---")
            print("1. Тестировать готовые стратегии")
            print("2. Создать свою стратегию")
            print("3. Сравнить стратегии")
            print("4. История тестирований")
            print("0. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.test_predefined_strategies()
            elif choice == "2":
                self.create_custom_strategy()
            elif choice == "3":
                self.compare_strategies()
            elif choice == "0":
                break
    
    def show_ai_menu(self):
        """Меню ИИ-ассистента"""
        while True:
            print("\n--- ИИ-АССИСТЕНТ ---")
            print("1. Анализ данных ИИ")
            print("2. Генерация стратегий ИИ")
            print("3. Тестирование ИИ стратегий")
            print("4. Полный ИИ отчет")
            print("0. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.ai_analyze_data()
            elif choice == "2":
                self.ai_generate_strategies()
            elif choice == "3":
                self.ai_test_strategies()
            elif choice == "4":
                self.ai_full_report()
            elif choice == "0":
                break
    
    def add_single_spin(self):
        """Добавляет один результат спина"""
        print("\n--- ДОБАВЛЕНИЕ РЕЗУЛЬТАТА СПИНА ---")
        
        try:
            number = int(input("Введите выпавшее число (0-36): "))
            
            if not self.utils.validate_number(number):
                print("Ошибка: число должно быть от 0 до 36")
                return
            
            casino_name = input("Название казино (опционально): ").strip() or None
            table_name = input("Название стола (опционально): ").strip() or None
            
            spin_id = self.data_collector.add_spin(
                number=number,
                casino_name=casino_name,
                table_name=table_name
            )
            
            color = self.utils.get_color(number)
            print(f"✓ Спин добавлен (ID: {spin_id})")
            print(f"  Число: {number}")
            print(f"  Цвет: {color}")
            
        except ValueError:
            print("Ошибка: введите корректное число")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def generate_test_data(self):
        """Генерирует тестовые данные"""
        print("\n--- ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ ---")
        
        try:
            count = int(input("Количество спинов для генерации (рекомендуется 100-1000): "))
            
            if count <= 0 or count > 10000:
                print("Ошибка: количество должно быть от 1 до 10000")
                return
            
            days_back = int(input("За сколько дней назад генерировать (по умолчанию 7): ") or "7")
            start_date = datetime.now() - timedelta(days=days_back)
            
            print(f"Генерирую {count} спинов начиная с {start_date.strftime('%d.%m.%Y')}...")
            
            numbers = self.data_collector.generate_random_spins(count, start_date)
            
            print(f"✓ Сгенерировано {len(numbers)} спинов")
            
            # Показываем краткую статистику
            red_count = sum(1 for num in numbers if self.utils.get_color(num) == 'red')
            black_count = sum(1 for num in numbers if self.utils.get_color(num) == 'black')
            green_count = sum(1 for num in numbers if self.utils.get_color(num) == 'green')
            
            print(f"  Красных: {red_count} ({red_count/len(numbers)*100:.1f}%)")
            print(f"  Черных: {black_count} ({black_count/len(numbers)*100:.1f}%)")
            print(f"  Зеленых: {green_count} ({green_count/len(numbers)*100:.1f}%)")
            
        except ValueError:
            print("Ошибка: введите корректные числа")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def show_statistics(self):
        """Показывает статистику"""
        print("\n--- СТАТИСТИКА ---")
        
        try:
            days_back = int(input("За сколько дней показать статистику (по умолчанию 7): ") or "7")
            start_date = datetime.now() - timedelta(days=days_back)
            
            stats = self.data_collector.get_statistics(start_date)
            
            if "error" in stats:
                print(f"Ошибка: {stats['error']}")
                return
            
            print(f"\n=== СТАТИСТИКА ЗА {days_back} ДНЕЙ ===")
            print(f"Всего спинов: {stats['total_spins']}")
            print(f"Период: с {start_date.strftime('%d.%m.%Y')} по {datetime.now().strftime('%d.%m.%Y')}")
            
            print(f"\nЦВЕТА:")
            for color, count in stats['colors'].items():
                percentage = stats['percentages']['colors'][color]
                print(f"  {color.capitalize()}: {count} ({percentage}%)")
            
            print(f"\nЧЕТНОСТЬ:")
            for parity, count in stats['even_odd'].items():
                percentage = stats['percentages']['even_odd'][parity]
                print(f"  {parity.capitalize()}: {count} ({percentage}%)")
            
            print(f"\nДЮЖИНЫ:")
            for dozen, count in stats['dozens'].items():
                percentage = stats['percentages']['dozens'][dozen]
                print(f"  {dozen}-я дюжина: {count} ({percentage}%)")
            
            print(f"\nСАМЫЕ ЧАСТЫЕ ЧИСЛА:")
            for num, count in stats['most_frequent'][:5]:
                print(f"  {num}: {count} раз")
            
            print(f"\nСАМЫЕ РЕДКИЕ ЧИСЛА:")
            for num, count in stats['least_frequent'][:5]:
                print(f"  {num}: {count} раз")
                
        except ValueError:
            print("Ошибка: введите корректное число дней")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def test_predefined_strategies(self):
        """Тестирует готовые стратегии"""
        print("\n--- ТЕСТИРОВАНИЕ ГОТОВЫХ СТРАТЕГИЙ ---")
        
        try:
            days_back = int(input("За сколько дней тестировать (по умолчанию 7): ") or "7")
            start_date = datetime.now() - timedelta(days=days_back)
            
            initial_balance = float(input("Начальный баланс (по умолчанию 1000): ") or "1000")
            
            print("\nДоступные стратегии:")
            print("1. Следование за цветом")
            print("2. Малые числа (1-18)")
            print("3. Большие числа (19-36)")
            print("4. Антисерия (ждем 9 одного цвета)")
            print("5. Все мои стратегии")
            
            choice = input("Выберите стратегию (1-5): ").strip()
            
            strategies = []
            base_bet = 10
            if choice == "1":
                strategies = [UserStrategies.color_following_strategy(base_bet, 2.1)]
            elif choice == "2":
                strategies = [UserStrategies.low_numbers_strategy(base_bet, 2.05)]
            elif choice == "3":
                strategies = [UserStrategies.high_numbers_strategy(base_bet, 2.05)]
            elif choice == "4":
                strategies = [UserStrategies.anti_streak_strategy(base_bet, 2.2, 9)]
            elif choice == "5":
                strategies = get_all_user_strategies(base_bet)
            else:
                print("Неверный выбор")
                return
            
            print(f"\nТестирую стратегии на данных за {days_back} дней...")
            
            if len(strategies) == 1:
                result = self.game_analyzer.test_strategy(strategies[0], start_date, None, initial_balance)
                self._print_strategy_result(result)
            else:
                comparison = self.game_analyzer.compare_strategies(strategies, start_date, None, initial_balance)
                self._print_comparison_results(comparison)
                
        except ValueError:
            print("Ошибка: введите корректные числа")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def ai_analyze_data(self):
        """ИИ анализ данных"""
        print("\n--- ИИ АНАЛИЗ ДАННЫХ ---")
        
        try:
            days_back = int(input("За сколько дней анализировать (по умолчанию 7): ") or "7")
            start_date = datetime.now() - timedelta(days=days_back)
            
            print("ИИ анализирует данные...")
            analysis = self.ai_assistant.analyze_data(start_date)
            
            if "error" in analysis:
                print(f"Ошибка: {analysis['error']}")
                return
            
            print(f"\n=== ИИ АНАЛИЗ ЗА {days_back} ДНЕЙ ===")
            print(f"Всего спинов: {analysis['total_spins']}")
            
            # Основная статистика
            basic_stats = analysis['basic_statistics']
            print(f"\nОсновная статистика:")
            print(f"  Красных: {basic_stats['colors']['red']} ({basic_stats['percentages']['colors']['red']}%)")
            print(f"  Черных: {basic_stats['colors']['black']} ({basic_stats['percentages']['colors']['black']}%)")
            print(f"  Зеленых: {basic_stats['colors']['green']} ({basic_stats['percentages']['colors']['green']}%)")
            
            # Аномалии
            anomalies = analysis.get('anomalies', {})
            if anomalies.get('long_color_streaks'):
                print(f"\nДлинные серии:")
                for streak in anomalies['long_color_streaks'][:3]:
                    print(f"  {streak['color']}: {streak['length']} подряд")
            
            # Волатильность
            volatility = analysis.get('volatility', {})
            if 'trend' in volatility:
                print(f"\nВолатильность: {volatility['trend']}")
                print(f"Предсказуемость: {volatility['predictability']}")
                
        except ValueError:
            print("Ошибка: введите корректное число дней")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def ai_generate_strategies(self):
        """ИИ генерация стратегий"""
        print("\n--- ИИ ГЕНЕРАЦИЯ СТРАТЕГИЙ ---")
        
        try:
            days_back = int(input("На основе скольких дней создать стратегии (по умолчанию 10): ") or "10")
            start_date = datetime.now() - timedelta(days=days_back)
            
            print("Выберите уровень риска:")
            print("1. Низкий (консервативный)")
            print("2. Средний (сбалансированный)")
            print("3. Высокий (агрессивный)")
            
            risk_choice = input("Выбор (1-3): ").strip()
            risk_levels = {"1": "low", "2": "medium", "3": "high"}
            risk_level = risk_levels.get(risk_choice, "medium")
            
            print("ИИ анализирует данные и создает стратегии...")
            
            analysis = self.ai_assistant.analyze_data(start_date)
            if "error" in analysis:
                print(f"Ошибка анализа: {analysis['error']}")
                return
            
            strategies = self.ai_assistant.generate_strategies(analysis, risk_level)
            
            print(f"\n=== ИИ СОЗДАЛ {len(strategies)} СТРАТЕГИЙ ===")
            
            for i, strategy in enumerate(strategies, 1):
                if "error" in strategy:
                    print(f"Стратегия {i}: Ошибка - {strategy['error']}")
                    continue
                
                print(f"\n--- СТРАТЕГИЯ {i} ---")
                print(f"Название: {strategy['name']}")
                print(f"Описание: {strategy['description']}")
                print(f"Риск: {strategy['risk_level']}")
                print(f"Ожидаемая прибыль: {strategy.get('expected_profit', 'Не определена')}")
                print(f"Логика: {strategy.get('logic', 'Не указана')}")
                
                # Показываем параметры
                params = strategy.get('parameters', {})
                if params:
                    print("Параметры:")
                    for key, value in params.items():
                        print(f"  {key}: {value}")
            
            # Предлагаем протестировать
            test_choice = input("\nПротестировать эти стратегии? (y/n): ").strip().lower()
            if test_choice == 'y':
                self._test_ai_strategies_generated(strategies, start_date)
                
        except ValueError:
            print("Ошибка: введите корректные данные")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _test_ai_strategies_generated(self, strategies: list, start_date: datetime):
        """Тестирует сгенерированные ИИ стратегии"""
        try:
            initial_balance = float(input("Начальный баланс для тестирования (по умолчанию 1000): ") or "1000")
            
            print("Тестирую ИИ стратегии...")
            results = self.ai_assistant.test_ai_strategies(strategies, start_date, None, initial_balance)
            
            if "error" in results:
                print(f"Ошибка тестирования: {results['error']}")
                return
            
            self._print_comparison_results(results)
            
        except ValueError:
            print("Ошибка: введите корректный баланс")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _print_strategy_result(self, result: dict):
        """Выводит результат тестирования одной стратегии"""
        if "error" in result:
            print(f"Ошибка: {result['error']}")
            return
        
        print(f"\n=== РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ ===")
        print(f"Стратегия: {result['strategy_name']}")
        print(f"Начальный баланс: {result['initial_balance']:.2f}")
        print(f"Конечный баланс: {result['final_balance']:.2f}")
        print(f"Прибыль: {result['total_profit']:.2f} ({result['profit_percentage']:.1f}%)")
        print(f"Всего ставок: {result['total_bets']}")
        print(f"Выигрышных: {result['winning_bets']} ({result['win_rate']:.1f}%)")
        print(f"Проигрышных: {result['losing_bets']}")
        print(f"Максимальная просадка: {result['max_drawdown']:.2f}")
    
    def _print_comparison_results(self, comparison: dict):
        """Выводит результат сравнения стратегий"""
        if "error" in comparison:
            print(f"Ошибка: {comparison['error']}")
            return
        
        print(f"\n=== СРАВНЕНИЕ СТРАТЕГИЙ ===")
        print(f"Протестировано стратегий: {comparison['tested_strategies']}")
        print(f"Лучшая стратегия: {comparison['best_strategy']}")
        print(f"Лучшая прибыль: {comparison['best_profit']:.2f}")
        
        print(f"\nДетальные результаты:")
        for i, result in enumerate(comparison['results'], 1):
            print(f"\n{i}. {result['strategy_name']}")
            print(f"   Прибыль: {result['total_profit']:.2f} ({result['profit_percentage']:.1f}%)")
            print(f"   Процент побед: {result['win_rate']:.1f}%")
            print(f"   Просадка: {result['max_drawdown']:.2f}")
    
    def run(self):
        """Запуск главного цикла программы"""
        try:
            while True:
                self.show_menu()
                choice = input("\nВыберите действие: ").strip()
                
                if choice == "1":
                    self.show_data_menu()
                elif choice == "2":
                    self.show_strategy_menu()
                elif choice == "3":
                    self.show_ai_menu()
                elif choice == "4":
                    self.show_statistics()
                elif choice == "5":
                    print_roulette_info()
                elif choice == "0":
                    print("До свидания!")
                    break
                else:
                    print("Неверный выбор, попробуйте снова")
                    
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
        except Exception as e:
            print(f"\nНеожиданная ошибка: {e}")

    def get_live_data(self):
        """Получение реальных данных рулетки"""
        print("\n--- ПОЛУЧЕНИЕ РЕАЛЬНЫХ ДАННЫХ ---")
        
        # Тестируем доступность источников
        connections = self.live_collector.test_connection()
        
        print("Доступные источники данных:")
        print("1. Симуляция реальных данных (всегда доступна)")
        if connections.get('api'):
            print("2. API онлайн-казино")
        if connections.get('scrape'):
            print("3. Веб-скрапинг")
        
        print("\n--- ВАРИАНТЫ ПОЛУЧЕНИЯ ДАННЫХ ---")
        print("1. Получить последние результаты")
        print("2. Загрузить исторические данные")
        print("3. Тест источников данных")
        print("0. Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            self._get_recent_results()
        elif choice == "2":
            self._load_historical_data()
        elif choice == "3":
            self._test_data_sources()
        elif choice == "0":
            return
    
    def start_live_monitoring(self):
        """Запуск мониторинга в реальном времени"""
        print("\n--- МОНИТОРИНГ В РЕАЛЬНОМ ВРЕМЕНИ ---")
        print("⚠️  ВНИМАНИЕ: Это будет получать данные в реальном времени")
        print("   и сразу сохранять их в базу данных для тестирования стратегий")
        
        try:
            duration = int(input("На сколько минут запустить мониторинг (по умолчанию 30): ") or "30")
            
            print(f"\n🎰 Запускаем мониторинг на {duration} минут...")
            print("   Нажмите Ctrl+C для остановки")
            
            # Запускаем получение данных в реальном времени
            results = self.live_collector.get_live_stream(duration)
            
            print(f"\n✅ Мониторинг завершен. Получено {len(results)} результатов")
            
            # Показываем статистику полученных данных
            if results:
                self._show_live_data_stats(results)
                
                test_choice = input("\nПротестировать стратегии на новых данных? (y/n): ").strip().lower()
                if test_choice == 'y':
                    self.test_predefined_strategies()
                    
        except KeyboardInterrupt:
            print("\n⏹️  Мониторинг остановлен пользователем")
        except ValueError:
            print("Ошибка: введите корректное число минут")
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")
    
    def _get_recent_results(self):
        """Получить последние результаты"""
        try:
            count = int(input("Сколько последних результатов получить (по умолчанию 50): ") or "50")
            
            print(f"\n🔄 Получаем {count} последних результатов...")
            
            results = self.live_collector.get_live_results('mock', limit=count)
            
            print(f"\n📊 Получено {len(results)} результатов:")
            print("=" * 50)
            
            # Показываем последние 10 результатов
            for result in results[-10:]:
                timestamp = result['timestamp'].strftime('%H:%M:%S')
                print(f"{timestamp}: {result['number']:2d} ({result['color']})")
            
            if len(results) > 10:
                print(f"... и еще {len(results) - 10} результатов")
            
            # Сохраняем в базу данных
            save_choice = input("\nСохранить результаты в базу данных? (y/n): ").strip().lower()
            if save_choice == 'y':
                saved_count = 0
                for result in results:
                    try:
                        self.data_collector.add_spin(
                            number=result['number'],
                            timestamp=result['timestamp']
                        )
                        saved_count += 1
                    except Exception as e:
                        print(f"Ошибка сохранения: {e}")
                
                print(f"✅ Сохранено {saved_count} результатов в базу данных")
                
        except ValueError:
            print("Ошибка: введите корректное число")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _load_historical_data(self):
        """Загрузить исторические данные"""
        try:
            days = int(input("За сколько дней загрузить данные (по умолчанию 7): ") or "7")
            
            print(f"\n📈 Загружаем исторические данные за {days} дней...")
            
            historical_data = self.live_collector.get_historical_data(days)
            
            print(f"\n📊 Получено {len(historical_data)} исторических записей")
            
            # Показываем статистику
            self._show_live_data_stats(historical_data)
            
            # Сохраняем в базу данных
            save_choice = input("\nСохранить данные в базу? (y/n): ").strip().lower()
            if save_choice == 'y':
                saved_count = 0
                for result in historical_data:
                    try:
                        self.data_collector.add_spin(
                            number=result['number'],
                            timestamp=result['timestamp']
                        )
                        saved_count += 1
                    except Exception as e:
                        continue  # Пропускаем дубликаты
                
                print(f"✅ Сохранено {saved_count} записей в базу данных")
                
        except ValueError:
            print("Ошибка: введите корректное число дней")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _test_data_sources(self):
        """Тестирование источников данных"""
        print("\n🔌 Тестирование источников данных...")
        
        connections = self.live_collector.test_connection()
        
        print("\n📋 Результаты тестирования:")
        print("=" * 40)
        
        for source, available in connections.items():
            status = "✅ Доступен" if available else "❌ Недоступен"
            description = {
                'mock': 'Симуляция реальных данных',
                'api': 'API онлайн-казино',
                'scrape': 'Веб-скрапинг'
            }.get(source, source)
            
            print(f"{description}: {status}")
        
        # Демонстрация получения данных
        print(f"\n🎯 Демонстрация получения данных:")
        demo_results = self.live_collector.get_live_results('mock', limit=5)
        
        for result in demo_results:
            timestamp = result['timestamp'].strftime('%H:%M:%S')
            print(f"   {timestamp}: {result['number']:2d} ({result['color']}) - {result['source']}")
    
    def _show_live_data_stats(self, results):
        """Показать статистику полученных данных"""
        if not results:
            return
        
        # Подсчитываем статистику
        colors = {'red': 0, 'black': 0, 'green': 0}
        numbers_count = {}
        
        for result in results:
            color = result['color']
            number = result['number']
            
            colors[color] += 1
            numbers_count[number] = numbers_count.get(number, 0) + 1
        
        total = len(results)
        
        print(f"\n📈 СТАТИСТИКА ПОЛУЧЕННЫХ ДАННЫХ:")
        print("=" * 40)
        print(f"Всего спинов: {total}")
        print(f"Красных: {colors['red']} ({colors['red']/total*100:.1f}%)")
        print(f"Черных: {colors['black']} ({colors['black']/total*100:.1f}%)")
        print(f"Зеленых: {colors['green']} ({colors['green']/total*100:.1f}%)")
        
        # Показываем самые частые числа
        if numbers_count:
            sorted_numbers = sorted(numbers_count.items(), key=lambda x: x[1], reverse=True)
            print(f"\nСамые частые числа:")
            for number, count in sorted_numbers[:5]:
                percentage = count/total*100
                print(f"  {number:2d}: {count} раз ({percentage:.1f}%)")
    
    def compare_strategies(self):
        """Сравнение стратегий"""
        print("\n--- СРАВНЕНИЕ СТРАТЕГИЙ ---")
        
        try:
            days_back = int(input("За сколько дней тестировать (по умолчанию 7): ") or "7")
            initial_balance = int(input("Начальный баланс (по умолчанию 10000): ") or "10000")
            
            start_date = datetime.now() - timedelta(days=days_back)
            
            print("\nВыберите стратегии для сравнения:")
            print("1. Следование цвету")
            print("2. Малые числа (1-18)")
            print("3. Большие числа (19-36)")
            print("4. Анти-серия")
            print("5. Все стратегии")
            
            choice = input("Выбор (1-5): ").strip()
            
            strategies = []
            base_bet = 10
            
            if choice == "1":
                strategies = [UserStrategies.color_following_strategy(base_bet, 2.1)]
            elif choice == "2":
                strategies = [UserStrategies.low_numbers_strategy(base_bet, 2.05)]
            elif choice == "3":
                strategies = [UserStrategies.high_numbers_strategy(base_bet, 2.05)]
            elif choice == "4":
                strategies = [UserStrategies.anti_streak_strategy(base_bet, 2.2, 9)]
            elif choice == "5":
                strategies = get_all_user_strategies(base_bet)
            else:
                print("Неверный выбор")
                return
            
            print(f"\nСравниваю стратегии на данных за {days_back} дней...")
            
            comparison = self.game_analyzer.compare_strategies(strategies, start_date, None, initial_balance)
            self._print_comparison_results(comparison)
                
        except ValueError:
            print("Ошибка: введите корректные числа")
        except Exception as e:
            print(f"Ошибка: {e}")


def main():
    """Главная функция"""
    try:
        # Проверяем наличие необходимых библиотек
        required_modules = ['sqlite3', 'datetime', 'random', 'json']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"Отсутствуют необходимые модули: {', '.join(missing_modules)}")
            print("Установите их с помощью: pip install [module_name]")
            return
        
        # Создаем и запускаем систему
        system = RouletteAnalysisSystem()
        system.run()
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        print("Обратитесь к разработчику")


if __name__ == "__main__":
    main()