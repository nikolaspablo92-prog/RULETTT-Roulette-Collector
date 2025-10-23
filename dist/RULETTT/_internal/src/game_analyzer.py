"""
АНАЛИЗАТОР ИГРОВЫХ СХЕМ
======================

Этот модуль позволяет тестировать различные стратегии игры в рулетку на исторических данных.

Простыми словами:
- Берет вашу стратегию игры
- Проверяет как она работала бы на реальных данных
- Показывает прибыль/убыток
- Помогает найти лучшие схемы игры
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
import json
from pathlib import Path

from data_collector import DataCollector
from utils import RouletteUtils


class GameStrategy:
    """Класс для описания игровой стратегии"""
    
    def __init__(self, name: str, description: str):
        """
        Инициализация стратегии
        
        Args:
            name (str): Название стратегии
            description (str): Описание стратегии
        """
        self.name = name
        self.description = description
        self.balance = 0.0
        self.initial_balance = 0.0
        self.bets_history = []
        self.current_spin = 0
        
    def reset(self, initial_balance: float = 1000.0):
        """
        Сбросить стратегию к начальному состоянию
        
        Простыми словами: Начать игру заново с чистого листа
        
        Args:
            initial_balance (float): Начальный баланс
        """
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.bets_history = []
        self.current_spin = 0
    
    def make_bet(self, spin_number: int, history: List[Dict]) -> Dict:
        """
        Делает ставку на основе стратегии
        
        Простыми словами: Решает куда и сколько поставить денег
        
        Args:
            spin_number (int): Номер текущего спина
            history (List[Dict]): История предыдущих спинов
            
        Returns:
            Dict: Информация о ставке {"type": "color", "numbers": ["red"], "amount": 10}
        """
        # Это базовый класс, конкретные стратегии должны переопределить этот метод
        return {"type": "color", "numbers": ["red"], "amount": 10}
    
    def update_balance(self, bet_result: Dict):
        """
        Обновляет баланс после результата ставки
        
        Args:
            bet_result (Dict): Результат ставки с информацией о выплате
        """
        payout = bet_result.get("payout", 0)
        bet_amount = bet_result.get("bet_amount", 0)
        
        # Вычитаем ставку и добавляем выплату
        self.balance = self.balance - bet_amount + payout
        
        # Записываем в историю
        self.bets_history.append({
            "spin": self.current_spin,
            "bet": bet_result,
            "balance_after": self.balance,
            "profit": self.balance - self.initial_balance
        })


class PredefinedStrategies:
    """Предопределенные стратегии для тестирования"""
    
    @staticmethod
    def martingale_red(initial_bet: float = 10) -> GameStrategy:
        """
        Стратегия Мартингейл на красное
        
        Простыми словами: Ставим на красное, если проиграли - удваиваем ставку
        
        Args:
            initial_bet (float): Начальная ставка
            
        Returns:
            GameStrategy: Настроенная стратегия
        """
        strategy = GameStrategy(
            name="Мартингейл Красное",
            description=f"Ставка на красное с удвоением при проигрыше. Начальная ставка: {initial_bet}"
        )
        
        strategy.current_bet = initial_bet
        strategy.consecutive_losses = 0
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            # Если это первый спин или предыдущий выиграл
            if not history or history[-1].get('won', False):
                strategy.current_bet = initial_bet
                strategy.consecutive_losses = 0
            else:
                # Если проиграли - удваиваем ставку
                strategy.current_bet *= 2
                strategy.consecutive_losses += 1
            
            return {
                "type": "color", 
                "numbers": ["red"], 
                "amount": min(strategy.current_bet, strategy.balance)  # Не ставим больше чем есть
            }
        
        strategy.make_bet = make_bet_logic
        return strategy
    
    @staticmethod
    def dozen_rotation(initial_bet: float = 15) -> GameStrategy:
        """
        Стратегия ротации дюжин
        
        Простыми словами: Поочередно ставим на разные дюжины
        
        Args:
            initial_bet (float): Размер ставки
            
        Returns:
            GameStrategy: Настроенная стратегия
        """
        strategy = GameStrategy(
            name="Ротация Дюжин",
            description=f"Поочередные ставки на дюжины. Ставка: {initial_bet}"
        )
        
        strategy.current_dozen = 1
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            # Переключаем дюжину
            dozen_to_bet = strategy.current_dozen
            strategy.current_dozen = (strategy.current_dozen % 3) + 1
            
            return {
                "type": "dozen",
                "numbers": [dozen_to_bet],
                "amount": min(initial_bet, strategy.balance)
            }
        
        strategy.make_bet = make_bet_logic
        return strategy
    
    @staticmethod
    def hot_numbers(initial_bet: float = 5, look_back: int = 50) -> GameStrategy:
        """
        Стратегия горячих чисел
        
        Простыми словами: Ставим на числа которые часто выпадали недавно
        
        Args:
            initial_bet (float): Размер ставки на число
            look_back (int): Сколько последних спинов анализировать
            
        Returns:
            GameStrategy: Настроенная стратегия
        """
        strategy = GameStrategy(
            name="Горячие Числа",
            description=f"Ставки на {look_back} самых частых чисел из последних {look_back} спинов"
        )
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            if len(history) < 10:  # Недостаточно данных
                return {"type": "color", "numbers": ["red"], "amount": initial_bet}
            
            # Анализируем последние спины
            recent_history = history[-look_back:] if len(history) >= look_back else history
            
            # Считаем частоту чисел
            number_counts = {}
            for spin in recent_history:
                num = spin['number']
                number_counts[num] = number_counts.get(num, 0) + 1
            
            # Находим самые частые числа
            hot_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            hot_nums = [num for num, count in hot_numbers if count > 1]
            
            if not hot_nums:
                # Если нет горячих чисел, ставим на красное
                return {"type": "color", "numbers": ["red"], "amount": initial_bet}
            
            return {
                "type": "number",
                "numbers": hot_nums,
                "amount": min(initial_bet * len(hot_nums), strategy.balance)
            }
        
        strategy.make_bet = make_bet_logic
        return strategy


class GameAnalyzer:
    """Основной класс для анализа игровых стратегий"""
    
    def __init__(self, data_collector: DataCollector):
        """
        Инициализация анализатора
        
        Args:
            data_collector (DataCollector): Сборщик данных для получения истории
        """
        self.data_collector = data_collector
        self.utils = RouletteUtils()
        
    def test_strategy(self, strategy: GameStrategy, start_date: datetime, 
                     end_date: datetime = None, initial_balance: float = 1000.0) -> Dict:
        """
        Тестирует стратегию на исторических данных
        
        Простыми словами: Проверяем как стратегия работала бы в прошлом
        
        Args:
            strategy (GameStrategy): Стратегия для тестирования
            start_date (datetime): Начальная дата периода
            end_date (datetime): Конечная дата периода
            initial_balance (float): Начальный баланс
            
        Returns:
            Dict: Результаты тестирования
        """
        # Получаем исторические данные
        spins = self.data_collector.get_spins_by_period(start_date, end_date)
        
        if len(spins) < 10:
            return {"error": "Недостаточно данных для тестирования"}
        
        # Сбрасываем стратегию
        strategy.reset(initial_balance)
        
        print(f"Тестируем стратегию '{strategy.name}' на {len(spins)} спинах...")
        
        # Проходим по каждому спину
        for i, spin in enumerate(spins):
            if strategy.balance <= 0:
                print("Баланс исчерпан, тестирование остановлено")
                break
            
            strategy.current_spin = i + 1
            
            # Получаем историю предыдущих спинов
            history = spins[:i] if i > 0 else []
            
            # Стратегия делает ставку
            bet_info = strategy.make_bet(i + 1, history)
            
            # Проверяем не пропускается ли ставка
            if bet_info.get("type") == "skip" or bet_info.get("amount", 0) <= 0:
                # Пропускаем этот спин, ставка не делается
                continue
            
            # Проверяем результат ставки
            winning_number = spin['number']
            bet_result = self._calculate_bet_result(bet_info, winning_number)
            
            # Обновляем баланс
            strategy.update_balance(bet_result)
            
            # Показываем прогресс каждые 100 спинов
            if (i + 1) % 100 == 0:
                current_profit = strategy.balance - initial_balance
                print(f"Спин {i + 1}/{len(spins)}, баланс: {strategy.balance:.2f}, прибыль: {current_profit:.2f}")
        
        # Подсчитываем результаты
        final_balance = strategy.balance
        total_profit = final_balance - initial_balance
        total_bets = len(strategy.bets_history)
        winning_bets = sum(1 for bet in strategy.bets_history if bet['bet']['payout'] > 0)
        
        win_rate = (winning_bets / total_bets * 100) if total_bets > 0 else 0
        
        # Находим максимальную просадку
        max_balance = initial_balance
        max_drawdown = 0
        for bet in strategy.bets_history:
            balance_after = bet['balance_after']
            if balance_after > max_balance:
                max_balance = balance_after
            drawdown = max_balance - balance_after
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        results = {
            "strategy_name": strategy.name,
            "period": {"start": start_date, "end": end_date or datetime.now()},
            "initial_balance": initial_balance,
            "final_balance": final_balance,
            "total_profit": total_profit,
            "profit_percentage": (total_profit / initial_balance * 100),
            "total_bets": total_bets,
            "winning_bets": winning_bets,
            "losing_bets": total_bets - winning_bets,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "spins_tested": len(spins),
            "bets_history": strategy.bets_history
        }
        
        return results
    
    def _calculate_bet_result(self, bet_info: Dict, winning_number: int) -> Dict:
        """
        Рассчитывает результат ставки
        
        Args:
            bet_info (Dict): Информация о ставке
            winning_number (int): Выигрышное число
            
        Returns:
            Dict: Результат ставки с выплатой
        """
        bet_type = bet_info.get("type", "color")
        bet_numbers = bet_info.get("numbers", [])
        bet_amount = bet_info.get("amount", 0)
        
        # Используем функцию из утилит для расчета выплаты
        payout = self.utils.calculate_payout(bet_type, bet_amount, winning_number, bet_numbers)
        
        won = payout > 0
        profit = payout - bet_amount if won else -bet_amount
        
        return {
            "bet_type": bet_type,
            "bet_numbers": bet_numbers,
            "bet_amount": bet_amount,
            "winning_number": winning_number,
            "payout": payout,
            "won": won,
            "profit": profit
        }
    
    def compare_strategies(self, strategies: List[GameStrategy], start_date: datetime,
                          end_date: datetime = None, initial_balance: float = 1000.0) -> Dict:
        """
        Сравнивает несколько стратегий
        
        Простыми словами: Тестирует разные стратегии и показывает какая лучше
        
        Args:
            strategies (List[GameStrategy]): Список стратегий для сравнения
            start_date (datetime): Начальная дата
            end_date (datetime): Конечная дата
            initial_balance (float): Начальный баланс
            
        Returns:
            Dict: Сравнительные результаты
        """
        print(f"Сравниваем {len(strategies)} стратегий...")
        
        results = []
        for strategy in strategies:
            result = self.test_strategy(strategy, start_date, end_date, initial_balance)
            if "error" not in result:
                results.append(result)
        
        if not results:
            return {"error": "Не удалось протестировать ни одну стратегию"}
        
        # Сортируем по прибыли
        results.sort(key=lambda x: x["total_profit"], reverse=True)
        
        comparison = {
            "tested_strategies": len(results),
            "period": {"start": start_date, "end": end_date or datetime.now()},
            "initial_balance": initial_balance,
            "best_strategy": results[0]["strategy_name"],
            "best_profit": results[0]["total_profit"],
            "results": results,
            "summary": {
                "most_profitable": results[0]["strategy_name"],
                "highest_win_rate": max(results, key=lambda x: x["win_rate"])["strategy_name"],
                "lowest_drawdown": min(results, key=lambda x: x["max_drawdown"])["strategy_name"]
            }
        }
        
        return comparison
    
    def save_strategy_results(self, results: Dict, filepath: str):
        """
        Сохраняет результаты тестирования в файл
        
        Args:
            results (Dict): Результаты тестирования
            filepath (str): Путь к файлу для сохранения
        """
        # Преобразуем datetime объекты в строки для JSON
        def datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=datetime_converter)
        
        print(f"Результаты сохранены в {filepath}")


# Тестирование
if __name__ == "__main__":
    print("Тестируем анализатор стратегий...")
    
    # Создаем сборщик данных и генерируем тестовые данные
    collector = DataCollector("../data/test_analyzer.db")
    
    # Генерируем данные за последнюю неделю
    start_date = datetime.now() - timedelta(days=7)
    print("Генерируем тестовые данные...")
    collector.generate_random_spins(500, start_date)
    
    # Создаем анализатор
    analyzer = GameAnalyzer(collector)
    
    # Тестируем предопределенные стратегии
    strategies = [
        PredefinedStrategies.martingale_red(10),
        PredefinedStrategies.dozen_rotation(15),
        PredefinedStrategies.hot_numbers(5, 30)
    ]
    
    # Сравниваем стратегии
    print("\nСравниваем стратегии...")
    comparison = analyzer.compare_strategies(strategies, start_date)
    
    print(f"\n=== РЕЗУЛЬТАТЫ СРАВНЕНИЯ ===")
    print(f"Лучшая стратегия: {comparison['best_strategy']}")
    print(f"Прибыль: {comparison['best_profit']:.2f}")
    
    for result in comparison['results']:
        print(f"\n{result['strategy_name']}:")
        print(f"  Прибыль: {result['total_profit']:.2f} ({result['profit_percentage']:.1f}%)")
        print(f"  Процент побед: {result['win_rate']:.1f}%")
        print(f"  Максимальная просадка: {result['max_drawdown']:.2f}")
    
    print("\nТест завершен!")