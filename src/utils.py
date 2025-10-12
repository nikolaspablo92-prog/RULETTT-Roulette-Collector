"""
УТИЛИТЫ ДЛЯ АНАЛИЗА РУЛЕТКИ
==========================

Этот файл содержит вспомогательные функции, которые используются во всем проекте.

Простыми словами:
- get_color() - определяет цвет числа (красный, черный, зеленый)
- is_even() - проверяет четное ли число
- get_dozen() - определяет дюжину числа (1-12, 13-24, 25-36)
- format_date() - форматирует дату для удобного отображения
- validate_number() - проверяет корректность номера в рулетке
"""

from datetime import datetime
from typing import Union, Optional


class RouletteUtils:
    """Класс с полезными функциями для работы с рулеткой"""
    
    # Красные числа в европейской рулетке
    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    
    # Черные числа в европейской рулетке  
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    
    @staticmethod
    def get_color(number: int) -> str:
        """
        Определяет цвет числа в рулетке
        
        Простыми словами: Функция берет число и говорит какого оно цвета
        
        Args:
            number (int): Число от 0 до 36
            
        Returns:
            str: "red" (красный), "black" (черный) или "green" (зеленый)
        """
        if number == 0:
            return "green"  # Зеро всегда зеленое
        elif number in RouletteUtils.RED_NUMBERS:
            return "red"    # Красные числа
        elif number in RouletteUtils.BLACK_NUMBERS:
            return "black"  # Черные числа
        else:
            return "unknown"  # На случай ошибки
    
    @staticmethod
    def is_even(number: int) -> bool:
        """
        Проверяет четное ли число
        
        Простыми словами: Проверяет делится ли число на 2 без остатка
        
        Args:
            number (int): Число для проверки
            
        Returns:
            bool: True если четное, False если нечетное
        """
        if number == 0:
            return None  # Зеро не считается ни четным ни нечетным в рулетке
        return number % 2 == 0
    
    @staticmethod
    def get_dozen(number: int) -> Optional[int]:
        """
        Определяет к какой дюжине относится число
        
        Простыми словами: Разделяет числа на 3 группы по 12 штук
        
        Args:
            number (int): Число от 0 до 36
            
        Returns:
            int: 1 (первая дюжина 1-12), 2 (вторая 13-24), 3 (третья 25-36) или None для зеро
        """
        if number == 0:
            return None  # Зеро не входит ни в какую дюжину
        elif 1 <= number <= 12:
            return 1  # Первая дюжина
        elif 13 <= number <= 24:
            return 2  # Вторая дюжина
        elif 25 <= number <= 36:
            return 3  # Третья дюжина
        else:
            return None
    
    @staticmethod
    def get_column(number: int) -> Optional[int]:
        """
        Определяет к какой колонке относится число
        
        Простыми словами: Разделяет числа на 3 вертикальные группы
        
        Args:
            number (int): Число от 0 до 36
            
        Returns:
            int: 1, 2 или 3 (номер колонки) или None для зеро
        """
        if number == 0:
            return None
        return ((number - 1) % 3) + 1
    
    @staticmethod
    def validate_number(number: Union[int, str]) -> bool:
        """
        Проверяет корректность номера для рулетки
        
        Простыми словами: Проверяет что число подходит для игры в рулетку
        
        Args:
            number: Число для проверки
            
        Returns:
            bool: True если число корректное (0-36), False если нет
        """
        try:
            num = int(number)
            return 0 <= num <= 36
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def format_date(date: datetime, format_type: str = "full") -> str:
        """
        Форматирует дату для удобного отображения
        
        Простыми словами: Превращает дату в красивый текст
        
        Args:
            date (datetime): Дата для форматирования
            format_type (str): Тип форматирования ("full", "short", "time")
            
        Returns:
            str: Отформатированная дата
        """
        if format_type == "full":
            return date.strftime("%d.%m.%Y %H:%M:%S")  # 01.01.2024 15:30:45
        elif format_type == "short":
            return date.strftime("%d.%m.%Y")           # 01.01.2024
        elif format_type == "time":
            return date.strftime("%H:%M:%S")           # 15:30:45
        else:
            return str(date)
    
    @staticmethod
    def calculate_payout(bet_type: str, bet_amount: float, winning_number: int, bet_numbers: list) -> float:
        """
        Рассчитывает выплату за ставку
        
        Простыми словами: Считает сколько денег выиграл игрок
        
        Args:
            bet_type (str): Тип ставки ("number", "color", "even_odd", "dozen", "column", "range", "skip")
            bet_amount (float): Размер ставки
            winning_number (int): Выигрышное число
            bet_numbers (list): На что поставил игрок
            
        Returns:
            float: Размер выплаты (0 если проиграл)
        """
        # Коэффициенты выплат в рулетке
        payouts = {
            "number": 35,      # Ставка на одно число: 1 к 35
            "color": 1,        # Ставка на цвет: 1 к 1
            "even_odd": 1,     # Ставка на четность: 1 к 1
            "dozen": 2,        # Ставка на дюжину: 1 к 2
            "column": 2,       # Ставка на колонку: 1 к 2
            "range": 1,        # Ставка на диапазон (1-18, 19-36): 1 к 1
            "skip": 0          # Пропуск ставки
        }
        
        # Проверяем выиграла ли ставка
        won = False
        
        if bet_type == "skip":
            # Пропуск ставки - нет выплаты, но и нет потери
            return bet_amount  # Возвращаем ставку обратно
        elif bet_type == "number":
            won = winning_number in bet_numbers
        elif bet_type == "color":
            winning_color = RouletteUtils.get_color(winning_number)
            won = winning_color in bet_numbers
        elif bet_type == "even_odd":
            is_winning_even = RouletteUtils.is_even(winning_number)
            won = ("even" in bet_numbers and is_winning_even) or ("odd" in bet_numbers and not is_winning_even)
        elif bet_type == "dozen":
            winning_dozen = RouletteUtils.get_dozen(winning_number)
            won = winning_dozen in bet_numbers
        elif bet_type == "column":
            winning_column = RouletteUtils.get_column(winning_number)
            won = winning_column in bet_numbers
        elif bet_type == "range":
            # Ставка на диапазон чисел (например 1-18 или 19-36)
            won = winning_number in bet_numbers
        
        # Возвращаем выплату
        if won:
            return bet_amount * (payouts.get(bet_type, 0) + 1)  # +1 потому что возвращается и ставка
        else:
            return 0.0


