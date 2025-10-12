"""
🎯 ИНТЕГРАЦИЯ ДАННЫХ ИЗ КОНСОЛИ В СИСТЕМУ АНАЛИЗА
=================================================

Этот скрипт берет данные из консоли браузера и использует их
для анализа рулетки и проверки стратегий игры.

ИСПОЛЬЗОВАНИЕ:
1. Получите данные из консоли браузера (они в буфере обмена)
2. Вставьте в файл roulette_console_data.json
3. Запустите: py console_to_analysis.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

from utils import RouletteUtils


class ConsoleDataAnalyzer:
    """Анализатор данных из консоли браузера"""
    
    def __init__(self, data_file: str = "roulette_console_data.json"):
        """
        Инициализация анализатора
        
        Args:
            data_file: Путь к файлу с данными из консоли
        """
        self.data_file = Path(data_file)
        self.data = []
        self.stats = {}
        
    def load_data(self) -> bool:
        """
        Загружает данные из JSON файла
        
        Returns:
            bool: True если данные загружены успешно
        """
        try:
            if not self.data_file.exists():
                print(f"❌ Файл не найден: {self.data_file}")
                print(f"")
                print(f"💡 ИНСТРУКЦИЯ:")
                print(f"   1. Откройте консоль браузера на странице рулетки")
                print(f"   2. Запустите код для извлечения данных")
                print(f"   3. Введите: copy(JSON.stringify(window.rouletteResults, null, 2))")
                print(f"   4. Создайте файл '{self.data_file}' и вставьте данные (Ctrl+V)")
                print(f"   5. Запустите этот скрипт снова")
                return False
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            print(f"✅ Загружено {len(self.data)} результатов из консоли")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка формата JSON: {e}")
            print(f"💡 Проверьте что файл содержит корректный JSON")
            return False
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return False
    
    def convert_to_analyzer_format(self) -> list:
        """
        Конвертирует данные из консоли в формат для анализатора
        
        Returns:
            list: Данные в формате для GameAnalyzer
        """
        converted = []
        base_time = datetime.now()
        
        for i, result in enumerate(self.data):
            # Создаем временную метку (каждый спин ~1 минута)
            spin_time = base_time.replace(second=0, microsecond=0) - timedelta(minutes=len(self.data) - i)
            
            converted.append({
                "number": result["number"],
                "color": result["color"],
                "time": spin_time.isoformat(),
                "table_id": "console_data",
                "source": "browser_console"
            })
        
        return converted
    
    def calculate_statistics(self):
        """Рассчитывает базовую статистику по данным"""
        if not self.data:
            return
        
        numbers = [r["number"] for r in self.data]
        colors = [r["color"] for r in self.data]
        
        # Подсчет цветов
        color_counts = {
            "red": colors.count("red"),
            "black": colors.count("black"),
            "green": colors.count("green")
        }
        
        # Самые частые числа
        number_counts = {}
        for num in numbers:
            number_counts[num] = number_counts.get(num, 0) + 1
        
        sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Серии
        red_series = self._find_series(colors, "red")
        black_series = self._find_series(colors, "black")
        
        self.stats = {
            "total_spins": len(self.data),
            "color_distribution": color_counts,
            "color_percentages": {
                color: round(count / len(self.data) * 100, 1)
                for color, count in color_counts.items()
            },
            "top_numbers": sorted_numbers[:5],
            "max_red_series": max(red_series) if red_series else 0,
            "max_black_series": max(black_series) if black_series else 0,
            "unique_numbers": len(set(numbers))
        }
    
    def _find_series(self, colors: list, target_color: str) -> list:
        """Находит серии одного цвета"""
        series = []
        current_series = 0
        
        for color in colors:
            if color == target_color:
                current_series += 1
            else:
                if current_series > 0:
                    series.append(current_series)
                current_series = 0
        
        if current_series > 0:
            series.append(current_series)
        
        return series
    
    def print_statistics(self):
        """Выводит статистику на экран"""
        if not self.stats:
            self.calculate_statistics()
        
        print("\n" + "="*60)
        print("📊 СТАТИСТИКА ПО ДАННЫМ ИЗ КОНСОЛИ")
        print("="*60)
        
        print(f"\n🎰 Всего спинов: {self.stats['total_spins']}")
        print(f"🔢 Уникальных чисел: {self.stats['unique_numbers']}")
        
        print(f"\n🎨 Распределение по цветам:")
        for color, count in self.stats['color_distribution'].items():
            emoji = "🔴" if color == "red" else "⚫" if color == "black" else "🟢"
            pct = self.stats['color_percentages'][color]
            print(f"   {emoji} {color.upper()}: {count} ({pct}%)")
        
        print(f"\n🔥 Топ-5 самых частых чисел:")
        for i, (number, count) in enumerate(self.stats['top_numbers'], 1):
            color = RouletteUtils.get_color(number)
            emoji = "🔴" if color == "red" else "⚫" if color == "black" else "🟢"
            print(f"   {i}. {emoji} {number}: {count} раз")
        
        print(f"\n📈 Максимальные серии:")
        print(f"   🔴 Красных подряд: {self.stats['max_red_series']}")
        print(f"   ⚫ Черных подряд: {self.stats['max_black_series']}")
        
        print("\n" + "="*60)
    
    def test_strategies(self, initial_balance: float = 1000.0):
        """
        Тестирует различные стратегии игры на данных из консоли
        
        Args:
            initial_balance: Начальный баланс для тестирования
        """
        print("\n" + "="*60)
        print("🎲 ТЕСТИРОВАНИЕ СТРАТЕГИЙ")
        print("="*60)
        
        if len(self.data) < 10:
            print("\n⚠️  Недостаточно данных для тестирования стратегий")
            print("   Минимум нужно 10 спинов, у вас:", len(self.data))
            print("   Соберите больше данных из консоли браузера!")
            return
        
        # Определяем стратегии для тестирования
        strategies = {
            "Мартингейл на красное": self._martingale_strategy("red", 10),
            "Мартингейл на черное": self._martingale_strategy("black", 10),
            "Фиксированная ставка на красное": self._flat_bet_strategy("red", 10),
            "Фиксированная ставка на черное": self._flat_bet_strategy("black", 10),
        }
        
        results = []
        
        for strategy_name, strategy_func in strategies.items():
            print(f"\n🎯 Тестирование: {strategy_name}")
            print(f"   Начальный баланс: ${initial_balance}")
            
            # Тестируем стратегию
            result = strategy_func(initial_balance)
            
            final_balance = result["final_balance"]
            profit = final_balance - initial_balance
            profit_pct = (profit / initial_balance) * 100
            
            emoji = "✅" if profit > 0 else "❌" if profit < 0 else "➖"
            
            print(f"   {emoji} Конечный баланс: ${final_balance:.2f}")
            print(f"   {emoji} Прибыль/Убыток: ${profit:.2f} ({profit_pct:+.1f}%)")
            print(f"   📊 Всего ставок: {result['total_bets']}")
            print(f"   🎯 Выигрышных: {result['winning_bets']} ({result['win_rate']:.1f}%)")
            
            results.append({
                "strategy": strategy_name,
                "profit": profit,
                "profit_pct": profit_pct,
                "final_balance": final_balance,
                "total_bets": result['total_bets'],
                "win_rate": result['win_rate']
            })
        
        # Показываем лучшую стратегию
        best = max(results, key=lambda x: x["profit"])
        worst = min(results, key=lambda x: x["profit"])
        
        print("\n" + "="*60)
        print("🏆 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*60)
        print(f"\n✅ Лучшая стратегия: {best['strategy']}")
        print(f"   Прибыль: ${best['profit']:.2f} ({best['profit_pct']:+.1f}%)")
        print(f"\n❌ Худшая стратегия: {worst['strategy']}")
        print(f"   Убыток: ${worst['profit']:.2f} ({worst['profit_pct']:+.1f}%)")
        print("\n" + "="*60)
    
    def _martingale_strategy(self, target_color: str, initial_bet: float):
        """Стратегия Мартингейл - удвоение ставки после проигрыша"""
        def test(initial_balance: float):
            balance = initial_balance
            current_bet = initial_bet
            total_bets = 0
            winning_bets = 0
            
            for result in self.data:
                if balance <= 0 or current_bet > balance:
                    break
                
                # Делаем ставку
                balance -= current_bet
                total_bets += 1
                
                # Проверяем выигрыш
                if result["color"] == target_color:
                    payout = current_bet * 2  # Выплата 2:1 за цвет
                    balance += payout
                    winning_bets += 1
                    current_bet = initial_bet  # Сбрасываем ставку
                else:
                    # Удваиваем ставку после проигрыша
                    current_bet = min(current_bet * 2, balance)
            
            return {
                "final_balance": balance,
                "total_bets": total_bets,
                "winning_bets": winning_bets,
                "win_rate": (winning_bets / total_bets * 100) if total_bets > 0 else 0
            }
        
        return test
    
    def _flat_bet_strategy(self, target_color: str, bet_amount: float):
        """Фиксированная ставка - всегда одинаковая сумма"""
        def test(initial_balance: float):
            balance = initial_balance
            total_bets = 0
            winning_bets = 0
            
            for result in self.data:
                if balance <= 0 or bet_amount > balance:
                    break
                
                # Делаем ставку
                balance -= bet_amount
                total_bets += 1
                
                # Проверяем выигрыш
                if result["color"] == target_color:
                    payout = bet_amount * 2  # Выплата 2:1 за цвет
                    balance += payout
                    winning_bets += 1
            
            return {
                "final_balance": balance,
                "total_bets": total_bets,
                "winning_bets": winning_bets,
                "win_rate": (winning_bets / total_bets * 100) if total_bets > 0 else 0
            }
        
        return test
    
    def save_analysis_report(self, filename: str = "console_analysis_report.txt"):
        """Сохраняет отчет анализа в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ АНАЛИЗА ДАННЫХ ИЗ КОНСОЛИ БРАУЗЕРА\n")
            f.write("="*60 + "\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Источник данных: {self.data_file}\n")
            f.write("\n")
            
            if self.stats:
                f.write("СТАТИСТИКА:\n")
                f.write(f"Всего спинов: {self.stats['total_spins']}\n")
                f.write(f"Уникальных чисел: {self.stats['unique_numbers']}\n")
                f.write("\nРаспределение цветов:\n")
                for color, count in self.stats['color_distribution'].items():
                    pct = self.stats['color_percentages'][color]
                    f.write(f"  {color}: {count} ({pct}%)\n")
                f.write("\n")
        
        print(f"\n💾 Отчет сохранен: {filename}")


def main():
    """Основная функция"""
    print("="*60)
    print("🎰 АНАЛИЗ ДАННЫХ ИЗ КОНСОЛИ БРАУЗЕРА")
    print("="*60)
    
    # Создаем анализатор
    analyzer = ConsoleDataAnalyzer("roulette_console_data.json")
    
    # Загружаем данные
    if not analyzer.load_data():
        return
    
    # Показываем статистику
    analyzer.calculate_statistics()
    analyzer.print_statistics()
    
    # Тестируем стратегии
    analyzer.test_strategies(initial_balance=1000.0)
    
    # Сохраняем отчет
    analyzer.save_analysis_report()
    
    print("\n✅ Анализ завершен!")
    print("\n💡 СОВЕТ: Запускайте этот скрипт после каждого обновления данных")
    print("   из консоли браузера для актуальной статистики!\n")


if __name__ == "__main__":
    main()
