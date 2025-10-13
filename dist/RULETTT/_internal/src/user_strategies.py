"""
ПОЛЬЗОВАТЕЛЬСКИЕ СТРАТЕГИИ
=========================

Этот модуль содержит стратегии, разработанные пользователем.

Простыми словами:
1. Следование за выигрывающим цветом с прогрессией
2. Ставки на малые числа (1-18) с прогрессией  
3. Ставки на большие числа (19-36) с прогрессией
4. Стратегия антисерии - ставка против длинных серий
"""

from datetime import datetime
from typing import List, Dict
from game_analyzer import GameStrategy
from utils import RouletteUtils


class UserStrategies:
    """Пользовательские стратегии с умным прогрессивным умножением"""
    
    @staticmethod
    def color_following_strategy(initial_bet: float = 10, multiplier: float = 2.1) -> GameStrategy:
        """
        Стратегия 1: Следование за цветом
        
        Простыми словами: Ставим на цвет который только что выиграл,
        если проиграли - увеличиваем ставку с умным расчетом для минимальной прибыли
        
        Args:
            initial_bet (float): Минимальная ставка
            multiplier (float): Коэффициент умножения (2.1 для минимального профита)
        """
        strategy = GameStrategy(
            name="Следование за Цветом",
            description=f"Ставим на выигравший цвет, при проигрыше умножаем на {multiplier}"
        )
        
        strategy.current_bet = initial_bet
        strategy.initial_bet = initial_bet
        strategy.target_color = "red"  # Начинаем с красного
        strategy.losses_in_row = 0
        strategy.multiplier = multiplier
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            if not history:
                # Первая ставка - на красное
                strategy.target_color = "red"
                strategy.current_bet = strategy.initial_bet
            else:
                last_spin = history[-1]
                last_color = last_spin['color']
                
                if last_color == 'green':
                    # Зеро - продолжаем с тем же цветом
                    pass
                else:
                    # Проверяем выиграли ли мы
                    if last_color == strategy.target_color:
                        # Выиграли! Продолжаем ставить на этот цвет с минимальной ставкой
                        strategy.current_bet = strategy.initial_bet
                        strategy.losses_in_row = 0
                        strategy.target_color = last_color
                    else:
                        # Проиграли - умножаем ставку для возврата потерь + минимальная прибыль
                        strategy.losses_in_row += 1
                        strategy.current_bet *= strategy.multiplier
                        # Цель остается та же
            
            # Ограничиваем ставку балансом
            bet_amount = min(strategy.current_bet, strategy.balance)
            
            return {
                "type": "color",
                "numbers": [strategy.target_color],
                "amount": bet_amount
            }
        
        strategy.make_bet = make_bet_logic
        return strategy
    
    @staticmethod
    def low_numbers_strategy(initial_bet: float = 10, multiplier: float = 2.05) -> GameStrategy:
        """
        Стратегия 2: Ставки на малые числа (1-18)
        
        Простыми словами: Всегда ставим на числа 1-18,
        если проиграли - умножаем ставку для возврата потерь
        
        Args:
            initial_bet (float): Минимальная ставка
            multiplier (float): Коэффициент умножения
        """
        strategy = GameStrategy(
            name="Малые Числа (1-18)",
            description=f"Ставки на 1-18 с прогрессией {multiplier}"
        )
        
        strategy.current_bet = initial_bet
        strategy.initial_bet = initial_bet
        strategy.multiplier = multiplier
        strategy.losses_in_row = 0
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            if history:
                last_spin = history[-1]
                last_number = last_spin['number']
                
                # Проверяем выиграли ли (число от 1 до 18)
                if 1 <= last_number <= 18:
                    # Выиграли! Возвращаемся к минимальной ставке
                    strategy.current_bet = strategy.initial_bet
                    strategy.losses_in_row = 0
                else:
                    # Проиграли (0 или 19-36) - увеличиваем ставку
                    strategy.losses_in_row += 1
                    strategy.current_bet *= strategy.multiplier
            
            # Ограничиваем ставку балансом
            bet_amount = min(strategy.current_bet, strategy.balance)
            
            return {
                "type": "range",  # Новый тип ставки на диапазон
                "numbers": list(range(1, 19)),  # 1-18
                "amount": bet_amount
            }
        
        strategy.make_bet = make_bet_logic
        return strategy
    
    @staticmethod
    def high_numbers_strategy(initial_bet: float = 10, multiplier: float = 2.05) -> GameStrategy:
        """
        Стратегия 3: Ставки на большие числа (19-36)
        
        Простыми словами: Всегда ставим на числа 19-36,
        если проиграли - умножаем ставку для возврата потерь
        
        Args:
            initial_bet (float): Минимальная ставка
            multiplier (float): Коэффициент умножения
        """
        strategy = GameStrategy(
            name="Большие Числа (19-36)",
            description=f"Ставки на 19-36 с прогрессией {multiplier}"
        )
        
        strategy.current_bet = initial_bet
        strategy.initial_bet = initial_bet
        strategy.multiplier = multiplier
        strategy.losses_in_row = 0
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            if history:
                last_spin = history[-1]
                last_number = last_spin['number']
                
                # Проверяем выиграли ли (число от 19 до 36)
                if 19 <= last_number <= 36:
                    # Выиграли! Возвращаемся к минимальной ставке
                    strategy.current_bet = strategy.initial_bet
                    strategy.losses_in_row = 0
                else:
                    # Проиграли (0-18) - увеличиваем ставку
                    strategy.losses_in_row += 1
                    strategy.current_bet *= strategy.multiplier
            
            # Ограничиваем ставку балансом
            bet_amount = min(strategy.current_bet, strategy.balance)
            
            return {
                "type": "range",  # Новый тип ставки на диапазон
                "numbers": list(range(19, 37)),  # 19-36
                "amount": bet_amount
            }
        
        strategy.make_bet = make_bet_logic
        return strategy
    
    @staticmethod
    def anti_streak_strategy(initial_bet: float = 10, multiplier: float = 2.2, 
                           wait_streaks: int = 9) -> GameStrategy:
        """
        Стратегия 4: Антисерия - ставка против длинных серий
        
        Простыми словами: Ждем пока выпадет 9 раз подряд один цвет,
        потом ставим на противоположный цвет с прогрессией
        
        Args:
            initial_bet (float): Минимальная ставка
            multiplier (float): Коэффициент умножения
            wait_streaks (int): Сколько раз подряд ждать один цвет
        """
        strategy = GameStrategy(
            name=f"Антисерия {wait_streaks}",
            description=f"Ждем {wait_streaks} одного цвета, ставим на противоположный"
        )
        
        strategy.current_bet = initial_bet
        strategy.initial_bet = initial_bet
        strategy.multiplier = multiplier
        strategy.wait_streaks = wait_streaks
        strategy.current_streak = 0
        strategy.streak_color = None
        strategy.betting_active = False
        strategy.target_color = None
        strategy.losses_in_row = 0
        
        def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
            if not history:
                # Еще нет истории, пропускаем ставку
                return {"type": "skip", "numbers": [], "amount": 0}
            
            last_spin = history[-1]
            last_color = last_spin['color']
            
            if not strategy.betting_active:
                # Режим ожидания серии
                if last_color == 'green':
                    # Зеро прерывает серию
                    strategy.current_streak = 0
                    strategy.streak_color = None
                elif strategy.streak_color is None:
                    # Начинаем считать серию
                    strategy.streak_color = last_color
                    strategy.current_streak = 1
                elif last_color == strategy.streak_color:
                    # Серия продолжается
                    strategy.current_streak += 1
                    
                    if strategy.current_streak >= strategy.wait_streaks:
                        # Серия достигла нужной длины - начинаем ставить!
                        strategy.betting_active = True
                        strategy.target_color = "black" if strategy.streak_color == "red" else "red"
                        strategy.current_bet = strategy.initial_bet
                        strategy.losses_in_row = 0
                        print(f"🎯 Серия {strategy.streak_color} достигла {strategy.current_streak}! Начинаем ставить на {strategy.target_color}")
                else:
                    # Серия прервалась, начинаем сначала
                    strategy.streak_color = last_color
                    strategy.current_streak = 1
                
                # В режиме ожидания не ставим
                return {"type": "skip", "numbers": [], "amount": 0}
            
            else:
                # Режим активных ставок
                if last_color == strategy.target_color:
                    # Выиграли! Возвращаемся в режим ожидания
                    print(f"✅ Выиграли на {strategy.target_color}! Возвращаемся к ожиданию серий")
                    strategy.betting_active = False
                    strategy.current_streak = 0
                    strategy.streak_color = None
                    strategy.current_bet = strategy.initial_bet
                    return {"type": "skip", "numbers": [], "amount": 0}
                elif last_color == 'green':
                    # Зеро - просто увеличиваем ставку
                    strategy.losses_in_row += 1
                    strategy.current_bet *= strategy.multiplier
                else:
                    # Проиграли - увеличиваем ставку
                    strategy.losses_in_row += 1
                    strategy.current_bet *= strategy.multiplier
                
                # Продолжаем ставить на целевой цвет
                bet_amount = min(strategy.current_bet, strategy.balance)
                
                return {
                    "type": "color",
                    "numbers": [strategy.target_color],
                    "amount": bet_amount
                }
        
        strategy.make_bet = make_bet_logic
        return strategy


# Функция для получения всех пользовательских стратегий
def get_all_user_strategies(initial_bet: float = 10) -> List[GameStrategy]:
    """
    Возвращает все пользовательские стратегии
    
    Args:
        initial_bet (float): Начальная ставка для всех стратегий
        
    Returns:
        List[GameStrategy]: Список всех пользовательских стратегий
    """
    return [
        UserStrategies.color_following_strategy(initial_bet, 2.1),
        UserStrategies.low_numbers_strategy(initial_bet, 2.05),
        UserStrategies.high_numbers_strategy(initial_bet, 2.05),
        UserStrategies.anti_streak_strategy(initial_bet, 2.2, 9)
    ]


# Тестирование пользовательских стратегий
if __name__ == "__main__":
    print("Тестируем пользовательские стратегии...")
    
    strategies = get_all_user_strategies(10)
    
    for strategy in strategies:
        print(f"\n=== {strategy.name} ===")
        print(f"Описание: {strategy.description}")
    
    print(f"\nВсего создано {len(strategies)} пользовательских стратегий")