def print_roulette_info():
    """
    Выводит информацию о европейской рулетке
    
    Простыми словами: Показывает как устроена рулетка
    """
    print("=== ИНФОРМАЦИЯ О ЕВРОПЕЙСКОЙ РУЛЕТКЕ ===")
    print(f"Всего чисел: 37 (от 0 до 36)")
    print(f"Красных чисел: {len(RouletteUtils.RED_NUMBERS)} - {sorted(RouletteUtils.RED_NUMBERS)}")
    print(f"Черных чисел: {len(RouletteUtils.BLACK_NUMBERS)} - {sorted(RouletteUtils.BLACK_NUMBERS)}")
    print(f"Зеленых чисел: 1 - [0]")
    print("=" * 40)


# Тест функций (запускается при запуске файла напрямую)
if __name__ == "__main__":
    print("Тестируем утилиты для рулетки...")
    
    # Тестируем определение цвета
    test_numbers = [0, 1, 2, 17, 23, 36]
    print("\nТест определения цветов:")
    for num in test_numbers:
        color = RouletteUtils.get_color(num)
        print(f"Число {num}: {color}")
    
    # Тестируем определение четности
    print("\nТест определения четности:")
    for num in test_numbers:
        even = RouletteUtils.is_even(num)
        if even is None:
            print(f"Число {num}: зеро (ни четное, ни нечетное)")
        else:
            print(f"Число {num}: {'четное' if even else 'нечетное'}")
    
    # Тестируем определение дюжин
    print("\nТест определения дюжин:")
    for num in test_numbers:
        dozen = RouletteUtils.get_dozen(num)
        if dozen:
            print(f"Число {num}: {dozen}-я дюжина")
        else:
            print(f"Число {num}: зеро (не в дюжине)")
    
    # Показываем информацию о рулетке
    print_roulette_info()
    
    print("\nТесты завершены!")